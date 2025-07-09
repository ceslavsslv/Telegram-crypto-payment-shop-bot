# bot.py
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from app.config import API_TOKEN
from app.handlers import start, shop, payment, account

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

def register_routers(dispatcher: Dispatcher):
    dispatcher.include_routers(
        start.router,
        shop.router,
        payment.router,
        account.router,
        support.router,
        admin.router
    )
