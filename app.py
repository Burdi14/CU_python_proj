import os
from flask import Flask, request, render_template
from core import get_5day_forecast, get_location_key
from datetime import datetime
from dotenv import load_dotenv

app = Flask(__name__, static_folder='static')

#setting minimumand maximum of the acceptable values
load_dotenv()
MAX_ACCEPTABLE_TEMP = float(os.getenv("MAX_ACCEPTABLE_TEMP", "26"))
MIN_ACCEPTABLE_TEMP = float(os.getenv("MIN_ACCEPTABLE_TEMP", "-10"))
print(MAX_ACCEPTABLE_TEMP , MIN_ACCEPTABLE_TEMP )
@app.route("/", methods= ["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            start_city = request.form["start_city"]
            dest_city = request.form["end_city"]
            #getting location key and normalized nomes of the cities
            start_key, start_localized = get_location_key(start_city)
            dest_key, dest_localized = get_location_key(dest_city)
            start_forecast = get_5day_forecast(start_key)
            dest_forecast = get_5day_forecast(dest_key)

            #formatting the date
            for day in range(5):
                tmp = start_forecast[day]["Date"]

                date_obj = datetime.fromisoformat(tmp)
                formatted_date = date_obj.strftime("%m.%d")

                start_forecast[day]["Date"] = formatted_date
                tmp = dest_forecast[day]["Date"]
                
                date_obj = datetime.fromisoformat(tmp)
                formatted_date = date_obj.strftime("%m.%d")

                dest_forecast[day]["Date"] = formatted_date

            return render_template(
                "index.html",
                start_city=start_localized,
                dest_city=dest_localized,
                start_forecast=start_forecast,
                dest_forecast=dest_forecast,
                min_temp=MIN_ACCEPTABLE_TEMP,
                max_temp=MAX_ACCEPTABLE_TEMP
            )
        except Exception as e:
            return render_template("index.html", error=str(e))
    return render_template("index.html")

if __name__ == "__main__":
    app.run()