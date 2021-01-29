import math

class Model():
    
    def __init__(self, dataset : list, smoothing = 2.0):
        self.dataset = dataset
        self.smoothing = smoothing
        self.lastAvgs = {}

    def calc_EMA(self, span : int, newPrice, prevAvg):
        weight = self.smoothing / (span + 1)
        return (newPrice * weight) + (prevAvg * (1 - weight))

    def calc_SMA(self, newPrice, prevAvg, prevPeriods):
        return (prevAvg * prevPeriods + newPrice) / (prevPeriods + 1)

    def add_data(self, stocks : dict):
        for sym in stocks.keys():
            newPrice = stocks[sym]["price"]
            numPeriods = stocks[sym]["numPeriods"]
            if(sym in self.lastAvgs.keys()):
                pass

        




