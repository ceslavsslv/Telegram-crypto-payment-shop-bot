# app/states/shop.py

from aiogram.fsm.state import StatesGroup, State

class ShopState(StatesGroup):
    city = State()
    product = State()
    area = State()
    amount = State()
