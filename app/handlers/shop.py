# handlers/shop.py
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database import get_db
from app.utils.helpers import get_or_create_user, get_cities, get_products_by_city
from app.keyboards.common import main_menu_keyboard, get_menu_button_values

router = Router()

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
