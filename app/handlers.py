from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import Route_Setting
from core import get_5day_forecast, get_location_key
import kb
import core
from datetime import datetime

router  = Router()

forecasts = {}
cities = core.cities()
period = "__"

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Privet! I can show you the weather forecast on your route \nPlease, set your way points and time period. \nTap /weather to go to the menu.\nTap /help if you need help.")

@router.message(Command("help"))
async def help(message: Message):
    await message.answer("Type /weather to get the menu. Then set start city and destination, some waypoints if you wish to, and to get the weather forecast on your route")


@router.message(Command("weather"))
async def weather(message: Message):
    await message.answer(kb.main_menu_text(cities, period), reply_markup=kb.main_menu)

@router.callback_query(F.data == "main_menu")
async def weather(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(kb.main_menu_text(cities, period), reply_markup=kb.main_menu)

@router.callback_query(F.data == "set_period")
async def set_period(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Select period", reply_markup=kb.set_period_menu)

@router.callback_query(F.data.startswith("set_period_"))
async def set_period(call: CallbackQuery, state: FSMContext):
    global period, cities
    period = call.data.split("_")[2]
    await call.message.edit_text(kb.main_menu_text(cities, period), reply_markup=kb.main_menu)

@router.callback_query(F.data == "set_route")
async def set_route(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Set your route", reply_markup=kb.make_input_city_menu(cities))

@router.callback_query(F.data == "add_waypoint")
async def add_waypoint(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Type the name of a waypoint")
    await state.set_state(Route_Setting.waypoints)

@router.message(Route_Setting.waypoints)
async def save_waypoint(message: Message, state: FSMContext):
    global cities
    cities.waypoints.append(message.text)
    await message.answer("Set your route", reply_markup=kb.make_input_city_menu(cities))
    await state.clear()

@router.callback_query(F.data.startswith("set_city_"))
async def set_city(call: CallbackQuery, state: FSMContext):
    global cities
    if "start" in call.data:
        await state.set_state(Route_Setting.start)
        await call.message.edit_text("Type the name of the start city...")
    if "dest" in call.data:
        await state.set_state(Route_Setting.dest)
        await call.message.edit_text("Type the name of the destination city...")
    if "waypoint" in call.data:
        await state.set_state(Route_Setting.waypoints)
        await call.message.edit_text("Type the name of the waypoint...")
    
    
@router.message(Route_Setting.start)
async def process_start_point(message: Message, state: FSMContext):
    global cities
    cities.start = message.text
    await message.answer("Set your route", reply_markup=kb.make_input_city_menu(cities))
    await state.clear()

@router.message(Route_Setting.dest)
async def process_dest_point(message: Message, state: FSMContext):
    global cities
    cities.dest = message.text
    await message.answer("Set your route", reply_markup=kb.make_input_city_menu(cities))
    await state.clear()

@router.callback_query(F.data.startswith("delete_waypoint_"))
async def delete_waypoint(call: CallbackQuery, state: FSMContext):
    global cities
    index = int(call.data.split("_")[1])
    cities.waypoints.pop(index)
    await call.message.edit_text("Set your route", reply_markup=kb.make_input_city_menu(cities))

@router.callback_query(F.data == "get_forecast")
async def get_forecast(call: CallbackQuery, state: FSMContext):
    global cities
    waypoints = cities.waypoints
    waypoints.insert(0, cities.start)
    waypoints.append(cities.dest)
    global forecasts
    import json
    for city in waypoints:
        city_key, city_localize = get_location_key(city)
        city_forecast = get_5day_forecast(city_key)
        forecasts.update( {city_localize:city_forecast})
        # #make city localize dont forget
    #formatting the date
    for day in range(int(period)):
        for city in forecasts:
            tmp = forecasts[city][day]["Date"]
            date_obj = datetime.fromisoformat(tmp)
            formatted_date = date_obj.strftime("%m.%d")
            forecasts[city][day]["Date"] = formatted_date

    await call.message.answer(text = city + "\n" + kb.generate_forecast_text(list(forecasts.values())[0], period), 
                              reply_markup=kb.generate_response_markup(list(forecasts.keys())))

@router.callback_query(F.data.startswith("forecast_"))
async def handle_forecast(call: CallbackQuery):
    global forecasts
    city = call.data.split("_")[1]
    await call.message.answer(text = city + "\n" + kb.generate_forecast_text(forecasts[city], period), 
                              reply_markup=kb.generate_response_markup(list(forecasts.keys())))