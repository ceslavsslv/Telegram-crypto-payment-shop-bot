# handlers/start.py
import logging
from aiogram import Router, types
from aiogram.filters import Command
from app.keyboards.common import main_menu_keyboard
from app.utils.texts import texts
from app.database import get_db, get_session
from app.models import User, Purchase, Amount
from app.utils.helpers import get_or_create_user

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    try:
        ref_id = message.text.split("=", 1)[-1] if "=" in message.text else None
        user_id = message.from_user.id
        with get_session() as db:
            user = db.query(User).filter_by(id=user_id).first()
            if not user:
                referred_by = int(ref_id) if ref_id and ref_id.isdigit() and int(ref_id) != user_id else None
                user = User(id=user_id, referred_by=referred_by)
                db.add(user)
                db.commit()
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
