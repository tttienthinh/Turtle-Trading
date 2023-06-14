import talib # pip install TA-Lib
# Des logiciels suplémentaires peuvent être nécessaires pour talib
# https://pypi.org/project/TA-Lib/
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def donchian_channel(serie, n, lower):
    serie = pd.Series(serie)
    if lower:
        return serie.rolling(n).min()
    else:
        return serie.rolling(n).max()

nO = 55
nC = 20

df = yf.download(tickers='BTC-USD')
df.drop("Adj Close", axis=1, inplace=True)
df["dcO"] = donchian_channel(df.High, nO, False) # Chaine de Donchian supérieur
df["dcC"] = donchian_channel(df.Low,  nC, True)  # Chaine de Donchian inférieur
df["atr"] = talib.ATR(df.High, df.Low, df.Close, 14) # ATR pas si important pour l'instant
df.dropna(inplace=True)

plt.plot(df.Close)
plt.plot(df.dcO)
plt.plot(df.dcC)
plt.show()

# Lire 
# https://www.newtrading.fr/turtle-trading#h-quelles-sont-les-regles-du-turtle-trading
""" 
Je suis le système 2 décrit dans cette article.
Je voudrais rajouter dans le dataframe df, les colonnes In et Out qui vaudrait True ou False.
In:
 - True, lorsqu'il faut acheter
 - False, le reste du temps
Out:
 - True, lorsqu'il faut revendre la position
 - False, le reste du temps
"""

"""
L'objectif à terme serait d'avoir un nouveau dataframe Trades
avec ces infos (comme dans 6-TurtleTrading.py) : 
['Size', 'EntryBar', 'ExitBar', 'EntryPrice', 'ExitPrice', 'PnL',
'ReturnPct', 'EntryTime', 'ExitTime', 'Duration', 'vanillaPNL', 'DcC',
'DcC_ratio', 'equity']
"""