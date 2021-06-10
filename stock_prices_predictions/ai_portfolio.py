#IMPORT LIBRARIES
import os
import pandas as pd
import numpy as np
from stock_prices_predictions.get_data import *
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras import layers
from sklearn.preprocessing import RobustScaler
#import matplotlib.pyplot as plt
#import seaborn as sns
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.losses import mean_absolute_percentage_error
import joblib
from tensorflow.keras.models import load_model

list_of_10_stocks = ['T', 'INTC', 'ADBE', 'JPM', 'PG', 'NVDA', 'AAPL', 'AMZN', 'UNH', 'MA']

# LOAD MODELS AND SCALERS

#cwd = os.getcwd()
if "DATA_DIRECTORY" in os.environ:
    cwd = os.environ['DATA_DIRECTORY']
else:
    cwd = os.path.abspath(os.path.join(os.path.abspath(__file__),"../.."))

dict_of_scaler = {}
dict_of_model = {}

for stock in list_of_10_stocks:
    dict_of_scaler[stock] = joblib.load(os.path.abspath(os.path.join(cwd,f'models_scalers/{stock}_scaler.joblib')))
    dict_of_model[stock] = load_model(os.path.abspath(os.path.join(cwd,f'models_scalers/{stock}_model.h5')))

# LOAD DATAFRAME

#df = get_portfolio_data()

# CREATE CLASS

class Stock:
    def __init__(self, name, initial_price, final_price, dollars):
        self.name = name
        self.initial_price = initial_price
        self.final_price = final_price
        
        self.current_price = initial_price

        self.amount_owned = dollars
        self.num_shares = dollars/initial_price
        self.prediction_higher = True
        self.num_shares_hold = dollars/initial_price
        
        self.prediction = 0.0
        self.prices = 0.0
    
    def prices(self,number):
        self.prices = number
         

# USER INPUT
def ai_trade(initial_date, final_date, initial_amount):
    '''insert initial date, final date and initial amount invested'''
    #initial_date = '2016-02-01'
    #final_date = '2016-12-30'
    #initial_amount = 10000
    in_hand = 0

    df = get_portfolio_data()
    # INSTATIATE CLASSES

    list_stocks = {}
    for i in list_of_10_stocks:
        qty = len(list_of_10_stocks)
        price = df[(df["date"]==initial_date) & (df["ticker"]==i)]
        final_price = df[(df["date"]==final_date) & (df["ticker"]==i)]
        list_stocks[i] = Stock(i, price['adj_close'], final_price['adj_close'], initial_amount/qty)

    # CREATE PREDICTIONS

    for s in list_stocks:
        df_T2 = df[df['ticker']== s]
        df_T2.reset_index(inplace=True)
        ind = df_T2.index[df_T2['date'] == initial_date].tolist()
        ind2 = df_T2.index[df_T2['date'] == final_date].tolist()
        df_T2 = df_T2[ind[0]-18:ind2[0]+1]
        df_T2 = df_T2.adj_close
        df_T2 = pd.DataFrame(df_T2)
        
        scaler = dict_of_scaler[s]
        X_test_T = scaler.transform(df_T2)
        
        model = dict_of_model[s]
        X_test_T2 = create_sequences_scaled(pd.DataFrame(X_test_T))
        prediction = model.predict(X_test_T2)

        prediction_back = scaler.inverse_transform(prediction.reshape(-1, 1))
        
        list_stocks[s].prediction = prediction_back
        
        df_T2 = df[df['ticker']== s]
        df_T2.reset_index(inplace=True)
        ind = df_T2.index[df_T2['date'] == initial_date].tolist()
        ind2 = df_T2.index[df_T2['date'] == final_date].tolist()
        df_T2 = df_T2[ind[0]:ind2[0]+1]
        list_stocks[s].prices = df_T2

    # CALCULATE RETURN ON BUY AND HOLD STRATEGY

    buyandhold = 0.0
    for i in list_stocks:
        buyandhold+=float(list_stocks[i].amount_owned / list_stocks[i].initial_price *float(list_stocks[i].final_price))

    df_ = df[df['ticker']== 'T']
    df_.reset_index(inplace=True)
    ind = df_.index[df_['date'] == initial_date].tolist()
    ind2 = df_.index[df_['date'] == final_date].tolist()
    df_ = df_[ind[0]:ind2[0]+1]

    # LOOP THROUGH DAYS PREDICTING 

    buyandholdgraph = []
    aitradergraph = []

    #loops through days
    for i in range(len(df_)-1):

        #for each day it checks the prediction and appends buy list
        buy_list = []
        
        for s in list_stocks:
            if float(list_stocks[s].prediction[i]) >= float(list_stocks[s].current_price):
                buy_list.append(s)

        #sells and puts all the money on wallet
        for s in list_stocks:
            in_hand += float(list_stocks[s].num_shares * list_stocks[s].current_price)
            list_stocks[s].num_shares = 0

        #buys
        if len(buy_list) > 0:
            for l in buy_list:
                amount_to_buy = float(in_hand / len(buy_list))
                list_stocks[l].num_shares =  amount_to_buy / float(list_stocks[l].current_price)

            in_hand = 0
        
        owned=0
        for s in list_stocks:
            owned += float(list_stocks[s].num_shares * list_stocks[s].current_price)  
        
        #create the data for the graphs
        buyandhold_ = 0
        aitrader_= 0
        
        for s in list_stocks:
            buyandhold_ += float(list_stocks[s].num_shares_hold) * float(list_stocks[s].current_price)
            aitrader_ += float(list_stocks[s].num_shares) * float(list_stocks[s].current_price)
        
        aitrader_+=in_hand
        buyandholdgraph.append(buyandhold_)
        aitradergraph.append(aitrader_)
        
        #update current price
        for s in list_stocks:
            list_stocks[s].current_price = list_stocks[s].prices.adj_close.iloc[i]


    final_amount = in_hand
    for s in list_stocks:
        final_amount += float(list_stocks[s].num_shares * list_stocks[s].current_price)

    #print(f"Buy and hold strategy made {buyandhold - initial_amount} ({(buyandhold - initial_amount)/initial_amount * 100}%)")
    #print(f"Our AI trader made {final_amount - initial_amount} ({(final_amount - initial_amount)/initial_amount * 100}%)")

    return (buyandhold, final_amount, buyandholdgraph, aitradergraph, df_)
