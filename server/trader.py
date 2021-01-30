import pandas as pd
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
from termcolor import colored

def getStocksData(symbols : list):
    
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
        srvr = server.Server()
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
        stocks = ["AAPL", "TSLA"]
        while True:
            stocks_data = getStocksData(stocks)
            response = m.add_data(stocks_data)
            srvr.broadcast_to_clients(response)

    
if __name__ == "__main__":
    main()