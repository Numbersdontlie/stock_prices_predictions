from os import pread
import streamlit as st
import numpy as np
import pandas as pd
import datetime
import requests
from get_data import get_lstm_training_data

##Header
st.markdown("""# Stock price prediction""")
            
            
# multiselection
st.markdown("""## Choose your stock""")
@st.cache
def get_select_box_data():
    print('get_select_box_data called')
    return pd.DataFrame({
          'first column': ["AMZN", "AAPL", "NVDA", "MA", "UNH", "PG", "JPN",  "ABBE", "INTC", "T"],
        })
df = get_select_box_data()
option = st.selectbox('Select a line to filter', df['first column'])
stock_chosen = df[df['first column'] == option]
st.write(stock_chosen)


#InputData -choose stocks and timeframe
#starting_date = st.date_input(‘starting prediction time’, value=datetime.datetime(2012, 10, 6, 12, 10, 20))
#prediction_time = st.time_input(‘prediction timeframe’, value=datetime.datetime(2012, 10, 6, 12, 10, 20))
#stocks_count = st.number_input(‘stocks count’, min_value=1, max_value=20, step=1, value=1)
#stoks_name = st.text_input(‘pickup latitude’)

#show the graph
@st.cache
def get_line_chart_data():
    print('get_line_chart_data called')
    return pd.DataFrame(
            np.random.randn(18,2),
            columns=['a','b']
        )
df = get_line_chart_data()
st.line_chart(df)
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

st.markdown("""### This is text""")
