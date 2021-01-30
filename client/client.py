import socket, sys, os
import json
import time
import argparse
from termcolor import colored
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime

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

c = None
x_vals = []
y1_vals = []
y2_vals = []

def plot_data(i):
    data = c.try_get_data()["stocks"]
    global y1_vals
    global y2_vals
    global x_vals

    x_vals.append(datetime.datetime.now())
    y1_vals.append(data["AAPL"]["price"])
    y2_vals.append(data["GAME"]["price"])

    if(len(y1_vals) >= 20):
        y1_vals = y1_vals[len(y1_vals)-20:]
        x_vals = x_vals[len(x_vals)-20:]

    if(len(y2_vals) >= 20):
        y2_vals = y2_vals[len(y2_vals)-20:]


    plt.cla()

    plt.plot(x_vals, y1_vals, label="AAPL")
    plt.plot(x_vals, y2_vals, label="GME")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Server-side trading program.')
    parser.add_argument("-a", "--adress", help="server adress", action="store")
    args = parser.parse_args()
    c =  Client("192.168.063.8" if args.adress == None else str(args.adress))
    c.start()
    anim = animation.FuncAnimation(plt.gcf(), plot_data, interval=200)

    plt.tight_layout()
    plt.show()





    
