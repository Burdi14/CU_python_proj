import os
from datetime import datetime
from dotenv import load_dotenv
import json
import dash
from dash import dcc, html, Input, Output, State

# Load environment variables
load_dotenv()
MAX_ACCEPTABLE_TEMP = float(os.getenv("MAX_ACCEPTABLE_TEMP", "26"))
MIN_ACCEPTABLE_TEMP = float(os.getenv("MIN_ACCEPTABLE_TEMP", "-10"))

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "5-Day Weather Forecast"

# Define the layout
app.layout = html.Div([
    html.H1("5-Day Weather Forecast", style={"textAlign": "center"}),

    html.Div([
        html.Label("Enter cities (comma-separated):"),
        dcc.Input(id="city-input", type="text", placeholder="e.g., New York, Los Angeles", style={"width": "100%"}),
        html.Button("Get Forecast", id="submit-button", n_clicks=0, style={"marginTop": "10px"}),
    ], style={"width": "50%", "margin": "auto"}),

    html.Div(id="forecast-output", style={"marginTop": "20px"})
])

# Helper function to process forecasts
def format_forecast(city, forecast_data):
    formatted_forecast = []
    for day in forecast_data["DailyForecasts"]:
        tmp_date = day["Date"]
        date_obj = datetime.fromisoformat(tmp_date)
        formatted_date = date_obj.strftime("%m.%d")
        formatted_forecast.append({
            "date": formatted_date,
            "min_temp": day["Temperature"]["Minimum"]["Value"],
            "max_temp": day["Temperature"]["Maximum"]["Value"]
        })
    return city, formatted_forecast

# Define callback
@app.callback(
    Output("forecast-output", "children"),
    Input("submit-button", "n_clicks"),
    State("city-input", "value")
)
def update_forecast(n_clicks, city_input):
    if n_clicks > 0 and city_input:
        try:
            cities = [city.strip() for city in city_input.split(",")]
            forecasts = {}

            for city in cities:
                # Here you would use an API call like `get_location_key` and `get_5day_forecast`
                # For this example, we load mock data from a JSON file
                with open("tests/forecast.json", "r") as f:
                    city_forecast = json.load(f)
                city_name, formatted_forecast = format_forecast(city, city_forecast)
                forecasts[city_name] = formatted_forecast

            # Render the forecasts
            forecast_elements = []
            for city, forecast in forecasts.items():
                city_header = html.H3(f"Forecast for {city}", style={"marginTop": "20px"})
                forecast_table = html.Table([
                    html.Thead(html.Tr([html.Th("Date"), html.Th("Min Temp"), html.Th("Max Temp")])),
                    html.Tbody([
                        html.Tr([
                            html.Td(day["date"]),
                            html.Td(day["min_temp"]),
                            html.Td(day["max_temp"])
                        ]) for day in forecast
                    ])
                ])
                forecast_elements.extend([city_header, forecast_table])

            return html.Div(forecast_elements)
        except Exception as e:
            return html.Div(f"Error: {str(e)}", style={"color": "red"})

    return html.Div("Enter city names and click 'Get Forecast' to see the weather.")

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
