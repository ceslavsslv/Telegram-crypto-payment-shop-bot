# app/keyboards/admin_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Add City")],
            [KeyboardButton(text="➕ Add Product")],
            [KeyboardButton(text="➕ Add Area")],
            [KeyboardButton(text="➕ Add Amount")],
        ],
        resize_keyboard=True
    )
