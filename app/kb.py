from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core import cities

def main_menu_text(cities: cities, period: str) -> str:
    return f"Start point: {cities.start}\nWaypoints: " + " -> ".join(cities.waypoints) + f"\nDestination: {cities.dest}\nPeriod (days): {period}"

def make_input_city_menu(cities: cities) -> InlineKeyboardMarkup:
    text_cities = []
    if cities.start == "":
        text_cities.append("Add start city")
    else:
        text_cities.append(cities.start)
    if cities.dest == "":
        text_cities.append("Add destination")
    else:
        text_cities.append(cities.dest)
    for i in range(len(cities.waypoints)):
        text_cities.append(cities.waypoints[i])
    text_cities.append("Add waypoint")


    inline_keyboard=[
            [
                InlineKeyboardButton(text=text_cities[0], callback_data='set_city_start'),
                InlineKeyboardButton(text=text_cities[1], callback_data='set_city_dest')
            ]
        ]
    waypoints = text_cities[2:-1]
    for i, waypoint in enumerate(text_cities[2:-1], start=0):
        inline_keyboard.append([InlineKeyboardButton(text=waypoint, callback_data=f'set_city_waypoint_{i}')])

    inline_keyboard.append([InlineKeyboardButton(text=text_cities[-1], callback_data='add_waypoint')])
    inline_keyboard.append([InlineKeyboardButton(text="Menu", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


main_menu = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text="Set route", callback_data="set_route"), InlineKeyboardButton(text="Set period", callback_data="set_period")],
    [InlineKeyboardButton(text="Get forecast", callback_data="get_forecast")]
])

set_period_menu = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = f"{i} day", callback_data = f"set_period_{i}") for i in range(1, 5)]])

set_waypoint_menu = InlineKeyboardMarkup(inline_keyboard = 
                                         [[InlineKeyboardButton (text = "Delete city", callback_data = "delete_city"), 
                                          InlineKeyboardButton(text=  "Set city", callback_data="set_city"),
                                          InlineKeyboardButton(text="Back", callback_data="set_route")]])

def generate_response_markup(cities: list) -> InlineKeyboardMarkup:
    inline_keyboard = []
    for city in cities:
        inline_keyboard.append([InlineKeyboardButton(text=city , callback_data=f"forecast_{city}")])
    inline_keyboard.append([InlineKeyboardButton(text="Menu", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def generate_forecast_text(forecast: dict, period: str) -> str:
    text = ""
    for i in range(int(period)):

        date = forecast[i]["Date"]
        min_temp = forecast[i].get("Temperature", {}).get("Minimum", {}).get("Value", "N/A")
        max_temp = forecast[i].get("Temperature", {}).get("Maximum", {}).get("Value", "N/A")
        day_phrase = forecast[i].get("Day", {}).get("IconPhrase", "N/A")
        night_phrase = forecast[i].get("Night", {}).get("IconPhrase", "N/A")
        

        text += f"Date: {date}\n" + f"Temperature: {min_temp}°C to {max_temp}°C\n" + f"Day: {day_phrase}\n" + f"Night: {night_phrase}"

        if i < int(period) - 1:
            text += "\n\n"
    return text + (
        "\n\n"
    )