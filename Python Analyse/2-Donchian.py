from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib
import pandas as pd
from backtesting.test import SMA, GOOG


def donchian_channel(serie, n, lower):
    serie = pd.Series(serie)
    if lower:
        return serie.rolling(n).min()
    else:
        return serie.rolling(n).max()

class Donchian(Strategy):
    nO = 55
    nC = 20
    factor = 9

    def init(self):
        data = self.data
        self.dcO = self.I(donchian_channel, data.High, self.nO, False)
        self.dcC = self.I(donchian_channel, data.Low, self.nC, True)
        self.atr = self.I(talib.ATR, data.High, data.Low, data.Close, 14)

    def next(self):
        print(len(self.trades))
        if self.dcO == self.data.High:
            size = (self.data.Close[-1]-self.dcC[-1])/(self.atr[-1]*self.factor)
            print(size, self.data.Close[-1], self.dcC[-1], self.atr[-1], self.factor)
            self.buy(size=min(size, 0.999))
        for trade in self.trades:
            if trade.is_long:
                trade.sl = self.dcC[-1]



bt = Backtest(GOOG, Donchian, commission=.00_06)
stats = bt.run()
print(stats)
# bt.plot()