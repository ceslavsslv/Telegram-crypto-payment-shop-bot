# utils/btcpay.py
import btcpay
from app.config import BTCPAY_HOST, BTCPAY_API_KEY, BTCPAY_STORE_ID

client = btcpay.Client(host=BTCPAY_HOST, api_key=BTCPAY_API_KEY)

def create_invoice(amount: float, metadata: dict) -> str:
    try:
        invoice = client.create_invoice(
            store_id=BTCPAY_STORE_ID,
            amount=round(amount, 2),
            currency="USD",
            metadata=metadata,
        )
        return invoice["checkoutLink"]
    except Exception:
        return ""

def get_invoice_status(invoice_id: str) -> str:
    try:
        invoice = client.get_invoice(invoice_id)
        return invoice.get("status", "unknown")
    except Exception:
        return "unknown"