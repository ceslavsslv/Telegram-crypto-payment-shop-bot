# handlers/account.py
from aiogram import Router, types, F
from app.keyboards.common import main_menu_keyboard, get_menu_button_values
from app.database import get_db
from app.utils.helpers import get_or_create_user

router = Router()

@router.message(F.text.in_(get_menu_button_values("language")))
async def handle_account(message: types.Message):
    try:
        db = next(get_db())
        user = get_or_create_user(db, telegram_id=message.from_user.id)
        await message.answer(f"👤 Your balance: ${user.balance:.2f}\nLanguage: {user.language.upper()}")
    except Exception:
        await message.answer("⚠️ Failed to load your account info.")