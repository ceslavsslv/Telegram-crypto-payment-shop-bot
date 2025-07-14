from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command
from app.keyboards.common import get_menu_button_values

router = Router()

@router.message(F.text.in_(get_menu_button_values("referral")))
async def handle_referral_command(message: Message):
    await message.answer("Here is your referral link!")
