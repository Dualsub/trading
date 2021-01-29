import socket, threading 
import sys, os
from portfolio import Portfolio
from termcolor import colored
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import common
import traceback

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
        for addr, conn in self.clients:
            conn.send(common.SERVER_HEADER)
            msg = port.to_json().encode(common.SERVER_FORMAT)         
            conn.send(msg)
            if(msg_length != None):
                msg_length = int()
                msg = conn.rcv(msg_length).decode(common.SERVER_FORMAT)
                print(f"[{addr}]", msg)
                if(msg == common.SERVER_DICONNECT_MSG):
                    break

if "__main__" == __name__:
    server = Server()
    server.start()

    while True:
        server.accept_clients()