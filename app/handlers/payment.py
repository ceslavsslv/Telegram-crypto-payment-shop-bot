# handlers/payment.py
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database import get_db, get_session
from app.utils.helpers import get_or_create_user, get_product, deduct_balance, add_purchase
from app.utils.btcpay import create_invoice
from app.keyboards.common import get_menu_button_values
from app.models import Product, Amount
from aiogram.fsm.context import FSMContext
from app.utils import texts
from app.utils.texts import t

router = Router()

@router.callback_query(F.data == "pay_balance")
async def handle_balance_payment(callback: types.CallbackQuery, state: FSMContext):

    db = next(get_db())
    user = get_or_create_user(db, telegram_id=callback.from_user.id)
    data = await state.get_data()
    amount_id = data.get("amount_id")

    if not amount_id:
        await callback.answer(t("INVALID_SELECTION", callback), show_alert=True)
        return

    with get_session() as session:
        amount = session.query(Amount).filter_by(id=amount_id).first()

        if not amount:
            await callback.answer(t("NO_SUCH_AMOUNT", callback), show_alert=True)
            return

        if hasattr(amount, "stock") and amount.stock is not None and amount.stock < 1:
            await callback.answer(t("OUT_OF_STOCK", callback), show_alert=True)
            return

        if not deduct_balance(session, user, amount.price):
            await callback.answer(t("INSUFFICIENT_FUNDS", callback), show_alert=True)
            return

        purchase_text = f"{t('PURCHASE_SUCCESS', callback)}\n\n{amount.purchase_info or ''}"
        add_purchase(session, user.id, amount.id, purchase_text)

        if amount.image_file_id:
            await callback.message.answer_photo(
                photo=amount.image_file_id,
                caption=purchase_text
            )
        else:
            await callback.message.answer(purchase_text)

        await state.clear()

@router.message(F.text.in_(get_menu_button_values("add_funds")))
async def handle_add_funds(message: types.Message):
    db = next(get_db())
    user = get_or_create_user(db, telegram_id=message.from_user.id)

    builder = InlineKeyboardBuilder()
    for amount in [5, 10, 25, 50]:
        builder.button(
            text=f"Add ${amount}",
            callback_data=f"add_funds:{amount}"
        )

    await message.answer("Choose amount:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("add_funds:"))
async def handle_invoice(callback: types.CallbackQuery):
    amount = float(callback.data.split(":")[1])
    link = create_invoice(amount, metadata={"telegram_id": callback.from_user.id})
    await callback.message.edit_text(f"💵 Please pay:\n{link}")
