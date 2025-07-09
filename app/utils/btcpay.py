# Updated btcpay.py with retry logic
import requests
import time
from app.config import BTCPAY_API_KEY, BTCPAY_HOST, BTCPAY_STORE_ID

MAX_RETRIES = 3
RETRY_DELAY = 2

def create_invoice(amount: float, metadata: dict) -> str:
    url = f"{BTCPAY_HOST}/api/v1/stores/{BTCPAY_STORE_ID}/invoices"
    headers = {
        "Authorization": f"token {BTCPAY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "amount": round(amount, 2),
        "currency": "EUR",
        "metadata": metadata
    }

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            if resp.status_code == 200:
                return resp.json().get("checkoutLink", "")
        except Exception:
            pass
        time.sleep(RETRY_DELAY)
    return ""

def get_invoice_status(invoice_id: str) -> str:
    url = f"{BTCPAY_HOST}/api/v1/stores/{BTCPAY_STORE_ID}/invoices/{invoice_id}"
    headers = {"Authorization": f"token {BTCPAY_API_KEY}"}

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                return resp.json().get("status", "unknown")
        except Exception:
            pass
        time.sleep(RETRY_DELAY)
    return "unknown"