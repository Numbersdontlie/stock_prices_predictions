import os
import pandas as pd
import numpy as np


def get_lstm_training_data(stock, prediction_timeframe):
    '''returns X and y for the training of the LSTM'''
    cwd = os.getcwd()
    simp_path4 = 'raw_data/df.csv'
    abs_path4 = os.path.abspath(os.path.join(cwd,'..',simp_path4))
    df_500 = pd.read_csv(abs_path4)
    list_of_10_stocks = ['T', 'INTC', 'ADBE', 'JPM', 'PG', 'NVDA', 'AAPL', 'AMZN', 'UNH', 'MA']
    df_top500 = df_500[df_500['ticker'].isin(list_of_10_stocks)]
    df_500.date = pd.to_datetime(df_500.date)
    df_500['year'] = pd.DatetimeIndex(df_500['date']).year
    df_500['month'] = pd.DatetimeIndex(df_500['date']).month
    df_500['day'] = pd.DatetimeIndex(df_500['date']).day
    df_500 = df_500[df_500.year>1999]
    df_top10_14y = df_500[df_500.year<2015]

    sequence_a = []
    y = []
    for i in range(0, 3600, 36):
        day = []
        df_ = df_top10_14y[df_top10_14y['ticker'] == stock]
        df_ = df_.iloc[i:i+36+prediction_timeframe,3:7]
        for p in range(36):
            day.append(df_.iloc[p,:]) 
        sequence_a.append(day)
        X = np.array(sequence_a).astype(np.float32)
        y.append(np.array(df_.iloc[35+prediction_timeframe,0]))

    return (X, np.array(y))

def get_lstm_test_data(stock, prediction_timeframe):
    '''returns X and y for the training of the LSTM'''
    cwd = os.getcwd()
    simp_path4 = 'raw_data/df.csv'
    abs_path4 = os.path.abspath(os.path.join(cwd,'..',simp_path4))
    df_500 = pd.read_csv(abs_path4)
    list_of_10_stocks = ['T', 'INTC', 'ADBE', 'JPM', 'PG', 'NVDA', 'AAPL', 'AMZN', 'UNH', 'MA']
    df_top500 = df_500[df_500['ticker'].isin(list_of_10_stocks)]
    df_500.date = pd.to_datetime(df_500.date)
    df_500['year'] = pd.DatetimeIndex(df_500['date']).year
    df_500['month'] = pd.DatetimeIndex(df_500['date']).month
    df_500['day'] = pd.DatetimeIndex(df_500['date']).day
    df_top10_3y = df_500[df_500.year>2014]

    sequence_a = []
    y = []
    for i in range(0, 800, 36):
        day = []
        df_ = df_top10_3y[df_top10_3y['ticker'] == stock]
        df_ = df_.iloc[i:i+36+prediction_timeframe,3:7]
        for p in range(36):
            day.append(df_.iloc[p,:]) 
        sequence_a.append(day)
        X = np.array(sequence_a).astype(np.float32)
        y.append(np.array(df_.iloc[35+prediction_timeframe,0]))

    return (X, np.array(y))