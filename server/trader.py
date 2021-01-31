import numpy as np
import requests
import secrets
import yahoofinance
import sys
import matplotlib.pyplot as plt
import datetime as dt
import model
import json
import argparse
import server
import time
import portfolio
from termcolor import colored
    
def main():
    # Parsing args
    parser = argparse.ArgumentParser(description='Server-side trading program.')
    parser.add_argument("-b", "--backtest", help=".json file to backtest with", action="store")
    parser.add_argument("-s", "--save", help="whether or not to save the data generated in the session", action="store_true")
    parser.add_argument("-d", "--dest", help="destination of the the data generated in the session", action="store")
    parser.add_argument("-o", "--offline", help="whether to launch the program in an offline state", action="store_false")
    args = parser.parse_args()

    srvr = None
    if(args.offline):
        srvr = server.Server(servername="192.168.0.63")
        srvr.start()

    dest = args.dest if args.dest != None else sys.path
    if(args.save):
        print(colored("[SAVING]", "green") ,f"The data will be saved to {dest} upon shutdown...")

    m = model.Model()


    if(args.backtest != None):
        inp_file = open(str(args.backtest), mode="r", encoding="utf8").read()
        stocks_data = json.loads(inp_file)
        result = []
        for stock in stocks_data:
            sym = str(stock["symbol"])
            price = float(stock["close"])
            response = m.add_data({ sym : { "quote": {"latestPrice" : price, "latestUpdate" : 18967987}}})
            result.append(result)
            srvr.broadcast_to_clients(response)
            time.sleep(.1)
    else:
        p = portfolio.Portfolio(100000)
        p.create_positions()
        time.sleep(5)
        p.update_stocks()
        print("Stocks:",p.get_stocks())
        print("Profit:",p.get_profit())
        print("Profit Percantage:", str(round((p.get_profit_percentage() - 1) * 100, 2))+"%")
        stocks = p.get_stocks()
        while True:
            stocks_data = portfolio.get_stocks_data(stocks)
            response = m.add_data(stocks_data)
            srvr.broadcast_to_clients(response)

    
if __name__ == "__main__":
    main()