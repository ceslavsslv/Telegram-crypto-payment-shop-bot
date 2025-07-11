#!/bin/bash

# Activate virtual environment if you use one
# source venv/bin/activate

echo "🚀 Starting Flask Telegram Webhook Server..."
export API_TOKEN="your_token_here"
export PORT=8000  # Ensure this matches NGINX proxy

python flask_webhook_server.py
