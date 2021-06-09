import streamlit as st
from stock_prices_predictions.one_day_prediction import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
#import mplcursors
import altair as alt
from datetime import timedelta  


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
        #graph_.set_index('date', inplace=True)
        st.write(graph_.head())
        
        

        # GRAPH THE PREDICTION AND PREVIOUS VALUES

        fig, ax = plt.subplots(figsize=(7, 3), dpi=100)

        # #plt.figure(figsize=(10,3), dpi=100)
        # ax.plot(graph_.index, graph_['adj_close'], label="previous days")
        # ax.plot(graph_.index[-1], real, 'bo', label="real")  # plot x and y using blue circle markers
        # ax.plot(graph_.index[-1], prediction, 'ro', label="prediction")  # plot x and y using blue circle markers
        # ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left',)
        # ax.set_xticklabels(ax.get_xticks(), rotation = 45, color='white')
        # ax.set_yticklabels(ax.get_yticks(), color='white')
        # ax.tick_params(axis='x', colors='white')
        # ax.tick_params(axis='y', colors='white')
        # ax.spines['bottom'].set_color('white')
        # ax.spines['top'].set_color('#0E1117') 
        # ax.spines['right'].set_color('#0E1117')
        # ax.spines['left'].set_color('white')
        # ax.patch.set_facecolor('#0E1117')
        # fig.patch.set_facecolor('#0E1117')
        # ax.set_title("Blablabla")
        # ax.title.set_color('white')
        # mplcursors.cursor(hover=True)
        # #plt.show()
        # st.pyplot(fig)
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
        



else:
    st.title('AI Trader')
        






