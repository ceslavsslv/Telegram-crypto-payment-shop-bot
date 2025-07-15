# handlers/admin.py
from aiogram import Router, types, F
from aiogram.filters import Command
from app.config import ADMINS
from app.database import engine
from app.models import Base
from app.keyboards.admin_menu import get_admin_keyboard

router = Router()

def is_admin(user_id: int) -> bool:
    return user_id in ADMINS

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Access denied.")
        return

    await message.answer("👤 Welcome Admin. Choose action:", reply_markup=get_admin_keyboard())

@router.message(Command("syncdb"))
async def sync_db(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Access denied.")
        return

    Base.metadata.create_all(bind=engine)
    await message.answer("✅ Database tables created.")
