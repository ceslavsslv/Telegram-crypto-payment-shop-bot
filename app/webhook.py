from flask import Flask, request, abort
import hmac, hashlib
from app.config import WEBHOOK_SECRET
from app.database import credit_user_balance

app = Flask(__name__)

@app.route("/btcpay_webhook", methods=["POST"])
def btcpay_webhook():
    raw = request.get_data()
    sig = hmac.new(WEBHOOK_SECRET.encode(), raw, hashlib.sha256).hexdigest()
    if request.headers.get("BTCPay-Sig") != f"sha256={sig}":
        abort(403)

    data = request.json
    status = data.get("type")
    metadata = data.get("metadata", {})
    order_id = metadata.get("orderId")
    telegram_id = metadata.get("telegram_id")
    amount = float(data.get("amount", 0))

    if status == "InvoiceSettled" and telegram_id:
        credit_user_balance(telegram_id, amount)
        return "OK"
    return "Ignored"