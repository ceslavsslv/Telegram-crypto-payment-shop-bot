from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    keyboard = [
        [KeyboardButton(text="🛍 Shopping"), KeyboardButton(text="💶 Add funds")],
        [KeyboardButton(text="🛒 Account"), KeyboardButton(text="☎️ Support")],
        [KeyboardButton(text="🗞 News")],
        [KeyboardButton(text="🔷 Referral system")],
        [KeyboardButton(text="🇷🇺 Сменить язык")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, is_persistent=True)
