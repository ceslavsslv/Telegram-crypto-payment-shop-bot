#!/usr/bin/env bash
# Stop the bot if running via the PID file
if [[ -f bot.pid ]]; then
  PID=$(cat bot.pid)
  kill "$PID" && rm bot.pid
  echo "Bot process $PID stopped."
else
  echo "No bot.pid file found. Is the bot running?"
fi