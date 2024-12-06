import os
from flask import Flask, request, render_template
from core import get_5day_forecast, get_location_key
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods= ["GET", "POST"])
def index():
    # if request.method == "GET":
    #     return render_template("index.html")

    if request.method == "POST":
        try:
            start_city = request.form["start_city"]
            dest_city = request.form["end_city"]

            start_key = get_location_key(start_city)
            dest_key = get_location_key(dest_city)
            start_forecast = get_5day_forecast(start_key)
            dest_forecast = get_5day_forecast(dest_key)

            for day in range(5):
                tmp = start_forecast[day]["Date"]

                date_obj = datetime.fromisoformat(tmp)
                formatted_date = date_obj.strftime("%m.%d")

                start_forecast[day]["Date"] = formatted_date
                tmp = dest_forecast[day]["Date"]

                date_obj = datetime.fromisoformat(tmp)
                formatted_date = date_obj.strftime("%m.%d")

                start_forecast[day]["Date"] = formatted_date

            return render_template(
                "index.html",
                start_city=start_city,
                end_city=dest_city,
                start_forecast=start_forecast,
                end_forecast=dest_forecast
            )
        except Exception as e:
            return render_template("index.html", error=str(e))
    return render_template("index.html")

if __name__ == "__main__":
    app.run()