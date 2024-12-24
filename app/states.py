from aiogram.fsm.state import StatesGroup, State

class Route_Setting(StatesGroup):
    start = State()
    dest = State()
    waypoints = State()
    period = State()