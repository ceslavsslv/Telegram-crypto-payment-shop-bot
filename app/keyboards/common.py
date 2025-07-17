# keyboards/common.py
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.utils.texts import texts
from app.utils.helpers import t

def main_menu_keyboard(language: str = "en") -> ReplyKeyboardMarkup:
    b = texts["menu_buttons"]
    builder = ReplyKeyboardBuilder()

    builder.button(text=b["shopping"][language])
    builder.button(text=b["add_funds"][language])
    builder.button(text=b["account"][language])
    builder.button(text=b["support"][language])
    builder.button(text=b["news"][language])
    builder.button(text=b["referral"][language])
    builder.button(text=b["language"][language])

    return builder.adjust(2, 2, 3).as_markup(resize_keyboard=True)

def get_menu_button_values(key: str) -> list[str]:
    return list(texts["menu_buttons"].get(key, {}).values())

def back_main_menu_buttons(lang):
    return [
        {"label": t("BACK", lang), "data": "back"},
        {"label": t("MAIN_MENU", lang), "data": "start"},
    ]
