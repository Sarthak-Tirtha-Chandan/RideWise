from fastapi import FastAPI
from schema import ShortPredictionRequest , FuturePredictionRequest
from predictor import predict_short , predict_future

app = FastAPI(title='Ridewise API')


@app.get("/")
def home():
  return {"Successfully running !!"}


@app.post("/predict-short")
def predict_route(req:ShortPredictionRequest):
  return predict_short(req)

@app.post("/predict-future")
def predict_route(req:FuturePredictionRequest):
  return predict_future(req)