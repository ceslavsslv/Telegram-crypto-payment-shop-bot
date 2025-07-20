from aiogram import Router, types, F
from app.keyboards.common import get_menu_button_values, get_menu_keyboard
from app.database import get_db
from app.utils.helpers import get_or_create_user
from app.models import User, Purchase
from app.utils.texts import t
from app.database import get_db, get_session
from app.models import User, Purchase, Amount
from aiogram.types import Message
from sqlalchemy.orm import joinedload
from sqlalchemy import func

router = Router()

REFERRAL_BONUS = 1.00

@router.message(F.text.in_(get_menu_button_values("referral")))
async def referral_info(message: Message):
    user_id = message.from_user.id
    with get_session() as db:
        referrals = db.query(User).filter_by(referred_by=user_id).all()
        referral_count = len(referrals)

        total_earned = db.query(Purchase).join(User).join(Amount).filter(User.referred_by == user_id).with_entities(
            func.sum(Amount.price)).scalar() or 0.0

        ref_link = f"https://t.me/{(await message.bot.get_me()).username}?start={user_id}"

    await message.answer(
        f"👥 You referred {referral_count} users."
        f"💸 Referral earnings: {total_earned:.2f}€"
        f"🔗 Your link: {ref_link}"
    )

# This function should be triggered after a successful purchase
async def handle_referral_bonus(user_id: int):
    with get_session() as db:
        user = db.query(User).filter_by(id=user_id).first()
        if user and user.referred_by and not user.referral_bonus_claimed:
            referrer = db.query(User).filter_by(id=user.referred_by).first()
            if referrer:
                user.balance += REFERRAL_BONUS
                referrer.balance += REFERRAL_BONUS
                user.referral_bonus_claimed = True
                db.commit()
                return True
    return False
