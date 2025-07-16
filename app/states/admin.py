# app/states/admin.py

from aiogram.fsm.state import StatesGroup, State

class AdminState(StatesGroup):
    choose_action = State()
    city_name = State()

    product_city = State()
    product_name = State()

    area_product = State()
    area_name = State()

    amount_area = State()
    amount_label = State()
    amount_price = State()
