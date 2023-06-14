from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib
import pandas as pd
from backtesting.test import SMA, GOOG
import yfinance as yf





def donchian_channel(serie, n, lower):
    serie = pd.Series(serie)
    if lower:
        return serie.rolling(n).min()
    else:
        return serie.rolling(n).max()

class TurtleTrading(Strategy):
    nO = 55
    nC = 20
    factor = 10 # A travailler dssus

    def init(self):
        data = self.data
        self.dcO = self.I(donchian_channel, data.High, self.nO, False)
        self.dcC = self.I(donchian_channel, data.Low, self.nC, True)
        self.atr = self.I(talib.ATR, data.High, data.Low, data.Close, 14)
        self.size = []

    def next(self):
        # print(len(self.trades))
        # print(type(self.dcO), type(self.dcC), self.dcC[-1], len(self.dcC))
        if self.dcO[-1] == self.data.High:
            size = (self.data.Close[-1]-self.dcC[-1])/(self.atr[-1]*self.factor)
            # size = 0.1
            self.size.append(size)
            # print(size, self.data.Close[-1], self.dcC[-1], self.atr[-1], self.factor)
            self.buy(size=min(size, 0.99))
            # self.buy(size=0.8)
        for trade in self.trades:
            if trade.is_long:
                trade.sl = self.dcC[-1]




data = yf.download(tickers='BTC-USD')
bt = Backtest(data, TurtleTrading, commission=.00_06, cash=1e6)
stats = bt.run()
print(stats)
bt.plot()

results = bt._results
trades = results._trades
trades["vanillaPNL"] = trades.ExitPrice/trades.EntryPrice 
trades.Duration = [day.days for day in trades.Duration]
dcC = stats._strategy.dcC
trades["DcC"] = [dcC[i] for i in trades.EntryBar]
trades["DcC_ratio"] = trades.DcC / trades.EntryPrice
equity = stats._equity_curve
trades["equity"] = [equity.iloc[i] for i in trades.EntryBar]
trades["size"] = stats._strategy.size[:5]
len(trades)


import matplotlib.pyplot as plt
import numpy as np


col = np.where(trades.vanillaPNL<1, "red", "green")
col = np.where(trades.ReturnPct<0, "red", "green")
#     Size  EntryBar  ExitBar    EntryPrice     ExitPrice           PnL  ReturnPct  EntryTime   ExitTime  Duration  vanillaPNL
# Il faut mettre des show() après chaque plt.scatter
plt.yscale("log")
plt.scatter(trades.Duration, trades.vanillaPNL, c=col) # Logarithmique ?
plt.scatter(trades.DcC_ratio, trades.vanillaPNL, c=col)
plt.scatter(trades.Size, trades.vanillaPNL, c=col) # Size > 15 sur de gagner ?
plt.scatter(trades.Size, trades.ReturnPct, c=col)
plt.scatter(trades.EntryPrice, trades.vanillaPNL, c=col)
plt.scatter(trades.size, trades.vanillaPNL, c=col)
plt.show()
