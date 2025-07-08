# ---------------- bot.py ----------------
from dotenv import load_dotenv
import os

load_dotenv()  # This loads .env file into environment variables

API_TOKEN = os.getenv("API_TOKEN")

from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
from app.config import API_TOKEN
from app.database import init_db, get_user_balance, create_or_get_user

router = Router()
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.include_router(router)

# States
class ShopStates(StatesGroup):
    city = State()
    product = State()
    option = State()

# Start
@router.message(F.text == "/start")
async def start_cmd(message: Message, state: FSMContext):
    create_or_get_user(message.from_user.id)
    from keyboards.menu import main_menu_keyboard

    await message.answer("Welcome/Sveiciens!", reply_markup=main_menu_keyboard())

@router.message(F.text == "/shop")
async def choose_city(message: Message, state: FSMContext):
    from app.database import get_db
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM cities")
        cities = cur.fetchall()

    kb = InlineKeyboardBuilder()
    for city in cities:
        kb.button(text=city["name"], callback_data=f"city_{city['id']}")
    await message.answer("Choose a city:", reply_markup=kb.as_markup())

# Choose City
@router.callback_query(F.data.startswith("city_"))
async def select_city(callback: CallbackQuery, state: FSMContext):
    city_id = int(callback.data.split("_")[1])
    await state.update_data(city_id=city_id)

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM products WHERE city_id = ?", (city_id,))
        products = cur.fetchall()

    kb = InlineKeyboardBuilder()
    for product in products:
        kb.button(text=product["name"], callback_data=f"product_{product['id']}")
    kb.button(text="Back", callback_data="back_to_start")
    await callback.message.edit_text("Choose a product:", reply_markup=kb.as_markup())

# Choose Product
@router.callback_query(F.data.startswith("product_"))
async def select_product(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split("_")[1])
    await state.update_data(product_id=product_id)

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, amount, price FROM product_options WHERE product_id = ?", (product_id,))
        options = cur.fetchall()

    kb = InlineKeyboardBuilder()
    for opt in options:
        kb.button(text=f"{opt['amount']} - {opt['price']}$", callback_data=f"option_{opt['id']}")
    kb.button(text="Back", callback_data="back_to_start")
    await callback.message.edit_text("Choose amount:", reply_markup=kb.as_markup())

# Choose Option
@router.callback_query(F.data.startswith("option_"))
async def select_option(callback: CallbackQuery, state: FSMContext):
    option_id = int(callback.data.split("_")[1])
    from app.database import get_db, get_user_balance
    telegram_id = callback.from_user.id

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT price, amount FROM product_options WHERE id = ?", (option_id,))
        option = cur.fetchone()

    balance = get_user_balance(telegram_id)

    if balance < option["price"]:
        await callback.message.answer("❌ Insufficient balance. Use /topup to add funds.")
        return

    # Save order
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO orders (user_id, option_id, status) VALUES ((SELECT id FROM users WHERE telegram_id = ?), ?, 'paid')",
                    (telegram_id, option_id))
        cur.execute("UPDATE users SET balance = balance - ? WHERE telegram_id = ?", (option["price"], telegram_id))

    await callback.message.answer(f"✅ Purchase successful! You bought: {option['amount']}\nYou will receive instructions shortly.")
    await callback.message.answer("📦 Your product is available at our pickup point. Please check your email or Telegram shortly.")

# Run Bot
async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
