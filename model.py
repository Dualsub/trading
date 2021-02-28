import math, sys, os
import datetime
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import common

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

    def add_historic_data(self, historic_data : dict):
        pass

    '''
    Proccesses new stock data and calculates the new averages.
    '''
    def proccess_data(self, stocks_data : dict):
        
        result = {}

        for sym in stocks_data.keys():
            
            newPrice = stocks_data[sym]["latestPrice"]

            # Calc timestamp
            # target_date_time_ms = stocks_data[sym]["latestUpdate"]
            # base_datetime = datetime.datetime( 1970, 1, 1 )
            # delta = datetime.timedelta( 0, 0, 0, target_date_time_ms)
            timestamp = datetime.datetime.now() # base_datetime + delta

            self.periods[sym] = self.periods[sym] + 1 if sym in self.periods.keys() else 1 
            
            if(not (sym in self.lastAvgs.keys())):
                self.lastAvgs[sym] = [newPrice, newPrice, newPrice]

            if(not (sym in self.lastMacd.keys())):
                self.lastMacd[sym] = 0
                
            
            # Calculates SMA for stocks that have not yet been tracked for the number of periods that were requested.

            ema12 = self.calc_EMA(12, newPrice, self.lastAvgs[sym][0]) if 12 <= self.periods[sym] else self.calc_SMA(newPrice, self.lastAvgs[sym][0], self.periods[sym]) 
            ema26 = self.calc_EMA(26, newPrice, self.lastAvgs[sym][1]) if 26 <= self.periods[sym] else self.calc_SMA(newPrice, self.lastAvgs[sym][1], self.periods[sym]) 
            ema200 = self.calc_EMA(200, newPrice, self.lastAvgs[sym][2]) if 200 <= self.periods[sym] else self.calc_SMA(newPrice, self.lastAvgs[sym][2], self.periods[sym]) 
            self.lastAvgs[sym][0] = ema12
            self.lastAvgs[sym][1] = ema26
            ema200trend = ema200 - self.lastAvgs[sym][2]
            self.lastAvgs[sym][2] = ema200
            macd = (ema12 - ema26)
            signal = self.calc_EMA(9, macd, self.lastMacd[sym]) if 9 <= self.periods[sym] else self.calc_SMA(macd, self.lastMacd[sym], self.periods[sym])
            histogram = (macd - signal)

            # -1 means nothing, 0 means sold and 1 means buy.
            action_flag = -1

            if(macd < signal and histogram < 0):
                action_flag = 1
            elif(macd > signal):
                action_flag = 0

            result[sym] = {
                "price" : newPrice,
                "macd" : macd,
                "signal" : signal, 
                "histogram" : histogram,
                "ema12" : ema12,
                "ema26" : ema26,
                "ema200" : ema200,
                "ema200trend" : ema200trend,
                "timestamp" : timestamp.strftime(common.TIME_FORMAT),
                "actionFlag" : action_flag
            }

        return result