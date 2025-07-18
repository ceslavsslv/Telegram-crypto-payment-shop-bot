# app/keyboards/admin_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_admin_keyboard():
    buttons = [
        ["➕ Add City", "🗑 Remove City"],
        ["➕ Add Product", "🗑 Remove Product"],
        ["➕ Add Area", "🗑 Remove Area"],
        ["➕ Add Amount", "🗑 Remove Amount"],
        ["🖼 Set Amount Image", "✏️ Set Amount Description"],
        ["📝 Set Delivery Note", "♻️ Remove Image/Note"],
        ["📝 Edit Purchase Info", "📦 View Stock"],
        ["💰 Edit Balance"],
        ["🔍 Lookup User", "📊 Bot Stats"],
        ["⬅️ Exit Admin"]
    ]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=b) for b in row] for row in buttons],
        resize_keyboard=True
    )
