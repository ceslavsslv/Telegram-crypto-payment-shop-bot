# handlers/payment.py
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database import get_db
from app.utils.helpers import get_or_create_user, get_product, deduct_balance, add_purchase
from app.utils.btc import create_invoice

router = Router()

@router.callback_query(F.data.startswith("buy:"))
async def handle_buy(callback: types.CallbackQuery):
    product_id = int(callback.data.split(":")[1])
    db = next(get_db())
    user = get_or_create_user(db, telegram_id=callback.from_user.id)
    product = get_product(db, product_id)

    if not product or product.stock < 1:
        await callback.answer("Product unavailable.", show_alert=True)
        return

    builder = InlineKeyboardBuilder()
    builder.button(text="💳 Buy by Balance", callback_data=f"buy_balance:{product.id}")
    builder.button(text="⬅️ Back", callback_data="shop")
    builder.button(text="⏮️ Back to Start", callback_data="start")

    text = f"<b>{product.name}</b>\n\n{product.description}\n\nPrice: ${product.price}"
    await callback.message.edit_text(text, reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("buy_balance:"))
async def handle_balance_purchase(callback: types.CallbackQuery):
    db = next(get_db())
    user = get_or_create_user(db, telegram_id=callback.from_user.id)
    product_id = int(callback.data.split(":")[1])
    product = get_product(db, product_id)

    if not product:
        await callback.answer("Product not found.", show_alert=True)
        return

    if not deduct_balance(db, user, product.price):
        await callback.answer("Insufficient balance.", show_alert=True)
        return

    # In real use, you'd assign a product license/code or delivery info
    info = f"You purchased: {product.name}\nFind your item here: [link or code]"
    add_purchase(db, user.id, product.id, info)

    await callback.message.edit_text(f"✅ Purchase successful!\n\n{info}")

@router.message(F.text == "💶 Add funds")
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
