import os
import logging
from dotenv import load_dotenv
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import setup_application
from aiogram.types import Message

# Load environment variables from .env
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")            # e.g. https://vielapardomam.duckdns.org
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN")  # optional, for added security
PORT = int(os.getenv("PORT", 5000))

# Webhook settings
WEBHOOK_PATH = f"/webhook/{API_TOKEN}"
WEBHOOK_URL_FULL = f"{WEBHOOK_URL}{WEBHOOK_PATH}"

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Import and register your handlers here
# Replace these with your actual modules
from handlers.start import register_handlers as register_start
from handlers.shop import register_handlers as register_shop
from handlers.payment import register_handlers as register_payments
from handlers.admin import register_handlers as register_admin
from handlers.language import register_handlers as register_language
from handlers.referral import register_handlers as register_referral
from handlers.support import register_handlers as register_support
from handlers.account import register_handlers as register_account

register_start(dp)
register_shop(dp)
register_payments(dp)
register_admin(dp)
register_language(dp)
register_referral(dp)
register_support(dp)
register_account(dp)
# Add additional handler modules as needed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Startup: set webhook
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL_FULL)
    logger.info(f"Webhook registered at {WEBHOOK_URL_FULL}")

# Shutdown: remove webhook and close
async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    await bot.session.close()
    logger.info("Webhook deleted and bot session closed.")

# Main entry
if __name__ == "__main__":
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    # Setup webhook route in aiohttp
    setup_application(app, dp, path=WEBHOOK_PATH, secret_token=WEBHOOK_SECRET_TOKEN)
    logger.info(f"Starting server at 0.0.0.0:{PORT}")
    web.run_app(app, host="0.0.0.0", port=PORT)