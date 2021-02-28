import json
import yahoofinance
import requests
import secrets
import math
from termcolor import colored
import datetime
import common
import os
import sys

class Portfolio():
    def __init__(self, path : str = "data"):

        self.path = path
        success, latest_data = load_data(os.path.join(path, "latest_status.json"), tolerateException=True)
        if(not success):
            self.generate_latest()
        
        _, init_data = load_data(os.path.join(path, "port_initial.json"), tolerateException=False)
        
        self.original_amount = init_data["originalAmount"]

        # If there is no latest position data then we use the intial positions and amount.
        if(success):
            self.positions = latest_data["positions"]
            self.amount = latest_data["currentAmount"]
        else:
            self.positions = init_data["initialPositions"]
            self.amount = init_data["originalAmount"]


    # Not complete
    def generate_latest(self):
        most_current = None
        now  = datetime.datetime.today()
        for path in os.listdir(os.path.join(self.path, "daily")):
            print(path)
            if("log_" in path):
                time = datetime.datetime.strptime(path[4:path.rfind(".json")], common.DATE_FORMAT)
                if(most_current == None or abs((now - time).seconds) < abs((now - most_current).seconds)):
                    most_current = time
                    print(time, (now - time).seconds,  most_current, (now - most_current).seconds)
                            

    '''
    The "initial" file contaings immutable data abount the portfolio. Settings can be changed after init. 
    '''
    @staticmethod
    def create_new(path : str, amount : float, market : str, settings : dict):
        out_file = open(os.path.join(path, "port_initial.json"), mode="w", encoding="utf8")
        
        if(out_file.writable()):
            init_json_str = json.dumps(
                {
                    "originalAmount": amount,
                    "market" : market,
                    "date" : datetime.datetime.now().strftime(common.TIME_FORMAT),
                    "initialpositions": {}
                }
            , indent=True)
            out_file.write(init_json_str)
        out_file.close()

        settings_file = open(os.path.join(path, "port_settings.json"), mode="w", encoding="utf8")

        if(settings_file.writable()):
            set_json_str = json.dumps(settings, indent=True)
            settings_file.write(set_json_str)
        settings_file.close()

        
        latest_file = open(os.path.join(path, "latest_status.json"), mode="w", encoding="utf8")

        if(latest_file.writable()):
            latest_json_str = json.dumps({"currentAmount" : amount, "positions" : {}}, indent=True)
            latest_file.write(latest_json_str)
        latest_file.close()

        return Portfolio(path)


    def save_state(self, date : datetime.datetime = None):
        datetime_obj : datetime.datetime = datetime.datetime.now() if date == None else date
        
        date_str = datetime_obj.strftime(common.DATE_FORMAT)
        time_str = datetime_obj.strftime(common.TIME_FORMAT)
        dir_path = os.path.join(self.path, "daily")
        file_path = os.path.join(dir_path, f"log_{date_str}.json")
        
        if(not os.path.isdir(dir_path)):
            os.mkdir(dir_path)

        current_status = {
            "updateTime" : time_str,
            "currentAmount" : self.amount,
            "positions" : self.positions
        }

        log_data = []
        log_file = open(file_path, mode=("r+" if os.path.exists(file_path) else "w+"), encoding="utf8")
        
        log_str = log_file.read()
        if(os.path.exists(file_path) and len(log_str) > 1):
            log_data = json.loads(log_str)

        log_file.seek(0)

        log_data.append(current_status)
        log_file.write(json.dumps(log_data, indent=True))
        log_file.close()
        
        latest_file = open(os.path.join(self.path, "latest_status.json"), "w", encoding="utf8")
        latest_file.write(json.dumps(current_status, indent=True))
        latest_file.close()


    def get_stocks(self):
        return list(self.positions.keys())

    def create_positions(self, provider, num_positions = 5):
        symbols = yahoofinance.get_gainers()[:num_positions]
        price_per_position = self.original_amount / num_positions
        data = provider.get_stocks_data(symbols)
        for symbol in symbols:
            price = data[symbol]["quote"]["latestPrice"]
            num_shares = int(math.floor(price / price_per_position))
            self.register_purchase(symbol, price, num_shares)

    # If "sold" is False then a buy is logged.
    def update_buy_sell_log(self, symbol : str, sold : bool):
        file_path = os.path.join(self.path, "log_buy_sell.txt")
        log_file = open(file_path, mode="a+", encoding="utf8")
        status_str = f"[SOLD {symbol.upper()}]" if sold else f"[BOUGHT {symbol.upper()}]"
        log_str = ""
        buy_price = float(self.positions[symbol]["buyPrice"])
        if(sold):
            delta = self.get_profit(symbol)
            latest_price = self.positions[symbol]["latestPrice"]
            log_str = ("Profit" if delta > 0 else "Loss")+f": {round(delta, 2)} "+f"Bought at {round(buy_price, 2)}, sold at { round(latest_price, 2) }."
        else:
            num_shares = self.positions[symbol]["numShares"]
            log_str = f"Bought {num_shares} shares at {buy_price}."

        print(colored(status_str, "green" if not sold else "red"), log_str)
        log_file.write(status_str+" "+log_str+"\n")
        
        
    def register_purchase(self, symbol, price, num_shares):
        if(symbol in self.positions.keys()):
            self.positions[symbol]["numShares"] += num_shares
            self.positions[symbol]["latestPrice"] = price
            self.positions[symbol]["totalAmount"] = self.positions[symbol]["numShares"] * price
        else:
            self.positions[symbol] = {
                "numShares" : num_shares,
                "buyPrice" : price,
                "latestPrice" : price,
                "totalAmount": price * num_shares
            }

        self.update_buy_sell_log(symbol, sold=False)

    def register_sales(self, symbols, drop_position=False):
        for symbol in symbols:
            delta = (self.positions[symbol]["numShares"] * (self.positions[symbol]["latestPrice"] - self.positions[symbol]["buyPrice"]))
            self.amount += delta

            if(drop_position):
                self.positions.pop(symbol, None)
            else:
                self.positions[symbol]["numShares"] = 0

            self.update_buy_sell_log(symbol, sold=True)

    def get_positions_value(self):
        result = 0.0
        for position in self.positions.values():
            result += position["latestPrice"] * position["numShares"]

        return result


    def get_profit(self, symbol):
        return self.positions[symbol]["latestPrice"] - self.positions[symbol]["buyPrice"]

    def get_profit_percentage(self, stock = None):
        return (self.amount / self.original_amount) if stock == None else self.positions["buyPrice"] / self.positions["latestPrice"] 

    def update_stocks(self, provider):
        stocks_data = provider.get_stocks_data(list(self.positions.keys()))
        symbols = stocks_data.keys()
        for symbol in symbols:
            self.positions[symbol]["latestPrice"] = stocks_data[symbol]["latestPrice"]
        
    def to_json(self):
        return json.dumps(self.__dict__, indent=True)

    def get_status(self):
        return {"currentAmount" : self.amount, "positions" : self.positions}


def load_data(path : str, tolerateException : bool) -> dict:
    data = {}
    success = False
    try:
        inp_file = open(path, mode="r", encoding="utf8")
        if(inp_file.readable()):
            data = json.loads(inp_file.read())
        inp_file.close()
        success = True
    except FileNotFoundError as e:
        print(colored("[FILE NOT FOUND]", "yellow" if tolerateException else "red"), f"Could not find inital portfolio file in {path}... \n Error:")
        print(e)

    return success, data

from debug import gen_rand_stock

if(__name__ == "__main__"):
    p = Portfolio("data")
    print(p.get_positions_value())
    r1 = gen_rand_stock()
    r2 = gen_rand_stock()
    p.register_purchase(r1[0],r1[1], 2)
    p.register_purchase(r2[0],r2[1], 2)
    print(p.get_positions_value())
    print(p.to_json())