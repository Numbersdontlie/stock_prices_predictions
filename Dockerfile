FROM python:3.8.6-buster

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN mkdir stock_project
RUN mv requirements.txt /stock_project/
COPY api /stock_project/api 
COPY stock_prices_predictions /stock_project/stock_prices_predictions
COPY models_scalers /stock_project/models_scalers
COPY raw_data/df.csv /stock_project/raw_data/df.csv
COPY setup.py /stock_project/setup.py
COPY app.py /stock_project/app.py 
WORKDIR stock_project



RUN pip install . 


#EXPOSE 8501
#CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
CMD streamlit run stock_prices_predictions/web_site.py --server.port $PORT

###To run my docker need to do this 

#to build a new image: docker build . -t api
#to list the images: docker images
#run the container: docker run -e PORT=8000 -p 8080:8000 api
#connect to our API: http://locahost:8080/


##Storage image on Container Registry parameters
#GCP_PROJECT_ID = "stock-price-prediction-606"
#DOCKER_IMAGE_NAME = "my-api-stock-in-kebab-case"
#GCR_MULTI_REGION = eu.gcr.io
#GCR_REGION = "europe-west1"

#build the image for container registry
#docker build -t $GCR_MULTI_REGION/$GCP_PROJECT_ID/$#DOCKER_IMAGE_NAME
#docker run -e PORT=8000 -p 8080:8000 $GCR_MULTI_REGION/$GCP_PROJECT_ID/$DOCKER_IMAGE_NAME not sure about this 

#push our image to Container Registry
#docker push $GCR_MULTI_REGION/$GCP_PROJECT_ID/$DOCKER_IMAGE_NAME


##Deploy the image to Cloud Run
#gcloud run deploy --image $GCR_MULTI_REGION/$GCP_PROJECT_ID/$DOCKER_IMAGE_NAME --platform managed --region $GCR_REGION
