# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram bot settings
API_TOKEN = os.getenv("API_TOKEN")  # Telegram bot token
ADMINS = list(map(int, os.getenv("ADMINS", "").split(",")))

# Webhook settings
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")

# Hosting settings
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

# Database
DB_URL = os.getenv("DATABASE_URL")
DB_PATH = os.getenv("DB_PATH")

# BTCPay server
BTCPAY_HOST = os.getenv("BTCPAY_HOST")
BTCPAY_API_KEY = os.getenv("BTCPAY_API_KEY")
BTCPAY_STORE_ID = os.getenv("BTCPAY_STORE_ID")

# Language support
LANGUAGES = os.getenv("LANGUAGES", "en,ru").split(",")