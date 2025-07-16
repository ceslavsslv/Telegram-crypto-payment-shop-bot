# handlers/account.py
from aiogram import Router, types, F
from app.keyboards.common import main_menu_keyboard, get_menu_button_values
from app.database import get_db
from app.utils.helpers import get_or_create_user
from app.models import Purchase, Product
from app.utils.texts import t

router = Router()

@router.message(F.text.in_(get_menu_button_values("account")))
async def handle_account(message: types.Message):
    db = next(get_db())
    user = get_or_create_user(db, telegram_id=message.from_user.id)

    purchases = db.query(Purchase).filter_by(user_id=user.id).order_by(Purchase.timestamp.desc()).all()

    if purchases:
        history_lines = [
            t("history_entry", user.language,
              product=p.product.name,
              price=p.product.price,
              timestamp=p.timestamp.strftime("%Y-%m-%d %H:%M"))
            for p in purchases
        ]
        total_spent = sum(p.product.price for p in purchases if p.product)
        history = "\n".join(history_lines)
    else:
        history = t("no_purchases", user.language)
        total_spent = 0.0

    await message.answer(t("account_info", user.language,
                           balance=user.balance,
                           user_id=user.telegram_id,
                           total=total_spent,
                           history=history))