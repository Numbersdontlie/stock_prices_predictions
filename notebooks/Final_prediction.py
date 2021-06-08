import os
import pandas as pd
import numpy as np
from stock_prices_predictions.get_data import *
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras import layers
from sklearn.preprocessing import RobustScaler
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.losses import mean_absolute_percentage_error
import joblib
from tensorflow.keras.models import load_model

#List of stocks that i will be working with
list_of_stocks = ['T', 'INTC', 'ADBE', 'JPM', 'PG', 'NVDA', 'AAPL', 'AMZN', 'UNH', 'MA']

#Scaler and model for each stock
dict_of_scaler = {}
dict_of_model = {}

for stock in list_of_stocks:
    dict_of_scaler[stock] = joblib.load(f'{stock}_scaler.joblib')
    dict_of_model[stock] = load_model(f'{stock}_model.h5')

#Loading the DataFrame
df = get_portfolio_data()

#User Input
prediction_date = "2015-04-15"
ticker_user = "T"

#Getting the data to predict 
def data_predict(ticker_user, prediction_date):
    df_ticker = df[df["ticker"] == ticker_user]
    df_ticker.reset_index(inplace=True)
    ind = df_ticker.index[df_ticker["date"] == prediction_date].tolist()
    df_ticker = df_ticker[ind[0]-19:ind[0]+1]
    df_ticker = df_ticker.adj_close
    return df_ticker

#Making scaling and predictions 
def make_prediction(ticker_user, prediction_date):
    df_ticker = pd.DataFrame(data_predict(ticker_user, prediction_date)[:-1])
    X_test_T = dict_of_scaler[ticker_user].transform(df_ticker)
    prediction = dict_of_model[ticker_user].predict(X_test_T[np.newaxis,:,:])
    prediction_back = dict_of_scaler[ticker_user].inverse_transform(prediction.reshape(-1, 1))
    return prediction_back

