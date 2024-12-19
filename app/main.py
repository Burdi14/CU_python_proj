import os
from flask import Flask, request, render_template
from datetime import datetime
from dotenv import load_dotenv
from app.core import get_5day_forecast, get_location_key
import json
from flask import Blueprint

bp = Blueprint("main", __name__, static_folder='static', template_folder='templates')

#setting minimumand maximum of the acceptable values
load_dotenv()
MAX_ACCEPTABLE_TEMP = float(os.getenv("MAX_ACCEPTABLE_TEMP", "26"))
MIN_ACCEPTABLE_TEMP = float(os.getenv("MIN_ACCEPTABLE_TEMP", "-10"))

@bp.route("/index.html", methods= ["GET", "POST"])
@bp.route("/", methods= ["GET", "POST"])
def index():
    if request.method == "POST":

        try:
            waypoints = request.form.getlist('waypoints[]')
            forecasts = {}
            for city in waypoints:
                # Сделайте API-запрос для получения прогноза погоды (например, к AccuWeather)
                city_key, city_localize = get_location_key(city)
                city_forecast = get_5day_forecast(city_key)
                forecasts.update( {city_localize:city_forecast})
                # city_forecast = json.load(open(f"tests/forecast.json", "r"))
                # forecasts[city] = city_forecast["DailyForecasts"]
                #make city localize dont forget
            #formatting the date
            for day in range(5):
                for city in forecasts:
                    tmp = forecasts[city][day]["Date"]
                    date_obj = datetime.fromisoformat(tmp)
                    formatted_date = date_obj.strftime("%m.%d")
                    forecasts[city][day]["Date"] = formatted_date
            return render_template(
                "index.html",
                forecasts=forecasts,
                min_temp=MIN_ACCEPTABLE_TEMP,
                max_temp=MAX_ACCEPTABLE_TEMP
            )
        except Exception as e:
            return render_template("index.html", error = str(e))
    else:
        return render_template("index.html")
