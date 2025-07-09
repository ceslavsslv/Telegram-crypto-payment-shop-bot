from aiogram import Router

router = Router()

@router.message(Command("referral"))
async def handle_referral_command(message: Message):
    await message.answer("Here is your referral link!")
