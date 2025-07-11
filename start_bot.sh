#!/usr/bin/env bash
set -euo pipefail

# === Automātiski nosaka projekta ceļu ===
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_ACTIVATE="$PROJECT_DIR/venv/bin/activate"

# === Ieiet projekta mapē ===
cd "$PROJECT_DIR"

# === Ielādē .env, ja tas eksistē ===
if [[ -f .env ]]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "❌ .env file not found in $PROJECT_DIR" >&2
  exit 1
fi

# === Nodrošina pareizu Python ceļu (handleriem) ===
export PYTHONPATH="$PROJECT_DIR"

# === Aktivē virtuālo vidi ===
if [[ -f "$VENV_ACTIVATE" ]]; then
  # shellcheck disable=SC1090
  source "$VENV_ACTIVATE"
else
  echo "❌ Cannot find venv activate script at $VENV_ACTIVATE" >&2
  exit 1
fi

# === Noņem iepriekšējo PID (ja nepieciešams) ===
if [[ -f bot.pid ]]; then
  PID=$(cat bot.pid)
  if kill -0 "$PID" >/dev/null 2>&1; then
    echo "⚠️ Bot already running (PID $PID). Killing..."
    kill "$PID"
    sleep 1
  fi
  rm -f bot.pid
fi

# === Palaiž botu fonā ===
echo "🚀 Starting bot..."
nohup python run.py > bot.log 2>&1 &
echo $! > bot.pid
echo "✅ Bot started (PID $(cat bot.pid)) – logs in bot.log"
