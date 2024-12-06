import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_location_key(city: str) -> str:
    url = "http://dataservice.accuweather.com/locations/v1/cities/search"
    params = {
        "apikey": API_KEY,
        "q": city,
        "language": "en-us",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    if response.status_code == 503:
        print("For today the amount of API requests was exceeded")
    data = response.json()
    try:
        return data[0]['Key']
    except:
        raise ValueError("Location key whas not found")

def get_5day_forecast(location_key: str):
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}"
    params = {
        "apikey": API_KEY,
        "metric": "true"
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 503:
        print("For today the amount of API requests was exceeded")
    response.raise_for_status()

    return response.json()["DailyForecasts"]

def get_current_weather(location_key: str):    
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}&details=true"
    response = requests.get(url)
    print(response)
    if response.status_code == 503:
        print("For today the amount of API requests was exceeded")
    response.raise_for_status()
    with open("weath.json", "w") as f:
        json.dump(response.json(), f, indent = 4)
    return response.json()
