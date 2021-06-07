import streamlit as st

import numpy as np
import pandas as pd
import datetime

import requests

from data.get_data.py import get_lstm_training_data()
##Header
st.markdown("""# This is a header
## This is a sub header
This is text""")

#InputData -choose stocks and timeframe
starting_date = st.date_input('starting prediction time', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
prediction_time = st.time_input('prediction timeframe', value=datetime.datetime(2012, 10, 6, 12, 10, 20))

stocks_count = st.number_input('stocks count', min_value=1, max_value=20, step=1, value=1)
stoks_name = st.text_input('pickup latitude')

#show the graph

data = 
@st.cache
def get_line_chart_data():
    print('get_line_chart_data called')
    return pd.DataFrame(
            np.random.randn(2000, 2018),
            columns=['data', 'prediction']
        )

df = get_line_chart_data()

st.line_chart(df)







# enter here the address of your flask api - fehlt da nicht noch /predict
url = 'http://127.0.0.1:8000 '

params = dict(
    starting_date=starting_date,
    prediction_time =prediction_time ,
    stocks_count=stocks_count)

response = requests.get(url, params=params)

prediction = response.json()

pred = prediction['prediction']

pred