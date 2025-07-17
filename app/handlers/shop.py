# handlers/shop.py
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session
from app.database import get_db, get_session
from app.utils.helpers import get_or_create_user, get_cities, get_products_by_city
from app.keyboards.common import get_menu_button_values, back_main_menu_buttons
from app.models import City, Product, Area, Amount
from app.states.shop import ShopState
from app.utils.texts import t

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
        await message.answer(t("NO_CITIES", message))
        return
    buttons = [{"label": city.name, "data": f"city:{city.id}"} for city in cities]
    await state.set_state(ShopState.city)
    await message.answer(t("CHOOSE_CITY", message), reply_markup=create_inline_keyboard(buttons))

@router.callback_query(F.data == "back_to_cities")
async def back_to_cities(callback: CallbackQuery, state: FSMContext):
    await start_shopping(callback.message, state)

@router.callback_query(F.data.startswith("city:"))
async def choose_city(callback: CallbackQuery, state: FSMContext):
    city_id = int(callback.data.split(":")[1])
    await state.update_data(city_id=city_id)
    with get_session() as db:
        products = db.query(Product).filter_by(city_id=city_id).all()
    if not products:
        await callback.message.edit_text(t("NO_PRODUCTS", callback), reply_markup=create_inline_keyboard([
            {"label": t("BACK", callback), "data": "back_to_cities"}
        ]))
        return
    buttons = [{"label": f"{p.name}", "data": f"product:{p.id}"} for p in products]
    buttons.append({"label": t("BACK", callback), "data": "back_to_cities"})
    await state.set_state(ShopState.product)
    await callback.message.edit_text(t("CHOOSE_PRODUCT", callback), reply_markup=create_inline_keyboard(buttons))

@router.callback_query(F.data == "back_to_products")
async def back_to_products(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    city_id = data.get("city_id")
    with get_session() as db:
        products = db.query(Product).filter_by(city_id=city_id).all()
    buttons = [{"label": f"{p.name}", "data": f"product:{p.id}"} for p in products]
    buttons.append({"label": t("BACK", callback), "data": "back_to_cities"})
    await state.set_state(ShopState.product)
    await callback.message.edit_text(t("CHOOSE_PRODUCT", callback), reply_markup=create_inline_keyboard(buttons))

@router.callback_query(F.data.startswith("product:"))
async def choose_product(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split(":")[1])
    data = await state.get_data()
    city_id = data.get("city_id")
    if not city_id:
        await callback.message.edit_text(t("ERROR_NO_CITY", callback))
        return
    await state.update_data(product_id=product_id)
    with get_session() as db:
        areas = db.query(Area).filter_by(product_id=product_id).all()
    if not areas:
        await callback.message.edit_text(t("NO_AREAS", callback), reply_markup=create_inline_keyboard([
            {"label": t("BACK", callback), "data": "back_to_products"},
            {"label": t("MAIN_MENU", callback), "data": "shopping"}
        ]))
        return
    buttons = [{"label": a.name, "data": f"area:{a.id}"} for a in areas]
    buttons.append({"label": t("BACK", callback), "data": "back_to_products"})
    buttons.append({"label": t("MAIN_MENU", callback), "data": "back_to_cities"})
    await state.set_state(ShopState.area)
    await callback.message.edit_text(t("CHOOSE_AREA", callback), reply_markup=create_inline_keyboard(buttons))

@router.callback_query(F.data.startswith("area:"))
async def choose_area(callback: CallbackQuery, state: FSMContext):
    area_id = int(callback.data.split(":")[1])
    await state.update_data(area_id=area_id)
    with get_session() as db:
        area = db.query(Area).filter_by(id=area_id).first()
        if not area:
            await callback.message.edit_text(t("AREA_NOT_FOUND", callback))
            return
        amounts = db.query(Amount).filter_by(area_id=area_id).all()
    if not amounts:
        await callback.message.edit_text(t("NO_AMOUNTS", callback), reply_markup=create_inline_keyboard([
            {"label": t("BACK", callback), "data": "back_to_products"},
            {"label": t("MAIN_MENU", callback), "data": "shopping"}
        ]))
        return
    buttons = [{"label": f"{amt.label} - {amt.price}€", "data": f"amount:{amt.id}"} for amt in amounts]
    buttons.append({"label": t("BACK", callback), "data": "back_to_areas"})
    buttons.append({"label": t("MAIN_MENU", callback), "data": "back_to_cities"})
    await state.set_state(ShopState.amount)
    await callback.message.edit_text(t("CHOOSE_AMOUNT", callback), reply_markup=create_inline_keyboard(buttons))

@router.callback_query(F.data == "back_to_areas")
async def back_to_areas(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("product_id")
    with get_session() as db:
        areas = db.query(Area).filter_by(product_id=product_id).all()
    if not areas:
        await callback.message.edit_text(t("NO_AREAS", callback))
        return
    buttons = [{"label": area.name, "data": f"area:{area.id}"} for area in areas]
    buttons.append({"label": t("BACK", callback), "data": "back_to_products"})
    buttons.append({"label": t("MAIN_MENU", callback), "data": "back_to_cities"})
    await state.set_state(ShopState.area)
    await callback.message.edit_text(t("CHOOSE_AREA", callback), reply_markup=create_inline_keyboard(buttons))

@router.callback_query(F.data.startswith("amount:"))
async def confirm_amount(callback: CallbackQuery, state: FSMContext):
    amount_id = int(callback.data.split(":")[1])
    data = await state.get_data()
    await state.update_data(amount_id=amount_id)
    with get_session() as db:
        amount = db.query(Amount).filter_by(id=amount_id).first()
    await state.clear()
    if not amount:
        await callback.message.answer(t("NO_SUCH_AMOUNT", callback))
        return
    msg_text = f"{t('PRODUCT_INFO', callback)}\n\n{amount.description}\n\n💶 Price: {amount.amount}€"
    buttons = [
        {"label": t("PAY_WITH_BALANCE", callback), "data": "pay_balance"},
        {"label": t("BACK", callback), "data": "back_to_amounts"},
        {"label": t("MAIN_MENU", callback), "data": "back_to_cities"},
    ]
    await state.set_state(ShopState.confirm)
    if amount.image_file_id:
        await callback.message.answer_photo(
            photo=amount.image_file_id,
            caption=msg_text,
            reply_markup=create_inline_keyboard(buttons)
        )
    else:
        await callback.message.answer(
            msg_text,
            reply_markup=create_inline_keyboard(buttons)
        )

@router.callback_query(F.data == "back_to_amounts")
async def back_to_amounts(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    area_id = data.get("area_id")
    with get_session() as db:
        amounts = db.query(Amount).filter_by(area_id=area_id).all()
    buttons = [{"label": f"{amt.amount}€", "data": f"amount:{amt.id}"} for amt in amounts]
    buttons.append({"label": t("BACK", callback), "data": "back_to_areas"})
    buttons.append({"label": t("MAIN_MENU", callback), "data": "back_to_cities"})
    await state.set_state(ShopState.amount)
    await callback.message.edit_text(t("CHOOSE_AMOUNT", callback), reply_markup=create_inline_keyboard(buttons))
