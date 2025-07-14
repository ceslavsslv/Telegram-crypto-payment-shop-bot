import os #nevajag
import sys
import logging
from os import getenv
from app.bot import register_routers
from aiohttp import web
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage #nevajag
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# Ensure project root is in Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env

API_TOKEN = getenv("API_TOKEN")
WEBHOOK_URL = getenv("WEBHOOK_URL")
HOST = getenv("HOST")
PORT = int(getenv("PORT"))
WEBHOOK_PATH = getenv("WEBHOOK_PATH")
WEBHOOK_URL_FULL = f"{WEBHOOK_URL}{WEBHOOK_PATH}"

# Initialize bot and dispatcher
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# Register routers via central function
register_routers(dp)

# Startup: set webhook
async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL_FULL)
    print(f"✅ Webhook set at {WEBHOOK_URL_FULL}")

# Shutdown: remove webhook and close
async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    await bot.session.close()
    print(f"🛑 Webhook deleted and bot session closed.")

# Start web server
def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    dp.startup.register(on_startup)
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot, 
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=HOST, port=PORT)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    logging.info(f"👉 WEBHOOK_PATH: {WEBHOOK_PATH}")
    logging.info(f"👉 WEBHOOK_URL_FULL: {WEBHOOK_URL_FULL}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
        