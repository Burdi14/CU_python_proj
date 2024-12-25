from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core import route

# Generates main menu text displaying start, waypoints, destination, and period
def main_menu_text(route: route, period: str) -> str:
    return f"Start point: {route.start}\nWaypoints: " + " -> ".join(route.waypoints) + f"\nDestination: {route.dest}\nPeriod (days): {period}"

# Creates an inline keyboard for inputting city information
def make_input_city_menu(route: route) -> InlineKeyboardMarkup:
    text_route = []
    
    # Add start city prompt or name
    if route.start == "":
        text_route.append("Add start city")
    else:
        text_route.append(route.start)
    
    # Add destination city prompt or name
    if route.dest == "":
        text_route.append("Add destination")
    else:
        text_route.append(route.dest)
    
    # Add current waypoints to the list
    for i in range(len(route.waypoints)):
        text_route.append(route.waypoints[i])
    
    # Add prompt to add a new waypoint
    text_route.append("Add waypoint")

    # Initialize inline keyboard with start and destination buttons
    inline_keyboard = [
        [
            InlineKeyboardButton(text=text_route[0], callback_data='set_city_start'),
            InlineKeyboardButton(text=text_route[1], callback_data='set_city_dest')
        ]
    ]

    # Add buttons for each waypoint
    for i, waypoint in enumerate(text_route[2:-1], start=0):
        inline_keyboard.append([InlineKeyboardButton(text=waypoint, callback_data=f'set_city_waypoint_{i}')])

    # Add button to add a new waypoint and return to the main menu
    inline_keyboard.append([InlineKeyboardButton(text=text_route[-1], callback_data='add_waypoint')])
    inline_keyboard.append([InlineKeyboardButton(text="Menu", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

# Main menu with options to set route, set period, and get forecast
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Set route", callback_data="set_route"), InlineKeyboardButton(text="Set period", callback_data="set_period")],
    [InlineKeyboardButton(text="Get forecast", callback_data="get_forecast")]
])

# Menu for selecting forecast period
set_period_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"{i} day", callback_data=f"set_period_{i}") for i in range(1, 5)]
])

# Generates a menu for waypoint options including delete and edit
def generate_waypoint_menu(index: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Delete waypoint", callback_data=f"delete_{index}"), 
         InlineKeyboardButton(text="Set waypoint", callback_data=f"edit_waypoint_{index}"),
         InlineKeyboardButton(text="Back", callback_data="set_route")]
    ])

# Generates markup for city forecast response
def generate_response_markup(route: list) -> InlineKeyboardMarkup:
    inline_keyboard = []
    
    # Add buttons for each city in the route
    for city in route:
        inline_keyboard.append([InlineKeyboardButton(text=city, callback_data=f"forecast_{city}")])
    
    # Add button to return to the main menu
    inline_keyboard.append([InlineKeyboardButton(text="Main Menu", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

# Generates forecast text for each day in the period
def generate_forecast_text(forecast: dict, period: str) -> str:
    text = ""
    
    # Iterate over the forecast period
    for i in range(int(period)):
        # Extract forecast details for each day
        date = forecast[i]["Date"]
        min_temp = forecast[i].get("Temperature", {}).get("Minimum", {}).get("Value", "N/A")
        max_temp = forecast[i].get("Temperature", {}).get("Maximum", {}).get("Value", "N/A")
        day_phrase = forecast[i].get("Day", {}).get("IconPhrase", "N/A")
        night_phrase = forecast[i].get("Night", {}).get("IconPhrase", "N/A")
        
        # Format forecast text for the day
        text += f"Date: {date}\n" + f"Temperature: {min_temp}°C to {max_temp}°C\n" + f"Day: {day_phrase}\n" + f"Night: {night_phrase}"

        # Add spacing between forecasts for different days
        if i < int(period) - 1:
            text += "\n\n"
    
    return text + "\n\n"
