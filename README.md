# Telegram Crypto Shop Bot

## Features
- Dynamic city → product → amount catalog
- Self-hosted crypto top-up using BTCPay Server
- Balance and purchase tracking
- Webhook to auto-credit balances

## Setup
1. Clone the repo
2. Create a `.env` file with:
   ```
   API_TOKEN=your_telegram_token
   BTCPAY_HOST=https://your.btcpay.server
   BTCPAY_API_KEY=your_api_key
   BTCPAY_STORE_ID=store_id_here
   WEBHOOK_SECRET=your_webhook_secret
   ```
3. Run the bot:
   ```bash
   python bot.py
   ```
4. Run the webhook listener:
   ```bash
   flask run --port=3000
   ```
5. Set BTCPay webhook to: `https://yourserver.com/btcpay_webhook`

## TODO
- Admin product manager
- Multilingual support
- Telegram login integration

 ## Webhook Listener (Flask)
Run this separately with:
```bash
flask --app webhook.py run --port=3000
```

Set your BTCPay Server webhook to:
```
https://yourdomain.com/btcpay_webhook
```

Make sure to use the same secret from `WEBHOOK_SECRET` environment variable.