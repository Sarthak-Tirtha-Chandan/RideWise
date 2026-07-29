import requests
from datetime import datetime , date

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def get_coordinates(city: str):
    """
    Returns latitude and longitude for a city.
    """

    response = requests.get(
        GEOCODING_URL,
        params={
            "name": city,
            "count": 1
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        raise ValueError(f"City '{city}' not found.")

    result = data["results"][0]

    return {
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "name": result["name"],
        "country": result.get("country", "")
    }


def get_current_weather(latitude: float, longitude: float):
    """
    Returns the current weather for a location.
    """

    response = requests.get(
        WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    current = data["current"]

    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "windspeed": current["wind_speed_10m"],
        "condition": weather_code_to_description(current["weather_code"]),
        "weathersit": weather_code_to_weathersit(current['weather_code']),
        "weather_code": current["weather_code"]
}


def weather_code_to_weathersit(code: int):
    """
    Convert Open-Meteo WMO weather codes
    to Bike Sharing Dataset weather situations.
    """

    # Clear
    if code in [0, 1]:
        return 1

    # Cloudy / Fog
    elif code in [2, 3, 45, 48]:
        return 2

    # Light rain / drizzle / snow
    elif code in [
        51, 53, 55,
        56, 57,
        61, 66,
        71, 73,
        77,
        80
    ]:
        return 3

    # Heavy rain / thunderstorm
    else:
        return 4

def weather_code_to_description(code):

    mapping = {
        0: "Clear",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Cloudy",
        45: "Fog",
        48: "Fog",
        51: "Light Drizzle",
        53: "Drizzle",
        55: "Heavy Drizzle",
        61: "Light Rain",
        63: "Rain",
        65: "Heavy Rain",
        71: "Light Snow",
        73: "Snow",
        75: "Heavy Snow",
        80: "Rain Showers",
        81: "Rain Showers",
        82: "Heavy Showers",
        95: "Thunderstorm"
    }

    return mapping.get(code, "Unknown")


def get_future_weather(latitude:float,longitude:float,date:date,hour:int):

    response = requests.get(
        WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "date" : date,
            "hour" : hour,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        },
        timeout=10
    )
    response.raise_for_status()

    data = response.json()

    current = data["current"]

    return {
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "windspeed": current["wind_speed_10m"],
            "condition": weather_code_to_description(current["weather_code"]),
            "weathersit": weather_code_to_weathersit(current['weather_code']),
            "weather_code": current["weather_code"]
}
