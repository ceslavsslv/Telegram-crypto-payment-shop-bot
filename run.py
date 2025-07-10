import os
import atexit
from dotenv import load_dotenv
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import Message

# Load environment variables from .env
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_HOST = os.getenv("WEBHOOK_URL")         
WEBHOOK_PATH = f"/webhook/{API_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Web server settings
WEBAPP_HOST = "127.0.0.1"
WEBAPP_PORT = int(os.getenv("PORT", 5000))

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Example handler
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello! I\u2019m up and running via webhook.")

# Startup: register webhook
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook registered: {WEBHOOK_URL}")

# Shutdown: remove webhook and close session
async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    await bot.session.close()
    print("Webhook deleted and session closed.")

# Create and configure aiohttp web app
app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
# Route Telegram updates to dispatcher
app.router.add_post(WEBHOOK_PATH, dp)

if __name__ == "__main__":
    print(f"Starting server on {WEBAPP_HOST}:{WEBAPP_PORT}...")
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)