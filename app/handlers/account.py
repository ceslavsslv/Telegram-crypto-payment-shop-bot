# handlers/account.py
from aiogram import Router, types, F
from app.keyboards.common import main_menu_keyboard, get_menu_button_values
from app.database import get_db
from app.utils.helpers import get_or_create_user
from app.models import Purchase, Product, Amount
from app.utils.texts import t

router = Router()

@router.message(F.text.in_(get_menu_button_values("account")))
async def handle_account(message: types.Message):
    db = next(get_db())
    user = get_or_create_user(db, telegram_id=message.from_user.id)
    purchases = db.query(Purchase).filter_by(user_id=user.id).order_by(Purchase.timestamp.desc()).all()
    if purchases:
        history_lines = []
        total_spent = 0.0
        for p in purchases:
            amount = db.query(Amount).filter_by(id=p.amount_id).first()
            if amount:
                history_lines.append(
                    f"🛒 {amount.label} – {p.total_price:.2f}€ at {p.timestamp.strftime('%Y-%m-%d %H:%M')}"
                )
                total_spent += p.total_price
        history = "\n".join(history_lines) if history_lines else t("no_purchases", user.language)
    else:
        history = t("no_purchases", user.language)
        total_spent = 0.0

    await message.answer(t("account_info", user.language,
                           balance=user.balance,
                           user_id=user.telegram_id,
                           total=total_spent,
                           history=history))