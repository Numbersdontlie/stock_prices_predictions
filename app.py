from os import pread
import streamlit as st
import numpy as np
import pandas as pd
import datetime
import requests
#import plotly.express as px
import altair as alt
from stock_prices_predictions.one_day_prediction import *

from stock_prices_predictions.get_data import get_lstm_training_data
import raw_data
### - - - - - - - - - - - - - - - - - - - - - - - - - ###
### - - - - - - -API- - - - - - - - - - - - - - - - - ###
### - - - - - - - - - - - - - - - - - - - - - - - - - ###
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
### - - - - - - - - - - - - - - - - - - - - - - - - - ###
### - - - - - - -select/choose stocks - - - - - - - - ###
### - - - - - - - - - - - - - - - - - - - - - - - - - ###
st.markdown("""## Choose your stock/stocks""")
stocks = ["AMZN", "AAPL", "NVDA", "MA",
          "UNH", "PG", "JPN",  "ABBE", "INTC", "T"]
option = st.multiselect('Select a line to filter', stocks, default=stocks[0])
st.write(option)


### - - - - - - - - - - - - - - - - - - - - - - - - - ###
### - - - - - - -load dataset- - -  - - - - - - - - - ###
### - - - - - - - - - - - - - - - - - - - - - - - - - ###
# evtl Ordner der df.csv Datei anpassen
@st.cache
def get_dataframe_data(file, cols, num_rows):
    print('get_dataframe_data called')
    df = pd.read_csv(file, usecols=cols)
    df_grouped = df.sort_values('date').groupby('ticker').tail(num_rows)
    return df_grouped

df = get_dataframe_data("./raw_data/df.csv", ["ticker", "adj_close", "date"], 15)
df_tickers = df[df['ticker'].isin(option)].copy()
data, real, forecast = make_prediction('T', "2015-04-15")

# df_forecast = pd.read_csv('./raw_data/forecast.csv') #predictive werte
# df_forecast_tickers = df_forecast[df_forecast['ticker'].isin(option)].copy()
# st.write("DF_tickers")
st.write(forecast)

##Header
st.markdown("""# Stock price prediction""")
### - - - - - - - - - - - - - - - - - - - - - - - - - ###
### - - - - - - -plot the line- - -  - - - - - - - - - ###
### - - - - - - - - - - - - - - - - - - - - - - - - - ###

data, real, forecast = make_prediction(option[0], prediction_date)
chart_line = alt.Chart(data).mark_line(point=True).encode(
   # x='date',
    x= range(0,19),
    y='adj_close',
    #color='ticker',
    strokeDash='ticker',
    tooltip='adj_close'
) 
chart_forecast = alt.Chart(data).mark_point().encode(
    x=range(0,19),
    y='adj_close',
    color='ticker',
    strokeDash='ticker',
    tooltip='adj_close'
)

charts = alt.layer(chart_line, chart_forecast)
# print(c)
st.altair_chart(charts, use_container_width=True)
# Hier die [-20:] anpassen um andere Daten angezeigt zu bekommen           

### - - - - - - - - - - - - - - - - - - - - - - - - - ###
### - - - - - - - - - - - - SIDEBAR- - - - - - - - - -###
### - - - - - - - - - - - - - - - - - - - - - - - - - ###
st.sidebar.title(f"""Menu """)
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
### - - - - SIDEBAR PAGE OPTIONS - - - - - - - - - - -###
### - - - - - - - - - - - - - - - - - - - - - - - - - ###
my_page = st.sidebar.radio('', ['Stock Price Prediction', 'AI Trader'])
if my_page == 'Stock Price Prediction':
    st.title('Stock Price Prediction')
    button = st.button('back')
    if button:
        st.write('clicked')
else:
    st.title('AI Trader')
### - - - - - - - - - - - - - - - - - - - - - - - - - ###
### - - - - - - -Organize your code - - - - - - - - - ###
### - - - - - - - - - - - - - - - - - - - - - - - - - ###
# def my_widget(key):
#     clicked = st.button(key)
# # This works in the main area
# clicked = my_widget("first")
# # ...and within an expander
# my_expander = st.beta_expander("Expand", expanded=True)
# with my_expander:
#     clicked = my_widget("second")
# # ...and in st.sidebar!
# with st.sidebar:
#     clicked = my_widget("Create my portfolio")
### - - - - - - - - - - - - - - - - - - - - - - - - - ###
### - - - - - - -Portfolio construction - - - - - - - - - ###
### - - - - - - - - - - - - - - - - - - - - - - - - - ###

@st.cache
def get_dataframe_data_AI(file, cols, num_rows):
    print('get_dataframe_data AI called')
    df_all = pd.read_csv(file, usecols=cols)
    df_all_grouped = df.sort_values('date').groupby('ticker')#.tail(num_rows)
    return df_all_grouped

df_all = get_dataframe_data_AI("./raw_data/df.csv", ["ticker", "adj_close", "date"], 15)
df_AI = pd.read_csv('./raw_data/forecast.csv') #predictive werte
df_forecast_tickers = df_forecast[df_forecast['ticker'].isin(option)].copy()
st.write("DF_tickers")
st.write(df_tickers)

#User input start and end date
start_date = st.date_input('Start date',datetime.date(2015,1,1))
end_date = st.date_input('End date',datetime.date(2015,12,31))
#st.write(date)
if start_date < end_date:
    st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))

else:
    st.error('Error: End date must fall after start date.')
    
    
#graph zeichnen, der
chart_lines = alt.Chart(df_tickers).mark_line(point=True).encode(
    x='date',
    y='adj_close',
    color='ticker',
    strokeDash='ticker',
    tooltip='adj_close'
) 
chart_forecast = alt.Chart(df_forecast_tickers).mark_point().encode(
    x='date',
    y='adj_close',
    color='ticker',
    strokeDash='ticker',
    tooltip='adj_close'
)

charts = alt.layer(chart_line, chart_forecast)
# print(c)
st.altair_chart(charts, use_container_width=True)