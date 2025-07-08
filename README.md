# 🛍️ Telegram Crypto Shop Bot (Aiogram v3 + BTCPay + Flask)

A dynamic, crypto-powered Telegram shop bot written in **Python** using **Aiogram v3**, **BTCPay Server**, **SQLite**, and **Flask**. Supports:

- 🔗 Self-hosted BTCPay-based crypto balance system
- 🏙️ Dynamic catalog (Cities → Categories → Products)
- 🛒 Simple purchase flow with Telegram inline buttons
- 🧾 Purchase instructions sent after order
- 🌐 Language switching (🇷🇺 / 🇺🇸)
- 👨‍💻 Admin panel via bot for managing products, cities, and categories (minimal)

---

## 🚀 Features

✅ Telegram webhook via Flask  
✅ Aiogram v3 async handlers  
✅ Inline navigation (city → product → amount)  
✅ User balance stored securely in SQLite  
✅ BTCPay Server integration for top-up QR/invoice generation  
✅ Inline admin panel for managing catalog  
✅ Language switcher with persistent settings

---

## 🧰 Requirements

- Python 3.10+
- A running **BTCPay Server** instance
- Telegram Bot Token
- Flask (for webhook delivery)

---

## 🛠️ Installation

1. **Clone the repo**

```bash
git clone https://github.com/yourname/telegram-crypto-shop-bot.git
cd telegram-crypto-shop-bot
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure bot**

Edit `config.py`:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN"
BTCPAY_URL = "https://your.btcpayserver.tld"
BTCPAY_API_KEY = "api-key-here"
BTCPAY_STORE_ID = "store-id"
WEBHOOK_SECRET = "yourwebhooksecret"
WEBHOOK_PATH = "/webhook/telegram"
DOMAIN = "https://your.domain.tld"  # Public domain for webhook
```

4. **Run bot + Flask webhook**

```bash
python bot.py
```

---

## ⚙️ Project Structure

```text
.
├── bot.py                  # Launches Flask + Aiogram bot
├── config.py               # Configs
├── database.py             # SQLite models + helpers
├── btc_pay.py              # BTCPay client logic
├── handlers/
│   ├── start.py            # /start, /shop, menu
│   ├── shop.py             # Product flow
│   ├── language.py         # Language change
│   ├── admin.py            # Simple admin commands
├── keyboards/
│   └── menu.py             # Main menu keyboard
├── requirements.txt
└── README.md
```

---

## 📦 Dynamic Catalog Design

- Admin can add:
  - Cities
  - Categories
  - Products (per city + category)

Handled via inline menus or database prefill. Admin access protected via Telegram ID.

---

## 🔐 BTCPay Integration

- Balance-based system
- Users top-up via invoice (QR code or URL)
- Invoice status polled or webhook-based update
- After payment, user balance is increased
- Orders subtract balance

---

## 📲 Telegram Flow Example

1. User joins, presses `🛍 Shopping`
2. Selects city → category → product → amount
3. Chooses `💰 Buy with Balance`
4. Gets order confirmation + instructions
5. Support and language tools available anytime

---

## 📌 Notes

- Project is fully async (Aiogram v3)
- You can deploy on **Render**, **Fly.io**, or any VPS
- Use `ngrok` for local testing if needed

---

## 🧑‍💻 Admin Commands (in-bot)

- `/add_city` – Add city
- `/add_category` – Add product category
- `/add_product` – Add product with name, price, stock

More coming soon.

---

## 📄 License

MIT License. Use and modify freely, but please don’t abuse this template.

---

## 💬 Contact

Built with ❤️ by [YourName]. Want help or custom build? Open an issue or contact me directly.
