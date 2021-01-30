import math
import datetime

class Model():
    
    def __init__(self, smoothing = 2.0):
        self.smoothing = smoothing
        self.lastAvgs = {}
        self.lastMacd = {}
        self.periods = {}


    def calc_EMA(self, span : int, newPrice : float, prevAvg : float):
        weight = self.smoothing / (span + 1)
        return (newPrice * weight) + (prevAvg * (1 - weight))

    def calc_SMA(self, newPrice, prevAvg, prevPeriods):
        return (prevAvg * prevPeriods + newPrice) / (prevPeriods + 1)

    def add_data(self, stocks : dict):
        
        result = {}

        for sym in stocks.keys():
            newPrice = stocks[sym]["quote"]["latestPrice"]

            # Calc timestamp
            target_date_time_ms = stocks[sym]["quote"]["latestUpdate"]
            base_datetime = datetime.datetime( 1970, 1, 1 )
            delta = datetime.timedelta( 0, 0, 0, target_date_time_ms )
            timestamp = base_datetime + delta

            self.periods[sym] = self.periods[sym] + 1 if sym in self.periods.keys() else 1 
            
            if(not (sym in self.lastAvgs.keys())):
                self.lastAvgs[sym] = [newPrice, newPrice]

            if(not (sym in self.lastMacd.keys())):
                self.lastMacd[sym] = 0
                
            
            ema12 = self.calc_EMA(12, newPrice, self.lastAvgs[sym][0]) if 12 <= self.periods[sym] else self.calc_SMA(newPrice, self.lastAvgs[sym][0], self.periods[sym]) 
            ema26 = self.calc_EMA(26, newPrice, self.lastAvgs[sym][1]) if 26 <= self.periods[sym] else self.calc_SMA(newPrice, self.lastAvgs[sym][1], self.periods[sym]) 
            self.lastAvgs[sym][0] = ema12
            self.lastAvgs[sym][1] = ema26
            macd = (ema12 - ema26)
            signal = self.calc_EMA(9, macd, self.lastMacd[sym]) if 9 <= self.periods[sym] else self.calc_SMA(macd, self.lastMacd[sym], self.periods[sym])
            result[sym] = {
                "price" : newPrice,
                "macd" : macd,
                "signal" : signal, 
                "histogram" : (macd- signal),
                "ema12" : ema12,
                "ema26" : ema26
            }

        return result
