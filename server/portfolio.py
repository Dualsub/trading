import json

class Portfolio():
    def __init__(self, amount : float, stocks : list):
        self.amount = amount
        self.stocks = stocks

    def add_stock(self, stock):
        pass

    def buy_stock(self, stock):
        pass

    def sell_stock(self, stock):
        pass

    def update_stocks(self, stocks):
        pass

    def to_json(self):
        return json.dumps(self.__dict__)
