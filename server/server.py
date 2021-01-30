import socket, threading 
import sys, os
from portfolio import Portfolio
from termcolor import colored
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import common
import traceback
import random
import time

class Server():
    def __init__(self, port : int = None):
        servername = socket.gethostbyname(socket.gethostname())
        port = port if port != None else common.SERVER_PORT
        self.address = (servername, port)
        self.server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []


    def start(self):
        print(colored("[STARTING]", "green"), "Server is starting...")
        self.server_soc.bind(self.address)
        self.server_soc.listen()
        self.server_soc.settimeout(0.0000001)
        print(colored("[LISTENING]", "green") ,f"Server is listening on {self.address[0]}...")
        

    def accept_clients(self):
        try:
            conn, addr = self.server_soc.accept()
            self.clients.append((conn, addr))
            print(colored("[ACTIVE CLIENTS]", "green") , f"{len(self.clients)} clients are active.")
        except socket.timeout:
            # print(colored("[CONNECTIONS]", "yellow"), "No new connections...")
            pass
        except:
             traceback.print_exc()
        # else:
        #     raise Exception(colored("[FAIL]", "red")+" Failed to accept clients.") 
            

    def broadcast_to_clients(self, port : Portfolio):
        self.accept_clients()
        remove_buffer = []
        for client in self.clients:
            msg = port.to_json()
            msg = f"{len(msg):<{common.SERVER_HEADER}}" + msg
            try:
                client[0].send(bytes(msg, common.SERVER_FORMAT))
            except:
                print(colored("[CLIENT EXCEPTION]", "red") , f"Failed sending data to client ({client[1]}).")
                remove_buffer.append(client)

        for client in remove_buffer:
            print(colored("[REMOVED CLIENT]", "yellow") , f"Removed client with adress: {client[1]}")
            self.clients.remove(client)

# For debug

if "__main__" == __name__:
    server = Server()
    server.start()
    p = Portfolio(1000, {
        "AAPL" : { "price" : 12.34 * (0.9 + (random.random() * 0.2)), "numPeriods" : 10 }, 
        "GAME" : { "price" : 54.12 * (0.9 + (random.random() * 0.2)), "numPeriods" : 24 }
        })

    while True:
        p.stocks["AAPL"]["price"] *= (0.9 + (random.random() * 0.2))
        p.stocks["AAPL"]["numPeriods"] += 1
        p.stocks["GAME"]["price"] *= (0.9 + (random.random() * 0.2)) 
        p.stocks["GAME"]["numPeriods"] += 1 
        time.sleep(.1)
        server.broadcast_to_clients(p)