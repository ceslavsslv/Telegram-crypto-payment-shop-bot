# handlers/start.py
import logging
from aiogram import Router, types
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
        logging.exception("Start handler failed")
        await message.answer("⚠️ Failed to start.")
