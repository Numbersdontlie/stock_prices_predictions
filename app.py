from os import pread
import streamlit as st
import numpy as np
import pandas as pd
import datetime
import requests
#from get_data import get_lstm_training_data
from stock_prices_predictions.get_data import get_lstm_training_data
import raw_data
##Header
st.markdown("""# Stock price prediction""")
            
            
# multiselection
# multiselection Tara
st.markdown("""## Choose your stock/stocks""")
stocks = ["AMZN", "AAPL", "NVDA", "MA",
          "UNH", "PG", "JPN",  "ABBE", "INTC", "T"]
option = st.multiselect('Select a line to filter', stocks, default=stocks[0])
# choosing a stock
@st.cache
def get_select_box_data():
    ticker_list = ["AMZN", "AAPL", "NVDA", "MA", "UNH", "PG", "JPN",  "ABBE", "INTC", "T"]
    df_list = []
    for ticker in ticker_list:
        df_ticker = pd.DataFrame({"ticker": [ticker]*18,
                            "adj_close": np.random.randn(18),
                            "date": list(range(1,19))})
                            #“date”: pd.to_datetime(‘13000101’, format=‘%Y%m%d’, errors=‘ignore’))})
                           #“date”: pd.Series([‘3/11/2000’, ‘3/12/2000’, ‘3/13/2000’] * 1000))})
                            #
        df_list.append(df_ticker)
    return pd.concat(df_list)


# enter here the address of your flask api - fehlt da nicht noch /predict
url = "http://127.0.0.1:8000"
#url = "http://localhost:8501"
params = dict(
    #starting_date=starting_date,
    #prediction_time =prediction_time ,
    stocks_count=1)
response = requests.get(url, params=params)
prediction = response.json()
pred = prediction['prediction']
pred

# load dataset Tara
@st.cache
def get_dataframe_data(file, cols):
    print('get_dataframe_data called')
    df = pd.read_csv(file, usecols=cols)
    return df

@st.cache
def get_dataframe_pivoted(df, tickers):
    df_ticker = df[df['ticker'].isin(tickers)].copy()
    df_pivot = df_ticker.pivot(index='date', columns='ticker')
    df_pivot.columns = [s2 for (s1, s2) in df_pivot.columns.tolist()]
    df_pivot.index.name = None
    return df_pivot
# evtl Ordner der df.csv Datei anpassen
df = get_dataframe_data("./raw_data/df.csv", ["ticker", "adj_close", "date"])
df_piv = get_dataframe_pivoted(df, option)
st.write(df_piv)

# Hier die [-20:] anpassen um andere Daten angezeigt zu bekommen
st.line_chart(df_piv[-20:])
st.write("Working")

### - - - - - - - - - - - - - - - - - - - - - - - - - ###
### - - - - - - - - - - - - SIDEBAR- - - - - - - - - -###
### - - - - - - - - - - - - - - - - - - - - - - - - - ###
st.sidebar.markdown(f""" Menu """)
font_size = st.sidebar.slider#(‘Changer header size’, 16, 72, 36)
FONT_SIZE_CSS = f"""
<style>
h1 {{
    font-size: {font_size}px !important;
}}
</style>
"""
st.write(FONT_SIZE_CSS, unsafe_allow_html=True)
### - - - - - - - - - - - - - - - - - - - - - - - - - ###
### - - - - - - -Organize your code - - - - - - - - - ###
### - - - - - - - - - - - - - - - - - - - - - - - - - ###
def my_widget(key):
    clicked = st.button(key)
# This works in the main area
clicked = my_widget("first")
# ...and within an expander
my_expander = st.beta_expander("Expand", expanded=True)
with my_expander:
    clicked = my_widget("second")
# ...and in st.sidebar!
with st.sidebar:
    clicked = my_widget("Create my portfolio")