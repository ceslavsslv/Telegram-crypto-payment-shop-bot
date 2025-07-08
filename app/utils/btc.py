# utils/btcpay.py
import btcpay
from app.config import BTCPAY_HOST, BTCPAY_API_KEY, BTCPAY_STORE_ID

client = btcpay.Client(host=BTCPAY_HOST, api_key=BTCPAY_API_KEY)

def create_invoice(amount: float, metadata: dict) -> str:
    invoice = client.create_invoice(
        store_id=BTCPAY_STORE_ID,
        amount=round(amount, 2),
        currency="USD",
        metadata=metadata,
    )
    return invoice["checkoutLink"]

def get_invoice_status(invoice_id: str) -> str:
    invoice = client.get_invoice(invoice_id)
    return invoice.get("status", "unknown")
