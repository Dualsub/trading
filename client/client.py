import socket, sys, os
import json
import time
import argparse
from termcolor import colored
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
import traceback

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import common

class Client():

    def __init__(self, servername):
        self.servername = servername
        self.client_soc = None

    def start(self):
        self.client_soc = socket.socket()
        self.client_soc.connect((self.servername, common.SERVER_PORT))
        print(colored("[CONNECTED]", "green") ,f"Connected to {self.servername}...")

    def try_get_data(self):
        msg = ""
        msg_len = 0
        try:
            msg_len = int(self.client_soc.recv(common.SERVER_HEADER).decode(common.SERVER_FORMAT))
        except socket.timeout:
            return
        except:
             traceback.print_exc()

        try:
            msg = str(self.client_soc.recv(msg_len).decode(common.SERVER_FORMAT))
        except socket.timeout:
            return
        except:
             traceback.print_exc()

        
        print(colored("[RECIVED]", "green") ,f"Recived message of length {msg_len}...")
        print(colored("[RECIVED]", "green") ,f"Message {msg}...")
        return json.loads(msg)
        

plt.style.use("seaborn")

span = 500

c = None
x_vals = []
y_vals = {}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Server-side trading program.')
    parser.add_argument("-a", "--adress", help="server adress", action="store")
    args = parser.parse_args()
    c =  Client("192.168.063.8" if args.adress == None else str(args.adress))
    c.start()
    fig, axs = plt.subplots(2)

    def plot_data(i):
        data = c.try_get_data()

        global y_vals
        global x_vals

        x_vals.append(datetime.datetime.now())

        if(len(x_vals) >= span):
            x_vals = x_vals[len(x_vals)-span:]


        sym = list(data.keys())[0]
        metrics = [["ema12", "ema26", "price"], ["macd", "signal", "histogram"]]
        for i in range(len(axs)):
            axs[i].cla()
            for metric in metrics[i]:
                if(metric in y_vals.keys()):
                    y_vals[metric].append(data[sym][metric])
                else:
                    y_vals[metric] = [data[sym][metric]]
                    
                if(len(y_vals[metric]) >= span):
                    y_vals[metric] = y_vals[metric][len(y_vals[metric])-span:]
                if(metric == "histogram"):
                    axs[i].plot(x_vals, y_vals[metric], label=metric.upper())
                else:
                    axs[i].plot(x_vals, y_vals[metric], label=metric.upper())


            axs[i].legend(loc='upper left')

    anim = animation.FuncAnimation(fig, plot_data, interval=200)

    plt.get_current_fig_manager().window.state('zoomed')
    plt.tight_layout()
    plt.show()