# app/keyboards/admin_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_admin_keyboard():
    buttons = [
        ["➕ Add City", "➕ Add Product"],
        ["➕ Add Area", "➕ Add Amount"],
        ["📝 Edit Notes", "📦 View Stock"],
        ["💰 Edit Balance", "🔄 Refund User"],
        ["🔍 Lookup User", "📊 Bot Stats"],
        ["⬅️ Exit Admin"]
    ]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=b) for b in row] for row in buttons],
        resize_keyboard=True
    )
