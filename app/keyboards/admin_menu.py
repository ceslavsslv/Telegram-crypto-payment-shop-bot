# app/keyboards/admin_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

ADMIN_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("➕ Add City"), KeyboardButton("🗑 Remove City")],
        [KeyboardButton("➕ Add Product"), KeyboardButton("🗑 Remove Product")],
        [KeyboardButton("➕ Add Area"), KeyboardButton("🗑 Remove Area")],
        [KeyboardButton("➕ Add Amount"), KeyboardButton("🗑 Remove Amount")],
        [KeyboardButton("📣 Broadcast"), KeyboardButton("📦 View Stock")],
        [KeyboardButton("⬅️ Exit Admin")],
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