# set_webhook.py
import requests
from app.config import API_TOKEN, WEBHOOK_URL, WEBHOOK_SECRET_TOKEN

url = f"https://api.telegram.org/bot{API_TOKEN}/setWebhook"

payload = {
    "url": f"{WEBHOOK_URL}/webhook",
    "secret_token": WEBHOOK_SECRET_TOKEN
}

response = requests.post(url, data=payload)

if response.status_code == 200:
    print("✅ Webhook set successfully:", response.json())
else:
    print("❌ Failed to set webhook:", response.status_code, response.text)
