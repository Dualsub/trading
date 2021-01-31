import json
import yahoofinance
import requests
import secrets
import math

class Portfolio():
    def __init__(self, amount : float, positions : dict = {}):
        self.original_amount = amount
        self.amount = amount
        self.positions = positions

    def get_stocks(self):
        return list(self.positions.keys())

    def create_positions(self, num_positions = 5):
        symbols = yahoofinance.get_gainers()[:num_positions]
        price_per_position = self.original_amount / num_positions
        data = get_stocks_data(symbols)
        for symbol in symbols:
            price = data[symbol]["quote"]["latestPrice"]
            num_shares = int(math.floor(price / price_per_position))
            self.buy_stock(symbol, price, num_shares)


    def buy_stock(self, stock, price, num_shares):
        self.positions[stock] = {
            "numShares" : num_shares,
            "buyPrice" : price,
            "latestPrice" : price
        }

    def sell_stock(self, stock, price):
        delta = (self.positions[stock]["numShares"] * (price - self.positions[stock]["buyPrice"]))
        print(delta)
        self.amount += delta

    def get_profit(self, stock = None):
        return self.original_amount - self.amount if stock == None else self.positions["latestPrice"] - self.positions["buyPrice"] 

    def get_profit_percentage(self, stock = None):
        return (self.amount / self.original_amount) if stock == None else self.positions["buyPrice"] / self.positions["latestPrice"] 


    def update_stocks(self):
        stocks = get_stocks_data(list(self.positions.keys()))
        for symbol in stocks.keys():
            self.positions[symbol]["latestPrice"] = stocks[symbol]["quote"]["latestPrice"]
            self.amount += self.positions[symbol]["latestPrice"] - self.positions[symbol]["buyPrice"] 
    
    def to_json(self):
        return json.dumps(self.__dict__)

def get_stocks_data(symbols : list):
    symbols = list(symbols)
    symbols_str = symbols[0]
    for sym in symbols[1:]:
        symbols_str += ","+sym

    url ="https://sandbox.iexapis.com/stable/stock/market/batch?symbols="+symbols_str+"&types=quote&token="+secrets.SECRET_KEY
    
    response = requests.get(url)
    if(response.status_code != 200):
        print("Failed to retrive stock data.\nError Code:", response.status_code)
        return None

    data = response.json()
    return data