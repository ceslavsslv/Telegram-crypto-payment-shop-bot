#!/usr/bin/env bash
set -euo pipefail

# === Determine project directory dynamically ===
# Uses the directory where this script resides
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_ACTIVATE="/home/debian/telegram/Telegram-crypto-payment-shop-bot-main/venv/bin/activate"   # adjust if your venv is elsewhere

# === Change into project directory ===
cd "$PROJECT_DIR"

# === Load environment variables ===
if [[ -f .env ]]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "❌ .env file not found in $PROJECT_DIR" >&2
  exit 1
fi

# === Activate virtualenv ===
if [[ -f "$VENV_ACTIVATE" ]]; then
  # shellcheck disable=SC1090
  source "$VENV_ACTIVATE"
else
  echo "❌ Cannot find venv activate script at $VENV_ACTIVATE" >&2
  exit 1
fi

# === Start bot in background ===
nohup python run.py > bot.log 2>&1 &
echo $! > bot.pid

echo "✅ Bot started (PID $(cat bot.pid)) – logs in bot.log"