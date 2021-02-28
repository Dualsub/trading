from termcolor import colored
import requests
import secrets


'''
class that interfaceses with data providers.
'''
class DataProvider():
    def __init__(self):
        self.max_calls_per_day = 100
        self.num_failed_attempts = 0

    def getStocks(self, symbols : list):
        return None

class IexSandbox(DataProvider):
    def __init__(self):
        self.max_calls_per_day = 500

        
    def get_stocks_data(self, symbols : list):
        symbols = list(symbols)
        symbols_str = symbols[0]
        for sym in symbols[1:]:
            symbols_str += ","+sym

        url ="https://sandbox.iexapis.com/stable/stock/market/batch?symbols="+symbols_str+"&types=quote&token="+secrets.keys["iexsandbox"]["secret"]
        
        response = requests.get(url)
        if(response.status_code != 200):
            print("Failed to retrive stock data.\nError Code:", response.status_code)
            if(self.num_failed_attempts <= 5):
                print(colored("[FAILED]", "red") ,f"There has been {self.num_failed_attempts} failed attempts...")
            else:
                print(colored("[SHUTTING DOWN]", "red") ,f"Raising error and terminating proccess...")
                raise Exception("Failed more than 4 times to retrive data.")
            return None


        self.num_failed_attempts = 0

        raw_data = response.json()

        data = {
            "latestPrice" : raw_data["latestPrice"],
            "other" : None
        }

        return data

class AlphaVantage(DataProvider):
    def __init__(self):
        self.max_calls_per_day = 500
        
    def get_stocks_data(self, symbols : list):
        symbols = list(symbols)
        symbols_str = symbols[0]
        for sym in symbols[1:]:
            symbols_str += ","+sym

        url ="https://sandbox.iexapis.com/stable/stock/market/batch?symbols="+symbols_str+"&types=quote&token="+secrets.keys["secret"]
        
        response = requests.get(url)
        if(response.status_code != 200):
            print("Failed to retrive stock data.\nError Code:", response.status_code)
            if(self.num_failed_attempts <= 5):
                print(colored("[FAILED]", "red") ,f"There has been {self.num_failed_attempts} failed attempts...")
            else:
                print(colored("[SHUTTING DOWN]", "red") ,f"Raising error and terminating proccess...")
                raise Exception("Failed more than 4 times to retrive data.")
            return None

        self.num_failed_attempts = 0

        data = response.json()
        return data

class NordNet(DataProvider):
    def __init__(self):
        self.max_calls_per_day = 500
        
    def get_stocks_data(self, symbols : list):
        symbols = list(symbols)
        symbols_str = symbols[0]
        for sym in symbols[1:]:
            symbols_str += ","+sym

        raw_data = {}

        data = {
            "latestPrice" : raw_data["latestPrice"],
            "other" : None
        }
        
        return data


def init_provider(name):
    provider_obj = {
        "alphavantage" : AlphaVantage(),
        "iexsandbox" : IexSandbox(),
        "nordnet" : NordNet()
    }[name.lower()]
    return provider_obj
    