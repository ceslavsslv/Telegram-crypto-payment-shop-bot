# bot.py
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.config import API_TOKEN
from app.handlers import start, shop, payment, account, support, admin, referral

def register_routers(dispatcher: Dispatcher):
    dispatcher.include_routers(
        start.router,
        shop.router,
        payment.router,
        account.router,
        support.router,
        admin.router,
        referral.router
    )
