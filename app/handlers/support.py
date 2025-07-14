# handlers/support.py
from aiogram import Router, types, F
from app.keyboards.common import get_menu_button_values

router = Router()

SUPPORT_USERNAME = "@YourSupportUsername"

@router.message(F.text == "❓ Support")
async def handle_support(message: types.Message):
    try:
        await message.answer(f"☎️ Please contact our support:\n{SUPPORT_USERNAME}")
    except Exception:
        await message.answer("⚠️ Failed to send support info.")