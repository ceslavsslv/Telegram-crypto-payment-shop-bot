# handlers/news.py
from aiogram import Router, types, F
from app.keyboards.common import get_menu_button_values

router = Router()

NEWS_CHANNEL_UNAME = "@YourSupportUsername"

@router.message(F.text.in_(get_menu_button_values("news")))
async def handle_news(message: types.Message):
    try:
        await message.answer(f"☎️ Here is our news channel:\n{NEWS_CHANNEL_UNAME}")
    except Exception:
        await message.answer("⚠️ Failed to send support info.")