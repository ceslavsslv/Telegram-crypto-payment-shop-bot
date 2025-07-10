# set_webhook.py
import asyncio
from aiogram import Bot
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

async def main():
    bot = Bot(token=API_TOKEN)
    await bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook set to: {WEBHOOK_URL}")

if __name__ == "__main__":
    asyncio.run(main())
