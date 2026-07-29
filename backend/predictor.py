import joblib
import pandas as pd

from config import (
    MODEL_PATH,
    MODEL_PATH2,
    FEATURE_PATH,
    FEATURE_PATH2,
    DATA_PATH,
    DATA_PATH2
)

from feature_engineering import create_feature_vector , create_future_feature_vector

from weather import ( get_coordinates , get_current_weather , get_future_weather )
from datetime import datetime, timedelta ,time


model = joblib.load(MODEL_PATH)
model2 = joblib.load(MODEL_PATH2)

feature_names = joblib.load(FEATURE_PATH)
feature_names2 = joblib.load(FEATURE_PATH2)

df = pd.read_csv(DATA_PATH)
df_2 = pd.read_csv(DATA_PATH2)




def predict_short(req):
  coords = get_coordinates(req.city)

  weather = get_current_weather(
    coords['latitude'] , coords['longitude']
  )

  features = create_feature_vector(df , weather)

  last_datetime = pd.to_datetime(df.iloc[-1]["datetime"])

  prediction_datetime = last_datetime + pd.Timedelta(hours=1)

  X = pd.DataFrame(
        [features]
  )

  X = X[feature_names]

  prediction = model.predict(X)[0]

  return {
        "prediction": float(prediction),
        "prediction_datetime": prediction_datetime.isoformat(),
        "weather": weather
    }

def predict_future(req):
    coords = get_coordinates(req.city)

    weather = get_future_weather(
        coords["latitude"],
        coords["longitude"],
        req.date,
        req.hour
    )

    features = create_future_feature_vector(
        weather=weather,
        date=req.date,
        hour=req.hour
    )

    X = pd.DataFrame([features])

    missing = set(feature_names2) - set(X.columns)
    if missing:
        raise ValueError(f"Missing features: {missing}")

    X = X[feature_names2]

    prediction = model2.predict(X)[0]

    prediction_datetime = datetime.combine(
        req.date,
        time(hour=req.hour)
    )

    return {
        "city": coords["name"],
        "prediction": float(prediction),
        "prediction_datetime": prediction_datetime.isoformat(),
        "weather": weather
    }