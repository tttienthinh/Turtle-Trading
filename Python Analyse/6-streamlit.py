import streamlit as st
import talib
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.graph_objects as go
import Strategy

# Sidebar
st.title("4T Funds")
st.sidebar.header('4T Funds')
ticker = st.sidebar.text_input('Choix du Ticker', 'BTC-USD')
option = st.sidebar.selectbox(
    'Quelle stratégie mettre en place ?',
    Strategy.Strategy.keys())

# Calcul
df = yf.download(tickers=ticker)
df.drop("Adj Close", axis=1, inplace=True)

df = Strategy.Strategy[option](df)
df = Strategy.traitement(df)


# Tabs
tab1, tab2, tab3 = st.tabs(["Marché", "Trades", "Modèle"])

with tab1:
    st.header(f'Cours du {ticker}')
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df.Open, high=df.High, low=df.Low, close=df.Close))
    st.plotly_chart(fig)

# st.plotly_chart(fig)

with tab2:
    st.header('Ensemble de trades')
    st.table(df[df.In].loc[:, ["dateOut", "gain"]])
    st.header('Nombre de trades')
    st.table(df.groupby("Statut").gain.agg(['mean', 'count']))
    st.header('Gain')
    st.area_chart(df.gain-1)
    st.header('Gain cumulé')
    st.line_chart(df.gainCum)



