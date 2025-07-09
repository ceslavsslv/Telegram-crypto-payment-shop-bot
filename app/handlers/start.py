# handlers/start.py
from aiogram import Router, types, F
from aiogram.filters import Command
from app.keyboards.common import main_menu_keyboard
from app.utils.texts import texts
from app.database import get_db
from app.utils.helpers import get_or_create_user

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        db = next(get_db())
        user = get_or_create_user(db, telegram_id=user_id)
        language = user.language or "en"
        await message.answer(
            texts["start"].get(language, "Welcome!"),
            reply_markup=main_menu_keyboard(language)
        )
    except Exception:
        await message.answer("⚠️ Failed to start.")

@router.message(F.text.in_(["🇷🇺 Change the language", "🇺🇸 Сменить язык"]))
async def language_switch(message: types.Message):
    try:
        db = next(get_db())
        user = get_or_create_user(db, telegram_id=message.from_user.id)
        user.language = "ru" if user.language == "en" else "en"
        db.commit()
        await message.answer(
            texts["language_set"].get(user.language, "Language updated."),
            reply_markup=main_menu_keyboard(user.language)
        )
    except Exception:
        await message.answer("⚠️ Language change failed.")
