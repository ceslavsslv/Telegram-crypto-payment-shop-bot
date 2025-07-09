# Rewritten btcpay.py using plain requests (API key auth)
import requests
from app.config import BTCPAY_API_KEY, BTCPAY_HOST, BTCPAY_STORE_ID

def create_invoice(amount: float, metadata: dict) -> str:
    try:
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
        resp = requests.post(url, json=payload, headers=headers)
        data = resp.json()
        return data.get("checkoutLink", "")
    except Exception:
        return ""

def get_invoice_status(invoice_id: str) -> str:
    try:
        url = f"{BTCPAY_HOST}/api/v1/stores/{BTCPAY_STORE_ID}/invoices/{invoice_id}"
        headers = {"Authorization": f"token {BTCPAY_API_KEY}"}
        resp = requests.get(url, headers=headers)
        data = resp.json()
        return data.get("status", "unknown")
    except Exception:
        return "unknown"
