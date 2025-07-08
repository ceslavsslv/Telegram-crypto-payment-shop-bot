# config.py
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")  # Telegram bot token
ADMINS = list(map(int, os.getenv("ADMINS", "").split(",")))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN")
DB_URL = os.getenv("DATABASE_URL")
BTCPAY_HOST = os.getenv("BTCPAY_HOST")
BTCPAY_API_KEY = os.getenv("BTCPAY_API_KEY")
BTCPAY_STORE_ID = os.getenv("BTCPAY_STORE_ID")
DB_PATH = "shop.db"
LANGUAGES = ["en", "ru"]