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

def plot_history(symbol):

    json_file = open(f"datasets/{symbol}.json", mode="r") 
    data = json.load(json_file)
    json_file.close()

    model_data = [(dt.datetime.strptime(entry["date"], '%Y-%m-%d'), float(entry["close"])) for entry in data]
    mod = model.Model(model_data)
    # shot_EMA = mod.calc_EMA(26)
    # long_EMA = mod.calc_EMA(12)

    # MACD = []
    plt.plot()

    plt.xticks(rotation=45)
    plt.show()
    

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

    if(args.backtest != None):
        pass
        
        
if __name__ == "__main__":
    main()