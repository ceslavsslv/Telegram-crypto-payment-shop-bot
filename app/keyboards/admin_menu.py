# app/keyboards/admin_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

ADMIN_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Add City"), KeyboardButton(text="🗑 Remove City")],
        [KeyboardButton(text="➕ Add Product"), KeyboardButton(text="🗑 Remove Product")],
        [KeyboardButton(text="➕ Add Area"), KeyboardButton(text="🗑 Remove Area")],
        [KeyboardButton(text="➕ Add Amount"), KeyboardButton(text="🗑 Remove Amount")],
        [KeyboardButton(text="📣 Broadcast"), KeyboardButton(text="📦 View Stock")],
        [KeyboardButton(text="⬅️ Exit Admin")],
    ],
    resize_keyboard=True
)

CANCEL_KB = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("❌ Cancel")]],
    resize_keyboard=True
)
#Vecais
'''
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
'''