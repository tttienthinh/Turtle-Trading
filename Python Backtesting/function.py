import pandas as pd


def donchian_channel(serie, n, lower):
    serie = pd.Series(serie)
    if lower:
        return serie.rolling(n).min()
    else:
        return serie.rolling(n).max()