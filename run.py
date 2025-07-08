# run.py
from flask import Flask, request, abort
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from app.config import API_TOKEN, WEBHOOK_URL, WEBHOOK_SECRET_TOKEN
from app.bot import register_routers

app = Flask(__name__)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())
register_routers(dp)

@app.post("/webhook")
def telegram_webhook():
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET_TOKEN:
        abort(403)

    update = request.get_data().decode("utf-8")
    dp.feed_raw_update(bot=bot, update=update)
    return "", 200

if __name__ == "__main__":
    import asyncio
    from aiogram.client.default import DefaultBotProperties
    from aiogram.enums import ParseMode

    async def main():
        await bot.set_webhook(
            url=WEBHOOK_URL,
            secret_token=WEBHOOK_SECRET_TOKEN
        )
        print("Webhook set.")

    asyncio.run(main())
    app.run(host="0.0.0.0", port=5000)
