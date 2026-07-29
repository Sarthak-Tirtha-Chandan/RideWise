import numpy as np


def create_feature_vector(history_df, weather):

    # Copy the latest engineered row
    features = history_df.iloc[-1].copy()

    # Next prediction timestamp
    features["hr"] = (features["hr"] + 1) % 24

    # Calendar Features
    features["yr"] = history_df.iloc[-1]["yr"]
    features["mnth"] = history_df.iloc[-1]["mnth"]
    features["weekday"] = (history_df.iloc[-1]["weekday"] + (1 if features["hr"] == 0 else 0)) % 7

    # Weather
    features["temp"] = weather["temperature"]
    features["hum"] = weather["humidity"]
    features["windspeed"] = weather["windspeed"]
    features["weathersit"] = weather["weathersit"]

    # Cyclical Features
    features["hr_sin"] = np.sin(2 * np.pi * features["hr"] / 24)
    features["hr_cos"] = np.cos(2 * np.pi * features["hr"] / 24)

    features["week_sin"] = np.sin(2 * np.pi * features["weekday"] / 7)
    features["week_cos"] = np.cos(2 * np.pi * features["weekday"] / 7)

    features["mnth_sin"] = np.sin(2 * np.pi * features["mnth"] / 12)
    features["mnth_cos"] = np.cos(2 * np.pi * features["mnth"] / 12)

    # Peak Hour
    features["is_peak_hour"] = int(
        features["hr"] in [7, 8, 9, 17, 18, 19]
    )

    # Interaction Features
    features["weather_hr"] = (
        features["weathersit"] * features["hr"]
    )

    features["temp_hr"] = (
        features["temp"] * features["hr"]
    )

    features["temp_hum"] = (
        features["temp"] * features["hum"]
    )

    return features

import numpy as np
from datetime import datetime

def create_future_feature_vector(weather, date, hour):
    """
    Create feature vector for future prediction.
    """

    dt = datetime.combine(date, datetime.min.time()).replace(hour=hour)

    month = dt.month
    weekday = dt.weekday()      
    year = dt.year
    season = ((month % 12) // 3) + 1

    yr = year - 2011

    holiday = 0    
    workingday = 0 if (weekday >= 5 or holiday == 1) else 1

    features = {
        # Calendar Features
        "season": season,
        "yr": yr,
        "mnth": month,
        "hr": hour,
        "holiday": holiday,
        "weekday": weekday,
        "workingday": workingday,

        # Weather Features
        "temp": weather["temperature"],
        "hum": weather["humidity"],
        "windspeed": weather["windspeed"],
        "weathersit": weather["weathersit"],
        "atemp" : weather["temperature"]
    }

    # Cyclical Features
    features["hr_sin"] = np.sin(2 * np.pi * hour / 24)
    features["hr_cos"] = np.cos(2 * np.pi * hour / 24)

    features["week_sin"] = np.sin(2 * np.pi * weekday / 7)
    features["week_cos"] = np.cos(2 * np.pi * weekday / 7)

    features["mnth_sin"] = np.sin(2 * np.pi * month / 12)
    features["mnth_cos"] = np.cos(2 * np.pi * month / 12)

    # Peak Hour
    features["is_peak_hour"] = int(hour in [7, 8, 9, 17, 18, 19])

    # Interaction Features
    features["weather_hr"] = features["weathersit"] * hour
    features["temp_hr"] = features["temp"] * hour
    features["temp_hum"] = features["temp"] * features["hum"]

    return features