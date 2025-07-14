# bot.py
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.config import API_TOKEN
from app.handlers import start, shop, payment, account, support, admin, referral, debug

def register_routers(dp: Dispatcher):
    dp.include_routers(
        start.router,
        shop.router,
        payment.router,
        account.router,
        support.router,
        admin.router,
        referral.router
    )
