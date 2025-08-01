# bot.py
from aiogram import Dispatcher
from app.handlers import languages, start, shop, payment, account, support, admin, referral, news

def register_routers(dp: Dispatcher):
    dp.include_routers(
        start.router,
        shop.router,
        payment.router,
        account.router,
        support.router,
        admin.router,
        referral.router,
        languages.router,
        news.router
    )
