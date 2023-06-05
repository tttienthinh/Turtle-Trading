from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib

from backtesting.test import SMA, GOOG


class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy(size=1.0)
        elif crossover(self.ma2, self.ma1):
            self.sell(size=1.0)


bt = Backtest(GOOG, SmaCross, commission=.002,
              exclusive_orders=True)
stats = bt.run()
print(stats)
bt.plot(filename="1-sma")