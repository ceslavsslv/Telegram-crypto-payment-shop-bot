# handlers/shop.py
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.orm import Session
from app.database import get_db, get_session
from app.utils.helpers import get_or_create_user, get_cities, get_products_by_city
from app.keyboards.common import get_menu_button_values
from app.models import City, Product, Area, Amount

router = Router()

class ShopState(StatesGroup):
    city = State()
    product = State()
    area = State()
    amount = State()

def create_inline_keyboard(buttons):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn['label'], callback_data=btn['data'])] for btn in buttons
    ])

@router.message(F.text.in_(get_menu_button_values("shopping")))
async def handle_shop(message: types.Message):
    db = next(get_db())
    user = get_or_create_user(db, telegram_id=message.from_user.id)

    cities = get_cities(db)
    builder = InlineKeyboardBuilder()
    for city in cities:
        builder.button(text=city.name, callback_data=f"shop_city:{city.id}")

    await message.answer("Select your city:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("shop_city:"))
async def handle_city(callback: types.CallbackQuery):
    db = next(get_db())
    city_id = int(callback.data.split(":")[1])
    products = get_products_by_city(db, city_id)

    if not products:
        await callback.message.edit_text("No products available in this city.")
        return

    builder = InlineKeyboardBuilder()
    for product in products:
        builder.button(text=f"{product.name} - ${product.price}", callback_data=f"buy:{product.id}")

    await callback.message.edit_text("Select a product:", reply_markup=builder.as_markup())

#new

@router.message(F.text.lower() == "shopping")
async def start_shopping(message: Message, state: FSMContext):
    with get_session() as db:
        cities = db.query(City).filter_by(is_active=True).all()
    buttons = [{"label": city.name, "data": f"city:{city.id}"} for city in cities]
    await state.set_state(ShopState.city)
    await message.answer("🌆 Choose your city:", reply_markup=create_inline_keyboard(buttons))

@router.callback_query(F.data.startswith("city:"))
async def choose_city(callback: CallbackQuery, state: FSMContext):
    city_id = int(callback.data.split(":")[1])
    await state.update_data(city_id=city_id)
    with get_session() as db:
        products = db.query(Product).filter_by(city_id=city_id).all()
    buttons = [{"label": p.name, "data": f"product:{p.id}"} for p in products]
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
