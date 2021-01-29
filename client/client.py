import socket, sys, os
import json
import time
from termcolor import colored

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import common

class Client():

    def __init__(self, servername):
        self.servername = servername

    def start(self):
        client_soc = socket.socket()
        client_soc.connect((self.servername, common.SERVER_PORT))
        print(colored("[CONNECTED]", "green") ,f"Connected to {self.servername}...")

    def try_get_data(self):
        pass

if __name__ == "__main__":
    c = Client("192.168.131.7")
    c.start()
    
