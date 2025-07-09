# run.py ar webhook
import asyncio
import logging
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web

from app.config import API_TOKEN, WEBHOOK_URL, WEBHOOK_SECRET_TOKEN
from app.bot import bot, register_routers

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def on_startup(dispatcher: Dispatcher):
    logger.info("Registering routers...")
    register_routers(dispatcher)
    logger.info("Bot is ready.")

def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.startup.register(on_startup)

    app = web.Application()
    app["bot"] = bot
    app["dispatcher"] = dp

    setup_application(app, dp, path="/webhook", secret_token=WEBHOOK_SECRET_TOKEN)
    web.run_app(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()