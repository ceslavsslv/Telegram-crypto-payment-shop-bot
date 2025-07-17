# handlers/shop.py
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session
from app.database import get_db, get_session
from app.utils.helpers import get_or_create_user, get_cities, get_products_by_city
from app.keyboards.common import get_menu_button_values
from app.models import City, Product, Area, Amount
from app.states.shop import ShopState
from app.utils import texts

router = Router()

def create_inline_keyboard(buttons):
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text=btn['label'], callback_data=btn['data'])] for btn in buttons
    ])

#new

@router.message(F.text.in_(get_menu_button_values("shopping")))
async def start_shopping(message: Message, state: FSMContext):
    with get_session() as db:
        cities = db.query(City).filter_by(is_active=True).all()
    if not cities:
        await message.answer(texts.NO_CITIES["en"])
        return
    buttons = [{"label": city.name, "data": f"city:{city.id}"} for city in cities]
    await state.set_state(ShopState.city)
    await message.answer(texts.CHOOSE_CITY["en"], reply_markup=create_inline_keyboard(buttons))

@router.callback_query(F.data.startswith("city:"))
async def choose_city(callback: CallbackQuery, state: FSMContext):
    city_id = int(callback.data.split(":")[1])
    await state.update_data(city_id=city_id)
    with get_session() as db:
        products = db.query(Product).filter_by(city_id=city_id).all()
    buttons = [{"label": f"{p.name}", "data": f"product:{p.id}"} for p in products]
    await state.set_state(ShopState.product)
    await callback.message.edit_text("🛍 Choose a product:", reply_markup=create_inline_keyboard(buttons))

@router.callback_query(F.data.startswith("product:"))
async def choose_product(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split(":")[1])
    await state.update_data(product_id=product_id)
    with get_session() as db:
        areas = db.query(Area).filter_by(product_id=product_id).all()
    buttons = [{"label": a.name, "data": f"area:{a.id}"} for a in areas]
    await state.set_state(ShopState.area)
    await callback.message.edit_text("📍 Choose an area/district:", reply_markup=create_inline_keyboard(buttons))

@router.callback_query(F.data.startswith("area:"))
async def choose_area(callback: CallbackQuery, state: FSMContext):
    area_id = int(callback.data.split(":")[1])
    await state.update_data(area_id=area_id)
    with get_session() as db:
        amounts = db.query(Amount).filter_by(area_id=area_id).all()
    buttons = [{"label": f"{amt.label} - {amt.price}€", "data": f"amount:{amt.id}"} for amt in amounts]
    await state.set_state(ShopState.amount)
    await callback.message.edit_text("💸 Choose amount:", reply_markup=create_inline_keyboard(buttons))

@router.callback_query(F.data.startswith("amount:"))
async def confirm_amount(callback: CallbackQuery, state: FSMContext):
    amount_id = int(callback.data.split(":")[1])
    data = await state.get_data()
    await state.clear()
    buttons = [
        {"label": "✅ Buy by Balance", "data": "buy"},
        {"label": "◀️ Back", "data": "back"},
        {"label": "🔙 Back to Start", "data": "shopping"}
    ]
    await callback.message.edit_text("✅ Confirm your purchase or navigate:", reply_markup=create_inline_keyboard(buttons))
