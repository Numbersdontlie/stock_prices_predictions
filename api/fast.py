from fastapi import FastAPI
from datetime import datetime
import joblib
from tensorflow.keras.models import load_model
from stock_prices_predictions.get_data import get_portfolio_data
from stock_prices_predictions.one_day_prediction import make_prediction
from stock_prices_predictions.ai_portfolio import *

app = FastAPI()

#getting the main response of the API 
@app.get("/")
def index():
    return {"prediction": "The price of the share for the selected day is ..."}

#getting the parameters for the prediction (model prediction)
@app.get("/predict")
def predict(stock_to_predict,       # T, NVDA, AAPL #check if ts the same in the program
            date_to_predict):        # 2013-07-06 17:18:00 #check if ts the same in the program 
            
            
    # create datetime object from user provided date
    # date_to_predict = datetime.strptime(date_to_predict, "%Y-%m-%d")
    
      
    
    #calling the scaler and the model of the stock
    #scaler_predict = joblib.load(f"models_scalers/{stock_to_predict}_scaler.joblib") 
    #model_predict = load_model(f"models_scalers/{stock_to_predict}_model.h5") 
    
       
    #making the scaling and predictions
    data_stock, date_series, real_value, prediction_back = make_prediction(stock_to_predict, date_to_predict) 
    #print("Searching the error")
    #formating the output 
    result_dict = {"stock_to_predict": stock_to_predict,"data_stock": [data_stock], "date_series": date_series, "real_value": real_value, "prediction_back": float(prediction_back[0])}
    return result_dict
    
    #take care: return (serie of 19 values, 1 predicted value and 1 real value) transform again in Streamlit 
    
    

#getting the parameters for the trader (IA Trader)
@app.get("/trader") #not sure about the trader need to check
def predict_trader(initial_date,        # 2013-07-06 17:18:00
           final_date,        # 2013-07-06 17:18:00
           amount_to_invest):       # 1000, 5000, 10_000

    # give a format to my inputs from user
    initial_date = datetime.strptime(initial_date, "%Y-%m-%d")
    final_date = datetime.strptime(final_date, "%Y-%m-%d")
    amount_to_invest = float(amount_to_invest)

    #calling the scaler and the model of the stock
    #scaler_predict = joblib.load(f"models_scalers/{stock_to_predict}_scaler.joblib") 
    #model_predict = load_model(f"models_scalers/{stock_to_predict}_model.h5") 

    #calling the function 
    buyandhold, final_amount, buyandholdgraph, aitradergraph = ai_trade(initial_date, final_date, amount_to_invest)
    result_dict_trade = {"buyandhold": buyandhold, "final_amount": final_amount, "buyandholdgraph": buyandholdgraph, "aitradergraph": aitradergraph}
    return result_dict_trade        
            

