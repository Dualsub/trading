import socket, sys, os
import json
import time
import argparse
from termcolor import colored
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import RadioButtons
import datetime
import traceback
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import common
from model import Model

plt.style.use("seaborn")

def proccess_data(symbol):
    data, _ = init_data(symbol)

    original_amount = 12000
    current_amount = original_amount
    last_amount = original_amount
    flag = -1
    num_shares = 0
    latest_price = 0

    num_profits = 0
    num_losses = 0
    largest_profit = 0.0
    largest_loss = 0.0

    for i in range(len(data)):
        entry = data[i]
        latest_price = entry["price"]
        if(entry["actionFlag"] > -1):
            if(entry["actionFlag"] == 1 and (flag == -1 or flag == 0)):
                num_shares = int(current_amount / entry["price"])
                current_amount -= (entry["price"] * num_shares + 0)
                flag = 1
            elif(entry["actionFlag"] == 0 and flag == 1):
                flag = 0
                current_amount += entry["price"] * num_shares
                profit = current_amount - last_amount
                last_amount = current_amount
                num_shares = 0

                if(profit > largest_profit):
                    largest_profit = profit
                if(profit < largest_loss):
                    largest_loss = profit

                if(profit > 0):
                    num_profits += 1
                if(profit < 0):
                    num_losses += 1

    if(num_shares > 0):
        current_amount += latest_price * num_shares

    profit_percentage = (float(current_amount) / float(original_amount)) - 1

    return current_amount, original_amount, profit_percentage, num_profits, num_losses, largest_profit, largest_loss


def plot_data(symbol, save):

    data, x_vals = init_data(symbol)

    price_vals = []
    ema12_vals = []
    ema26_vals = []
    ema200_vals = []
    histo_vals = []
    macd_vals = []
    signal_vals = []

    signal_sell_x = []
    signal_buy_x = []
    signal_buy = []
    signal_sell = []

    original_amount = 12000
    current_amount = original_amount
    last_amount = current_amount
    latest_price = 0
    flag = -1
    num_shares = 0

    tot_profit = 0.0
    num_profits = 0
    num_losses = 0
    largest_profit = 0.0
    largest_loss = 0.0

    for i in range(len(data)):
        entry = data[i]
        latest_price = entry["price"]
        price_vals.append(entry["price"])
        ema12_vals.append(entry["ema12"])
        ema26_vals.append(entry["ema26"])
        ema200_vals.append(entry["ema200"])

        histo_vals.append(entry["histogram"])
        signal_vals.append(entry["signal"])
        macd_vals.append(entry["macd"])


        if(entry["actionFlag"] > -1):

            if(entry["actionFlag"] == 1 and (flag == -1 or flag == 0)):
                num_shares = int(current_amount / entry["price"])
                current_amount -= (entry["price"] * num_shares + 0)
                signal_buy.append(entry["price"])
                signal_buy_x.append(x_vals[i])
                flag = 1
            elif(entry["actionFlag"] == 0 and flag == 1):
                flag = 0
                current_amount += entry["price"] * num_shares
                num_shares = 0
                profit = current_amount - last_amount
                last_amount = current_amount
                print("Current:", round(current_amount, 2), "Profit:", round(profit, 2))

                signal_sell.append(entry["price"])
                signal_sell_x.append(x_vals[i])

                if(profit > largest_profit):
                    largest_profit = profit
                if(profit < largest_loss):
                    largest_loss = profit

                if(profit > 0):
                    num_profits += 1
                if(profit < 0):
                    num_losses += 1

    if(num_shares > 0):
        current_amount += latest_price * num_shares


    print("\nTotal Profit:".ljust(21),round(current_amount - original_amount, 2))
    print("Profit Percentage:".ljust(20),str(round((float(current_amount)*100 / float(original_amount)) - 100, 1))+"%")
    print("Amount:".ljust(20),round(current_amount, 2))
    print("Investment:".ljust(20),round(original_amount, 2))
    print("Periods:".ljust(20), len(x_vals))
    print("Number Of Trades:".ljust(20), num_profits+num_losses)
    print("Number Of Profits:".ljust(20),num_profits)
    print("Number Of Losses:".ljust(20),num_losses)
    print("Profit Percentage:".ljust(20), str(round(float(num_profits)*100 / float(num_profits+num_losses), 1))+"%")
    print("Largest Profit:".ljust(20),round(largest_profit, 2))
    print("Largest Loss:".ljust(20),round(largest_loss, 2))
    
    fig, axs = plt.subplots(2)

    axs[0].plot(x_vals, price_vals, label="Price", alpha=0.6)
    axs[0].plot(x_vals, ema12_vals, label="EMA12", alpha=0.6)
    axs[0].plot(x_vals, ema26_vals, label="EMA26", alpha=0.6)
    axs[0].plot(x_vals, ema200_vals, label="EMA200", alpha=0.6)

    axs[0].scatter(signal_buy_x, signal_buy, label="Buy", color="green", marker="^", alpha=1)
    axs[0].scatter(signal_sell_x, signal_sell, label="Sell", color="red", marker="v", alpha=1)

    
    axs[1].plot(x_vals, macd_vals, label="MACD")
    axs[1].plot(x_vals, signal_vals, label="SIGNAL")
    axs[1].fill_between(x_vals, histo_vals, label="histogram", alpha=0.6)

    axs[0].legend()
    axs[1].legend()
    axs[0].title.set_text(symbol)
    plt.xlabel("Profit Percentage: "
    +str(round((float(current_amount)*100 / float(original_amount)) - 100, 1))+"%, Profit-rate: "
    +str(round(float(num_profits)*100 / float(num_profits+num_losses), 1))+"%, Number of Periods: "
    +str(len(x_vals))
    )
    if(save):
        time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        plt.savefig(f"figures/{symbol}_{time_str}")
    else:
        plt.show()


def init_data(symbol):
    backtest_data = None
    with open(os.path.join("./datasets", symbol+".json"), mode="r", encoding="utf8") as data_file:
        backtest_data = json.loads(data_file.read())
    
    m = Model()

    result = []
    timestamps = []

    for entry in backtest_data[len(backtest_data)-500:]:
        entry_result = m.proccess_data({symbol : { "latestPrice" : entry["close"]}})
        result.append(entry_result[symbol])
        timestamps.append(datetime.datetime.strptime(entry["date"], common.DATE_FORMAT))

    return result, timestamps

def backtest(symbol = None, save = False):
    if(symbol != None):
        # Look at specific ticker.
        plot_data(symbol, save)
    else:
        # Look at all tickers in "datasets" folder.
        sum_profit = 0.0 
        num_profits = 0
        num_losses = 0
        num_stocks = 0
        for dirpath, dirnames, filenames in os.walk("datasets"):
            for filename in filenames[1:]:
                if(".json" in filename):
                    symbol = filename[:filename.rindex(".json")]
                    result = proccess_data(symbol)
                    num_stocks += 1
                    sum_profit += result[2]
                    num_profits += result[3]
                    num_losses += result[4]
                    print(symbol+",", "profit:", str(round(result[2]*100, 1))+"%")


        print("\nAverage Profit:", str(round((sum_profit / num_stocks) * 100, 1))+"%")
        if((num_profits + num_losses) > 0):
            print("Win-Rate:", str(round((num_profits / (num_profits + num_losses)) * 100, 1))+"%")
        print("Num Samples:", num_stocks)
