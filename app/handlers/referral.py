from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command
from app.keyboards.common import get_menu_button_values
from app.database import get_db
from app.utils.helpers import get_or_create_user
from app.models import User, Purchase
from app.utils.texts import t

router = Router()

@router.message(F.text.in_(get_menu_button_values("referral")))
async def show_referrals(message: types.Message):
    db = next(get_db())
    user = get_or_create_user(db, telegram_id=message.from_user.id)

    invited_users = db.query(User).filter_by(referred_by=user.telegram_id).all()
    earnings = 0.0

    for u in invited_users:
        purchases = db.query(Purchase).filter_by(user_id=u.id).all()
        earnings += sum(p.product.price for p in purchases if p.product)

    await message.answer(t("ref_info", user.language, count=len(invited_users), earned=earnings))
