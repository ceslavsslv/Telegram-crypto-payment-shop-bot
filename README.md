# 🛍️ Telegram Crypto Shop Bot (Aiogram v3 + BTCPay)

A dynamic, crypto-powered Telegram shop bot using **Python**, **Aiogram v3**, **SQLite**, and **BTCPay Server**. Fully self-hosted with balance-based purchases, product selection, and city-specific catalogs.

---

## 🚀 Features

- 🔗 Crypto payments via BTCPay Server
- 🏙️ City → Product → Quantity navigation
- 💳 Balance top-up and purchase system
- 🧾 Instant delivery after purchase
- 🌐 Multi-language support (`en`, `ru`)
- 👤 Admin panel inside Telegram for managing catalog
- 🖥️ Self-hosted with webhook

---

## 🧰 Requirements

- Python 3.10+
- A working BTCPay Server instance
- Telegram Bot Token
- SQLite or PostgreSQL

---

## 🛠️ Installation

```bash
# Clone the repository
cd ~
git clone https://github.com/yourname/Telegram-crypto-payment-shop-bot.git
cd Telegram-crypto-payment-shop-bot

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create and edit your .env file
cp .env.example .env
nano .env

# Initialize the database
python init_db.py

# Make scripts executable
chmod +x start_bot.sh stop_bot.sh
```

---

## 📁 .env Configuration Example

```ini
API_TOKEN=your_telegram_bot_token
ADMINS=123456789
WEBHOOK_URL=https://yourdomain.com  # Full path is added automatically
WEBHOOK_SECRET_TOKEN=supersecret

HOST=0.0.0.0
PORT=8000

DATABASE_URL=sqlite:///shop.db
DB_PATH=shop.db

BTCPAY_HOST=https://your.btcpay.url
BTCPAY_API_KEY=your-api-key
BTCPAY_STORE_ID=your-store-id

LANGUAGES=en,ru
```

---

## ▶️ Running the Bot

```bash
# Activate your environment
source venv/bin/activate

# Start using script
./start_bot.sh

# Stop using script
./stop_bot.sh
```

Bot logs will be written to `bot.log` and its PID to `bot.pid`.

---

## 🔗 Setting the Webhook Manually

If the webhook is not active or your bot doesn’t respond, set it manually:

```bash
python set_webhook.py
```

Create `set_webhook.py`:
```python
import asyncio
from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

async def main():
    bot = Bot(token=API_TOKEN)
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    print(f"✅ Webhook set to: {WEBHOOK_URL}/webhook")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🔄 Run 24/7 using systemd

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Paste:
```ini
[Unit]
Description=Telegram Crypto Shop Bot
After=network.target

[Service]
User=your-linux-user
WorkingDirectory=/home/your-linux-user/Telegram-crypto-payment-shop-bot
EnvironmentFile=/home/your-linux-user/Telegram-crypto-payment-shop-bot/.env
ExecStart=/home/your-linux-user/Telegram-crypto-payment-shop-bot/venv/bin/python run.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reexec
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

---

## 🛑 If Things Go Wrong

```bash
# View logs
journalctl -u telegram-bot.service -e

# Stop the service
sudo systemctl stop telegram-bot

# Restart the bot
sudo systemctl restart telegram-bot

# Kill manually (if pid file exists)
./stop_bot.sh

# Tail live log 
tail -f bot.log

#Show last 50 lines
tail -n 50 bot.log

```

---

## 📬 Telegram Commands (if implemented)

- `/start` – show menu
- `/shop` – browse products
- `/balance` – view balance
- `/addfunds` – top up crypto
- `/account` – view purchases
- `/support` – contact support
- `/language` – switch language

---
