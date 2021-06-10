import os
import pandas as pd
import numpy as np


def get_lstm_training_data(stock, prediction_timeframe):
    '''returns X and y for the training of the LSTM'''
    #cwd = os.getcwd()
    cwd = os.path.abspath(os.path.join(os.path.abspath(__file__),"../.."))
    simp_path4 = 'raw_data/df.csv'
    #abs_path4 = os.path.abspath(os.path.join(cwd,'..',simp_path4))
    abs_path4 = os.path.abspath(os.path.join(cwd,simp_path4))
    df_500 = pd.read_csv(abs_path4)
    df_500.date = pd.to_datetime(df_500.date)
    df_500['year'] = pd.DatetimeIndex(df_500['date']).year
    df_500['month'] = pd.DatetimeIndex(df_500['date']).month
    df_500['day'] = pd.DatetimeIndex(df_500['date']).day
    df_500 = df_500[df_500.year>1999]
    df_500 = df_500[df_500.year<2015]
    list_of_10_stocks = ['T', 'INTC', 'ADBE', 'JPM', 'PG', 'NVDA', 'AAPL', 'AMZN', 'UNH', 'MA']
    df_top10_14y = df_500[df_500['ticker'].isin(list_of_10_stocks)]

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
    df_500.date = pd.to_datetime(df_500.date)
    df_500['year'] = pd.DatetimeIndex(df_500['date']).year
    df_500['month'] = pd.DatetimeIndex(df_500['date']).month
    df_500['day'] = pd.DatetimeIndex(df_500['date']).day
    df_500 = df_500[df_500.year>2014]
    list_of_10_stocks = ['T', 'INTC', 'ADBE', 'JPM', 'PG', 'NVDA', 'AAPL', 'AMZN', 'UNH', 'MA']
    df_top10_3y = df_500[df_500['ticker'].isin(list_of_10_stocks)]

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

def get_lstm_data(stock):
    '''returns X and y for the training of the LSTM'''
    cwd = os.getcwd()
    simp_path4 = 'raw_data/df.csv'
    abs_path4 = os.path.abspath(os.path.join(cwd,'..',simp_path4))
    df_ = pd.read_csv(abs_path4)
 
    df_ = df_[df_['ticker'] == stock]

    df_.date = pd.to_datetime(df_.date)
    df_['year'] = pd.DatetimeIndex(df_['date']).year
    df_['month'] = pd.DatetimeIndex(df_['date']).month
    df_['day'] = pd.DatetimeIndex(df_['date']).day
    df_ = df_[df_.year>1999]
    
    X_train = df_[df_.year<2015]
    X_test = df_[df_.year>2014]
    #X_test = X_test[X_test.year<2016]
    X_train = X_train.iloc[:,3:4]
    X_test = X_test.iloc[:, 3:4]

    return X_train, X_test

def create_sequences(dataf, datanotscaled, prediction_timeframe):
    sequence_a = []
    y = []
    for i in range(0, len(dataf)-100, 19):
        day = []
        df_ = dataf.iloc[i:i+36+prediction_timeframe,:]

        for p in range(19):
            day.append(df_.iloc[p,:])
        sequence_a.append(day)

        df_2 = datanotscaled.iloc[i:i+19+prediction_timeframe,:]
        y.append(np.array(df_2.iloc[18+prediction_timeframe,0]-df_2.iloc[17+prediction_timeframe,0]))

    X = np.array(sequence_a).astype(np.float32)

    return (np.array(X), np.array(y))

def create_sequences_scaled(dataf, prediction_timeframe=1, sequence_lenght=19):
    sequence_a = []

    for i in range(0, len(dataf)-sequence_lenght):

        sequence_a.append(dataf.iloc[i:i+sequence_lenght,:]) 

    return np.array(sequence_a)

def create_sequences_scaled_plus(dataf, data2, prediction_timeframe=1, sequence_lenght=19):
    sequence_a = []
    y = []
    z =[]

    for i in range(0, len(dataf)-100, 4):
        day = []
        df_ = dataf.iloc[i:i+sequence_lenght+prediction_timeframe,:]
        sequence_a.append(df_.iloc[:-prediction_timeframe,:])
        y.append(df_.iloc[-1,0])
        
        df_2 = data2.iloc[i:i+sequence_lenght+prediction_timeframe,:]
        z.append(np.array(df_2.iloc[-2,0]))

    X = np.array(sequence_a).astype(np.float32)
    #X = sequence_a
    return (np.array(X), np.array(y), np.array(z))
    #return (X, y, z)#

def get_portfolio_data():
    print("enter get portfolio data")
    '''returns X and y for the training of the LSTM'''
    #cwd = os.getcwd()
    #cwd = os.path.abspath(os.path.join(os.path.abspath(__file__),"../.."))
    if os.environ['DATA_DIRECTORY']:
        cwd = os.environ['DATA_DIRECTORY']
    else:
        cwd = os.path.abspath(os.path.join(os.path.abspath(__file__),"../.."))
    simp_path4 = 'raw_data/df.csv'
    #abs_path4 = os.path.abspath(os.path.join(cwd,'..',simp_path4))
    abs_path4 = os.path.abspath(os.path.join(cwd,simp_path4))
    df_500 = pd.read_csv(abs_path4)
    df_500.date = pd.to_datetime(df_500.date)
    df_500['year'] = pd.DatetimeIndex(df_500['date']).year
    df_500['month'] = pd.DatetimeIndex(df_500['date']).month
    df_500['day'] = pd.DatetimeIndex(df_500['date']).day
    df_500 = df_500[df_500.year>2013]
    #df_500 = df_500[df_500.year<year+1]
    list_of_10_stocks = ['T', 'INTC', 'ADBE', 'JPM', 'PG', 'NVDA', 'AAPL', 'AMZN', 'UNH', 'MA']
    df_ = df_500[df_500['ticker'].isin(list_of_10_stocks)]

    return df_