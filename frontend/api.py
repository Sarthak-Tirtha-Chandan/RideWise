import requests

BASE_URL = "http://127.0.0.1:8000"


def predict_short(city):
    try:
        response = requests.post(
            f"{BASE_URL}/predict-short",
            json={"city": city},
            timeout=15
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }

def predict_future(city, date, hour):
    try:
        response = requests.post(
            f"{BASE_URL}/predict-future",
            json={
                "city": city,
                "date": str(date),   # Converts datetime.date to "YYYY-MM-DD"
                "hour": hour
            },
            timeout=15
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }