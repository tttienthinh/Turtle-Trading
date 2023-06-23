import streamlit as st
import talib
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Traitement
def traitement(df, commission = 0.06/100):
    df["dateOut"] = df.apply(
        lambda x: (
            df
            .Out[x.name:]
            .idxmax()
        ),
        axis=1
    )
    df.loc[
        (df.index == df.dateOut) & np.logical_not(df.Out), 
        "dateOut"
    ] = np.nan # retrait des 
    df["gain"] = (
        df
        .apply(
            lambda x: 
            df.loc[x.dateOut, "Close"] / x.Close - commission 
            if x.In 
            else 1,
            axis=1
        )
    )
    df["gainCum"] = df.gain.cumprod()

    df["Statut"] = "Standby"
    df.loc[df.gain > 1, "Statut"] = "Gagnant"
    df.loc[df.gain < 1, "Statut"] = "Perdant"
    return df


# RSI
def RSI(df):
    df["RSI"] = talib.RSI(df.Close)
    df["In"] = (
        (df.RSI.shift(1) < 30) &
        (30 < df.RSI)
    )
    df["Out"] = (
        (df.RSI.shift(1) < 70) &
        (70 < df.RSI)
    )
    df["Size"] = 1
    return df



Strategy = {
    "RSI": RSI
}



# Test
if __name__ == "__main__":
    ticker = "BTC-USD"
    option = "RSI"
    df = yf.download(tickers=ticker)
    df.drop("Adj Close", axis=1, inplace=True)

    df = Strategy[option](df)
    df = traitement(df)