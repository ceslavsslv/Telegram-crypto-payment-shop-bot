import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load from env
TOKEN = os.getenv("API_TOKEN")
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook/")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))

# Init bot + dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Setup web app
app = web.Application()

# ✅ Manually bind webhook route
app.router.add_post(WEBHOOK_PATH, SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET_TOKEN))

async def main():
    logger.info(f"🌐 Starting server at {HOST}:{PORT}")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=HOST, port=PORT)
    await site.start()
    logger.info(f"✅ Webhook set at {WEBHOOK_PATH}")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
