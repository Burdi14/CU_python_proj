Route Weather Forecast Telegram Bot
This Telegram bot helps you plan your trip by providing a weather forecast for your route, including waypoints, over a specified period.

Features

Get the weather forecast for multiple locations along your route, including start, destination, and waypoints.
Choose a forecast period of 1 to 4 days.
View detailed weather information for each day, including minimum and maximum temperatures, and day and night weather conditions.
Installation

1. Install Dependencies:

This bot requires the following Python libraries, listed in requirements.txt:

Bash
pip install -r requirements.txt
2. Environment Variables:

Create a .env file in your project directory and add the following variables:

API_KEY_WEATHER=<your_weather_api_key>
TOKEN=<your_telegram_bot_token>
MIN_ACCEPTABLE_TEMP=<minimum acceptable temperature threshold (optional)>
MAX_ACCEPTABLE_TEMP=<maximum acceptable temperature threshold (optional)>
3. Run the Bot:
python run.py

Usage
Open Telegram and search for the bot using its username.
Start a conversation with the bot by typing /start.
The bot will guide you through setting your route and selecting a forecast period.
Once you've configured your preferences, use the /get_forecast command to retrieve the weather information for your route.
The bot will display the weather forecast for each location on your route, allowing you to view details for each day of the selected period.
