# config.py
import os

API_TOKEN = os.getenv("API_TOKEN")  # Telegram bot token
BTCPAY_HOST = os.getenv("BTCPAY_HOST")
BTCPAY_API_KEY = os.getenv("BTCPAY_API_KEY")
BTCPAY_STORE_ID = os.getenv("BTCPAY_STORE_ID")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
DB_PATH = "shop.db"
