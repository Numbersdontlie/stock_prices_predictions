import streamlit as st
from stock_prices_predictions.one_day_prediction import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime


### - - - - - - - - - - - - - - - - - - - - - - - - - ###
### - - - - - - - - - - - - SIDEBAR- - - - - - - - - -###
### - - - - - - - - - - - - - - - - - - - - - - - - - ###
st.sidebar.title(f"""Menu""")
font_size = st.sidebar.slider#('Changer header size', 16, 72, 36)
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
    #PAGE TITLE
    st.markdown("""# Stock Price Prediction""")
    st.markdown("""## Please choose a stock and a date to predict the next day price:""")




    # USER CHOOSES STOCK
    @st.cache
    def get_select_box_data():
        print('get_select_box_data called')
        return pd.DataFrame({
            'first column': ['select stock','Amazon', 'AT&T', 'JP Morgan', 'Intel', 'Nvidia', 'Adobe', 'P&G', 'Apple', 'United Health', 'Mastercard'],#list(range(1, 11)),
            'second column': [0,'AMZN','T', 'JPM', 'INTC', 'NVDA', 'ADBE',  'PG',  'AAPL',  'UNH', 'MA']
            })

    df = get_select_box_data()

    option = st.selectbox('Select a company to predict', df['first column'])
    #option = st.multiselect('Select a line to filter', stocks, default=stocks[0])
    filtered_df = df[df['first column'] == option]

    #st.write(filtered_df)

    #user inputs date
    d = st.date_input(
        "What date you want to predict?",
        datetime.date(2015, 4, 15))
    #st.write('Your birthday is:', str(d)))

    if st.button('predict'):
        # print is visible in server output, not in the page
        data, date, real, prediction = make_prediction(filtered_df.iloc[0,1], str(d))
        graph_ = pd.concat([date, data], axis=1)
        graph_.set_index('date', inplace=True)


        # GRAPH THE PREDICTION AND PREVIOUS VALUES

        fig, ax = plt.subplots(figsize=(7, 3), dpi=100)

        #plt.figure(figsize=(10,3), dpi=100)
        ax.plot(graph_.index, graph_['adj_close'], label="previous days")
        ax.plot(graph_.index[-1], real, 'bo', label="real")  # plot x and y using blue circle markers
        ax.plot(graph_.index[-1], prediction, 'ro', label="prediction")  # plot x and y using blue circle markers
        ax.legend()
        #plt.show()
        st.pyplot(fig)



else:
    st.title('AI Trader')






