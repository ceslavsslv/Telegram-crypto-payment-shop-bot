import os
import sys
import logging
import asyncio
from dotenv import load_dotenv
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import setup_application

# Ensure project root is in Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Webhook config
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/")
WEBHOOK_URL_FULL = f"{WEBHOOK_URL}{WEBHOOK_PATH}"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Register routers via central function
from app import bot
bot.register_routers(dp)

# Startup: set webhook
async def on_startup(app: web.Application):
    await bot.set_webhook(url=WEBHOOK_URL_FULL)  # ← removed secret_token
    logger.info(f"✅ Webhook set at {WEBHOOK_URL_FULL}")

# Shutdown: remove webhook and close
async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    await bot.session.close()
    logger.info("🛑 Webhook deleted and bot session closed.")

# Manual webhook set (if run directly)
async def manual_set_webhook():
    await bot.set_webhook(url=WEBHOOK_URL_FULL)
    await bot.session.close()
    print(f"✅ Webhook manually set at {WEBHOOK_URL_FULL}")

# Start web server
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "set_webhook":
        asyncio.run(manual_set_webhook())
    else:
        app = web.Application()
        app.on_startup.append(on_startup)
        app.on_shutdown.append(on_shutdown)

        setup_application(app, dp, path=WEBHOOK_PATH)
        logger.info(f"📍 Webhook path registered at {WEBHOOK_PATH}")
        logger.info(f"🌐 Starting server at {HOST}:{PORT}")
        web.run_app(app, host=HOST, port=PORT)