# handlers/admin.py
from aiogram import Router, types
from aiogram.filters import Command
from app.config import ADMINS
from app.database import engine
from app.models import Base

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Access denied.")
        return

    await message.answer("👮 Admin panel (stub):\nYou can later add controls for products, cities, and users.")

@router.message(Command("syncdb"))
async def sync_db(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Access denied.")
        return

    Base.metadata.create_all(bind=engine)
    await message.answer("✅ Database tables created.")
