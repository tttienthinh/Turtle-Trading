from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib
from backtesting.test import SMA, GOOG
from function import *

# SMACross
class SmaCross(Strategy):

    def init(self): # Params ma1, ma2, size
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy(size=0.01)
        elif crossover(self.ma2, self.ma1):
            self.sell(size=0.01)

# Turtle Trading
class TurtleTrading(Strategy):
    nO = 55
    nC = 20
    factor = 10 # A travailler dessus

    def init(self):
        data = self.data
        self.dcO = self.I(donchian_channel, data.High, self.nO, False)
        self.dcC = self.I(donchian_channel, data.Low, self.nC, True)
        self.atr = self.I(talib.ATR, data.High, data.Low, data.Close, 14)
        self.size = []

    def next(self):
        if self.dcO[-1] == self.data.High:
            size = (self.data.Close[-1]-self.dcC[-1])/(self.atr[-1]*self.factor)
            self.size.append(size)
            self.buy(size=min(size, 0.01))
        for trade in self.trades:
            if trade.is_long:
                trade.sl = self.dcC[-1]