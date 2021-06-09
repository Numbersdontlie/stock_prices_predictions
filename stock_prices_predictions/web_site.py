import streamlit as st
from stock_prices_predictions.one_day_prediction import *
from stock_prices_predictions.ai_portfolio import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
#import mplcursors
import altair as alt
from datetime import timedelta  


st.set_page_config(
    page_title="Stock Price Prediction",
    page_icon="🧙‍♂️",
    layout="centered",
    initial_sidebar_state="expanded")

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
    col3, col4 = st.beta_columns(2)
    with col3:
        option = st.selectbox('Select a company to predict', df['first column'])
    #option = st.multiselect('Select a line to filter', stocks, default=stocks[0])
    filtered_df = df[df['first column'] == option]

    #st.write(filtered_df)

    #user inputs date
    col5, col6 = st.beta_columns(2)
    with col5:
        d = st.date_input(
            "What date you want to predict?",
            datetime.date(2015, 4, 15))
    #st.write('Your birthday is:', str(d)))

    if st.button('predict'):
        # print is visible in server output, not in the page
        data, date, real, prediction = make_prediction(filtered_df.iloc[0,1], str(d))
        graph_ = pd.concat([date, data], axis=1)
        #graph_.set_index('date', inplace=True)
        
        
        

        # GRAPH THE PREDICTION AND PREVIOUS VALUES

        fig, ax = plt.subplots(figsize=(7, 3), dpi=100)
        #--------------------------------
        #--------------------------------
        #----create the dataframes
        last_date = max(graph_['date'])
        prediction_data = {'date': [last_date + timedelta(days=1)], 'adj_close': [prediction]}
        prediction_df = pd.DataFrame(data=prediction_data)
        real['date'] = last_date + timedelta(days=1)
        real['legend']='Real'
        prediction_df['legend']='Predicted'
        graph_['legend']='DataSeries'
        
         #--------------------------------
        #--------------------------------
        #----create the graphs
        chart_line = alt.Chart(graph_).mark_line(point=True).encode(
            x='date',
            y='adj_close',
            color=alt.Color('legend', legend=alt.Legend(title="Legend"))
            ,tooltip='adj_close'  
        )

        chart_real = alt.Chart(real).mark_point(filled=True, size=100.0).encode(
            x='date',
            y='adj_close',
            color=alt.Color('legend', legend=alt.Legend(title="Legend")),
        
            tooltip='adj_close'
        ).properties(title="Prediction")
        
        chart_forecast = alt.Chart(prediction_df).mark_point(filled=True, size=100.0).encode(
            x='date',
            y='adj_close',
            tooltip='adj_close',
            color=alt.Color('legend', legend=alt.Legend(title="Legend"))
        )
        charts = chart_forecast + chart_line + chart_real
        charts = alt.layer(chart_line, chart_real, chart_forecast)
        st.altair_chart(charts, use_container_width=True)
        

        with st.beta_expander("See explanation"):
            st.write("""This site uses trained models to predict the next day. Each stock has a different model and a different error""")


else:

    #PAGE TITLE
    st.markdown("""# AI Trader""")
    st.markdown("""## Please choose a date interval and amount of dollars to invest""")
    st.markdown("""## Check out return of our AI Trader""")
    st.markdown("""### compare how the AI Trader compares to buy and hold stocks""")

    # USER CHOOSES DATES

    col1, col2 = st.beta_columns(2)
    with col1:
        s = st.date_input(
            "Pick start date",
            datetime.date(2015, 4, 15))
    with col2:
        e = st.date_input(
            "Pick end date",
            datetime.date(2015, 12, 30))

    # USER CHOOSES AMOUNT OF DOLLARS
    amount_invest = st.slider('Select how much to invest', 0, 100_000, 10_000, 10_000, key="choose amount to invest")

    if st.button('predict'):
        # print is visible in server output, not in the page
        hold_result, ai_result, hold, ai, df_ = ai_trade(str(s), str(e),amount_invest)
        frame = { 'index': df_['date'][:-1], 'hold': hold, 'ai': ai }
        graph_ = pd.DataFrame(frame)
        graph_.set_index('index', inplace=True)

        # GRAPH THE PREDICTION AND PREVIOUS VALUES

        fig, ax = plt.subplots(figsize=(7, 3), dpi=100)

        #plt.figure(figsize=(10,3), dpi=100)

        ax.plot(graph_.index, hold, label="buy and hold")
        ax.plot(graph_.index, ai, label="AI Trader")
        ax.legend()
        #plt.show()
        st.pyplot(fig)

        st.write(f'Buy and Hold strategy would have returned {int(hold_result)} USD or {int((hold_result-amount_invest)/amount_invest * 100)}%')
        st.write(f'AI Trader would have returned {int(ai_result)} USD or {int((ai_result-amount_invest)/amount_invest * 100)}%')
        
         #--------------------------------
        #--------------------------------
        #----create the df
        
        prediction_data = e
        prediction_df = pd.DataFrame(data=prediction_data)
        #ai
        real['date'] = last_date + timedelta(days=1)
        real['legend']='Real'
        prediction_df['legend']='Predicted'
        graph_['legend']='DataSeries'
        
         #--------------------------------
        #--------------------------------
        #----create the graphs
        chart_line = alt.Chart(graph_).mark_line(point=True).encode(
            x='date',
            y='adj_close',
            color=alt.Color('legend', legend=alt.Legend(title="Legend"))
            ,tooltip='adj_close'  
        )

        chart_real = alt.Chart(real).mark_point(filled=True, size=100.0).encode(
            x='date',
            y='adj_close',
            color=alt.Color('legend', legend=alt.Legend(title="Legend")),
        
            tooltip='adj_close'
        ).properties(title="Prediction")
        
        chart_forecast = alt.Chart(prediction_df).mark_point(filled=True, size=100.0).encode(
            x='date',
            y='adj_close',
            tooltip='adj_close',
            color=alt.Color('legend', legend=alt.Legend(title="Legend"))
        )
        charts = chart_forecast + chart_line + chart_real
        charts = alt.layer(chart_line, chart_real, chart_forecast)
        st.altair_chart(charts, use_container_width=True)
        with st.beta_expander("See explanation"):
            st.write("""AI Trader checks the next day prediction for each stock every day, if the stock is predicted to go higher, it 
            buys the stock and if it is predicted to go lower, it sells the stock""")