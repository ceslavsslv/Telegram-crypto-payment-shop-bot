#!/usr/bin/env bash
set -e

# Navigate to project directory
cd /home/debian/Telegram-crypto-payment-shop-bot-main

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Activate virtual environment
source /home/debian/duckdns/venv/bin/activate

# Start bot in background, log output, record PID
nohup python run.py > bot.log 2>&1 &
echo $! > bot.pid

echo "Bot started with PID $(cat bot.pid)"