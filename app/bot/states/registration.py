from aiogram.fsm.state import State, StatesGroup


class RegistrationState(StatesGroup):
    waiting_name = State()
    waiting_age = State()
    waiting_city = State()
    waiting_about = State()
