# handlers/admin.py
import re
from aiogram import Router, types, F, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, Filter
from sqlalchemy.orm import Session, joinedload
from app.states.admin import AdminState
from app.config import ADMINS
from app.database import engine, get_session
from app.models import Base, City, Product, Area, Amount, User, Purchase, StockItem
from app.keyboards.admin_menu import get_admin_keyboard
from sqlalchemy import func


class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS
    
router = Router()
router.message.filter(IsAdmin())


def is_admin(user_id: int) -> bool:
    return user_id in ADMINS

@router.message(Command("admin"))
async def admin_panel(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        await message.answer("Access denied.")
        return

    await state.set_state(AdminState.choose_action)
    await message.answer("👤 Welcome Admin. Choose action:", reply_markup=get_admin_keyboard())

@router.message(Command("syncdb"))
async def sync_db(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Access denied.")
        return

    Base.metadata.create_all(bind=engine)
    await message.answer("✅ Database tables created.")

@router.message(F.text == "❌ Cancel")
async def cancel_admin_action(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Action canceled. Back to main menu.", reply_markup=get_admin_keyboard())
    await state.set_state(AdminState.choose_action)

@router.message(AdminState.choose_action, F.text == "⬅️ Exit Admin")
async def exit_admin_panel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("👋 Exited admin mode.", reply_markup=ReplyKeyboardRemove())

#new Add city flow

@router.message(AdminState.choose_action, F.text == "➕ Add City")
async def add_city_prompt(message: Message, state: FSMContext):
    await message.answer("🏙 Enter city name:", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.city_name)

@router.message(AdminState.city_name)
async def add_city_save(message: Message, state: FSMContext):
    city_name = message.text.strip()
    with get_session() as db:
        existing = db.query(City).filter(City.name == city_name).first()
        if existing:
            await message.answer("⚠️ City already exists.")
        else:
            db.add(City(name=city_name, is_active=True))
            db.commit()
            await message.answer("✅ City added.")
    await state.set_state(AdminState.choose_action)
    await message.answer("✅ City added.", reply_markup=get_admin_keyboard())

# ➕ Add Product Flow

@router.message(AdminState.choose_action, F.text == "➕ Add Product")
async def add_product_prompt_city(message: Message, state: FSMContext):
    with get_session() as db:
        cities = db.query(City).all()
    if not cities:
        await message.answer("❌ No cities found. Add a city first.")
        return
    msg = "Select city ID:\n" + "\n".join(f"{c.id}. {c.name}" for c in cities)
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.product_city)

@router.message(AdminState.product_city)
async def add_product_prompt_name(message: Message, state: FSMContext):
    try:
        city_id=int(message.text)
    except ValueError:
        await message.answer("❌ Invalid city ID. Please enter a number.")
        return
    await state.update_data(city_id=city_id)
    await message.answer("📝 Enter product name:", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.product_name)

@router.message(AdminState.product_name)
async def add_product_save(message: Message, state: FSMContext):
    data = await state.get_data()
    with get_session() as db:
        db.add(Product(name=message.text.strip(), city_id=data["city_id"]))
        db.commit()
    await state.clear()
    await message.answer("✅ Product added.", reply_markup=get_admin_keyboard())
    await state.set_state(AdminState.choose_action)

#new ➕ Add Area Flow
@router.message(AdminState.choose_action, F.text == "➕ Add Area")
async def admin_add_area_choose_city(message: Message, state: FSMContext):
    with get_session() as db:
        cities = db.query(City).all()
    if not cities:
        await message.answer("❌ No cities found.")
        return
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=city.name)] for city in cities] + [[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    )
    await message.answer("🏙 Select a city:", reply_markup=keyboard)
    await state.set_state(AdminState.add_area_city_chosen)

@router.message(AdminState.add_area_city_chosen)
async def add_area_prompt_product(message: Message, state: FSMContext):
    city_name = message.text.strip()
    with get_session() as db:
        city = db.query(City).filter_by(name=city_name).first()
        if not city:
            await message.answer("❌ City not found.")
            return
        await state.update_data(city_id=city.id)
        products = db.query(Product).filter_by(city_id=city.id).all()
    if not products:
        await message.answer("❌ No products in this city.")
        return
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=f"{p.name} (#{p.id})")] for p in products] + [[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    )
    await message.answer("🛒 Select product ID:", reply_markup=keyboard)
    await state.set_state(AdminState.area_product)

@router.message(AdminState.area_product)
async def add_area_prompt_name(message: Message, state: FSMContext):
    try:
        product_id = int(re.search(r"#(\d+)", message.text).group(1))
    except ValueError:
        await message.answer("❌ Invalid product ID. Please enter a number.")
        return
    await state.update_data(product_id=product_id)
    await message.answer("📝 Enter area/district name:", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.area_name)

@router.message(AdminState.area_name)
async def add_area_save(message: Message, state: FSMContext):
    data = await state.get_data()
    with get_session() as db:
        db.add(Area(name=message.text.strip(), product_id=data["product_id"]))
        db.commit()
    await state.clear()
    await message.answer("✅ Area added.", reply_markup=get_admin_keyboard())
    await state.set_state(AdminState.choose_action)

# ➕ Add Amount Flow

@router.message(AdminState.choose_action, F.text == "➕ Add Amount")
async def admin_add_amount_choose_city(message: Message, state: FSMContext):
    with get_session() as db:
        cities = db.query(City).all()
    if not cities:
        await message.answer("❌ No cities available.")
        return
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=city.name)] for city in cities] + [[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    )
    await message.answer("🏙 Choose a city:", reply_markup=keyboard)
    await state.set_state(AdminState.add_amount_city_chosen)

@router.message(AdminState.add_amount_city_chosen)
async def add_amount_prompt_area(message: Message, state: FSMContext):
    city_name = message.text.strip()
    with get_session() as db:
        city = db.query(City).filter_by(name=city_name).first()
        if not city:
            await message.answer("❌ City not found.")
            return
        areas = db.query(Area).join(Product).filter(Product.city_id == city.id).all()
    if not areas:
        await message.answer("❌ No areas found. Add an area first.")
        return
    await state.update_data(city_id=city.id)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=f"{a.name} (#{a.id})")] for a in areas] + [[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    )
    await message.answer("📍 Select area ID:", reply_markup=keyboard)
    await state.set_state(AdminState.amount_area)

@router.message(AdminState.amount_area)
async def add_amount_prompt_label(message: Message, state: FSMContext):
    try:
        area_id = int(re.search(r"#(\d+)", message.text).group(1))
    except:
        await message.answer("❌ Invalid area ID. Please enter a number.")
        return
    await state.update_data(area_id=area_id)
    await message.answer("📝 Enter amount label (1peace, 0.5KG, etc.):", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.amount_label)  

@router.message(AdminState.amount_label)
async def add_amount_prompt_price(message: Message, state: FSMContext):
    await state.update_data(label=message.text.strip())
    await message.answer("💰 Enter price (EUR):", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]], resize_keyboard=True
    ))
    await state.set_state(AdminState.amount_price)

@router.message(AdminState.amount_price)
async def add_amount_save(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        price = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("❌ Invalid price. Please enter a numeric value.")
        return
    with get_session() as db:
        db.add(Amount(area_id=data["area_id"], label=data["label"], price=price))
        db.commit()
    await state.clear()
    await message.answer("✅ Amount added.", reply_markup=get_admin_keyboard())
    await state.set_state(AdminState.choose_action)

@router.message(F.text == "📝 Edit Purchase Info")
async def edit_purchase_note(message: Message, state: FSMContext):
    msg = "Send the purchase info you'd like to set (this will show after a purchase)."
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.edit_purchase_note)

@router.message(AdminState.edit_purchase_note)
async def save_note(message: types.Message, state: FSMContext):
    data = await state.get_data()
    amount_id = data.get("amount_id")
    with get_session() as db:
        amount = db.query(Amount).filter_by(id=amount_id).first()
        if amount:
            amount.purchase_note = message.text
            db.commit()
    await state.clear()
    await message.answer("✅ Saved post-purchase message.")

@router.message(AdminState.choose_action, F.text == "💰 Edit Balance")
async def ask_balance_user_id(message: Message, state: FSMContext):
    msg = "Enter User ID to change balance:"
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.balance_user_id)

@router.message(AdminState.balance_user_id)
async def ask_balance_amount(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
    except ValueError:
        await message.answer("❌ Invalid User ID. Must be a number.")
        return
    await state.update_data(user_id=user_id)
    await message.answer("Enter amount to add (negative to subtract):", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]], resize_keyboard=True
    ))
    await state.set_state(AdminState.balance_amount)

@router.message(AdminState.balance_amount)
async def update_user_balance(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("❌ Invalid amount. Please enter a number.")
        return
    data = await state.get_data()
    user_id = data.get("user_id")
    with get_session() as db:
        user = db.query(User).filter_by(telegram_id=user_id).first()
        if not user:
            await message.answer("❌ User not found.")
        else:
            user.balance += amount
            db.commit()
            await message.answer(f"✅ Updated balance by {amount:+.2f}. New: ${user.balance:.2f}")
    await state.set_state(AdminState.choose_action)

@router.message(AdminState.choose_action, F.text == "🔍 Lookup User")
async def lookup_user_prompt(message: Message, state: FSMContext):
    msg = "Enter Telegram User ID to lookup:"
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.lookup_user)

@router.message(AdminState.lookup_user)
async def lookup_user_data(message: Message, state: FSMContext):
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Invalid User ID. Please enter a numeric Telegram ID.")
        return
    with get_session() as db:
        user = db.query(User).filter_by(telegram_id=user_id).first()
        if not user:
            await message.answer("❌ User not found.")
            return
        msg = f"👤 User ID: <code>{user.id}</code>\n"
        msg += f"💰 Balance: {user.balance:.2f}€\n"
        msg += f"🕐 Registered: {user.created_at.strftime('%Y-%m-%d')}"
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📊 View Purchases"), KeyboardButton(text="💳 Edit Balance")],
                [KeyboardButton(text="✅ Done")]
            ], resize_keyboard=True
        )
        await state.update_data(user_id=user.id)
        await message.answer(msg, parse_mode="HTML", reply_markup=keyboard)
        await state.set_state(AdminState.confirm_view_purchases)
        
@router.message(AdminState.confirm_view_purchases)
async def admin_view_user_purchases_by_state(message: Message, state: FSMContext):
    text = message.text.strip()
    if text == "✅ Done":
        await state.clear()
        await message.answer("✅ Back to admin menu.", reply_markup=get_admin_keyboard())
        await state.set_state(AdminState.choose_action)
        return
    if text == "📊 View Purchases":
        data = await state.get_data()
        user_id = data.get("user_id")
        if not user_id:
            await message.answer("⚠️ No user selected.")
            return
        with get_session() as db:
            purchases = db.query(Purchase).options(joinedload(Purchase.amount)).filter_by(user_id=user_id).order_by(Purchase.timestamp.desc()).limit(10).all()
            total_spent = db.query(func.sum(Amount.price)).join(Purchase).filter(Purchase.user_id == user_id).scalar() or 0.0
            if not purchases:
                await message.answer("ℹ️ This user has no purchases.")
            else:
                msg = f"📦 Last purchases for user {user_id}:\n"
                for p in purchases:
                    area = db.query(Area).filter_by(id=p.amount.area_id).first()
                    product = db.query(Product).filter_by(id=area.product_id).first() if area else None
                    city = db.query(City).filter_by(id=product.city_id).first() if product else None
                    city_name = city.name if city else "Unknown"
                    msg += f"\n🛒 <b>{p.amount.label}</b> - {p.amount.price}€\n📍 {area.name}, {city_name}\n🕐 {p.timestamp.strftime('%Y-%m-%d %H:%M')}\n"
                msg += f"\n💸 <b>Total Spent:</b> {total_spent:.2f}€"
                await message.answer(msg, parse_mode="HTML")
        return
    if text == "💳 Edit Balance":
        msg = "Enter User ID to change balance:"
        await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True))
        await state.set_state(AdminState.balance_user_id)
        return
    await message.answer("❌ Invalid option. Please choose a button.")

@router.message(AdminState.choose_action, F.text == "📦 View Stock")
async def view_stock_summary(message: Message, state: FSMContext):
    with get_session() as db:
        results = (
            db.query(StockItem.amount_id, func.count(StockItem.id))
            .group_by(StockItem.amount_id)
            .all()
        )
        if not results:
            await message.answer("📦 No stock items available.")
            return
        stock_data = {}
        for amount_id, count in results:
            amount = db.query(Amount).filter_by(id=amount_id).first()
            if not amount:
                continue
            area = db.query(Area).filter_by(id=amount.area_id).first()
            if not area:
                continue
            product = db.query(Product).filter_by(id=area.product_id).first()
            if not product:
                continue
            city = db.query(City).filter_by(id=product.city_id).first()
            if not city:
                continue
            city_name = city.name
            area_name = area.name
            amount_label = amount.label
            stock_data.setdefault(city_name, {})
            stock_data[city_name].setdefault(area_name, {})
            stock_data[city_name][area_name][amount_label] = count
        text = "📦 Available Stock:\n"
        for city, areas in stock_data.items():
            text += f"\n🏙 City: {city}\n"
            for area, amounts in areas.items():
                text += f"  🌍 Area: {area}\n"
                for amount_label, count in amounts.items():
                    text += f"    📏 {amount_label}: {count} item(s)\n"
        await message.answer(text)
    await state.set_state(AdminState.choose_action)

@router.message(AdminState.choose_action, F.text == "📊 Bot Stats")
async def show_bot_stats(message: Message, state: FSMContext):
    with get_session() as db:
        total_purchases = db.query(func.count(Purchase.id)).scalar() or 0
        total_revenue = db.query(func.sum(Purchase.total_price)).scalar() or 0.0
        total_users = db.query(func.count(User.id)).scalar() or 0
        total_products = db.query(func.count(Product.id)).scalar() or 0
        top_amounts = (
            db.query(Purchase.amount_id, func.count(Purchase.id).label("cnt"))
            .group_by(Purchase.amount_id)
            .order_by(func.count(Purchase.id).desc())
            .limit(5)
            .all()
        )
        response = f"📊 <b>Bot Statistics</b>\n"
        response += f"🧾 Total purchases: <b>{total_purchases}</b>\n"
        response += f"💶 Total revenue: <b>{total_revenue:.2f}€</b>\n"
        response += f"👤 Total users: <b>{total_users}</b>\n"
        response += f"📦 Total products: <b>{total_products}</b>\n"
        if top_amounts:
            response += "\n🏆 <b>Top Purchased Amounts:</b>\n"
            for amount_id, count in top_amounts:
                amount = db.query(Amount).filter_by(id=amount_id).first()
                label = amount.label if amount else f"ID {amount_id}"
                response += f"• {label}: {count}x\n"
    await message.answer(response, parse_mode="HTML")
    await state.set_state(AdminState.choose_action)

@router.message(AdminState.choose_action, F.text == "🗑 Remove City")
async def remove_city_prompt(message: Message, state: FSMContext):
    with get_session() as db:
        cities = db.query(City).all()
    if not cities:
        await message.answer("⚠️ No cities found.")
        return
    msg = "📋 Enter city ID to remove:\n" + "\n".join(f"{c.id}. {c.name}" for c in cities)
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.remove_city)

@router.message(AdminState.remove_city)
async def remove_city_execute(message: Message, state: FSMContext):
    try:
        city_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Invalid ID. Please enter a number.")
        return
    with get_session() as db:
        city = db.query(City).filter_by(id=city_id).first()
        if city:
            db.delete(city)
            db.commit()
            await message.answer("✅ City removed.")
        else:
            await message.answer("❌ City not found.")
    await state.set_state(AdminState.choose_action)
    await message.answer("↩️ Back to menu.", reply_markup=get_admin_keyboard())

@router.message(AdminState.choose_action, F.text == "🗑 Remove Product")
async def remove_product_prompt(message: Message, state: FSMContext):
    with get_session() as db:
        products = db.query(Product).all()
    if not products:
        await message.answer("⚠️ No products found.")
        return
    msg = "📋 Enter product ID to remove:\n"
    for p in products:
        city = db.query(City).filter_by(id=p.city_id).first() if p else None
        city_label = city.name if city else "Unknown"
        msg += f"{p.id}. {p.name} (City: {city_label})\n"
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.remove_product)

@router.message(AdminState.remove_product)
async def remove_product_execute(message: Message, state: FSMContext):
    try:
        product_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Invalid ID. Please enter a number.")
        return
    with get_session() as db:
        product = db.query(Product).filter_by(id=product_id).first()
        if product:
            db.delete(product)
            db.commit()
            await message.answer("✅ Product removed.")
        else:
            await message.answer("❌ Product not found.")
    await state.set_state(AdminState.choose_action)
    await message.answer("↩️ Back to menu.", reply_markup=get_admin_keyboard())

@router.message(AdminState.choose_action, F.text == "🗑 Remove Area")
async def remove_area_prompt(message: Message, state: FSMContext):
    with get_session() as db:
        areas = db.query(Area).all()
    if not areas:
        await message.answer("⚠️ No areas found.")
        return
    msg = "📋 Enter area ID to remove:\n"
    for a in areas:
        product = db.query(Product).filter_by(id=a.product_id).first() if a else None
        city = db.query(City).filter_by(id=product.city_id).first() if product else None
        city_label = city.name if city else "Unknown"
        msg += f"{a.id}. {a.name} (City: {city_label})\n"
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.remove_area)

@router.message(AdminState.remove_area)
async def remove_area_execute(message: Message, state: FSMContext):
    try:
        area_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Invalid ID. Please enter a number.")
        return
    with get_session() as db:
        area = db.query(Area).filter_by(id=area_id).first()
        if area:
            db.delete(area)
            db.commit()
            await message.answer("✅ Area removed.")
        else:
            await message.answer("❌ Area not found.")
    await state.set_state(AdminState.choose_action)
    await message.answer("↩️ Back to menu.", reply_markup=get_admin_keyboard())

@router.message(AdminState.choose_action, F.text == "🗑 Remove Amount")
async def remove_amount_prompt(message: Message, state: FSMContext):
    with get_session() as db:
        amounts = db.query(Amount).all()
    if not amounts:
        await message.answer("⚠️ No amounts found.")
        return
    msg = "📋 Enter amount ID to remove:\n"
    for a in amounts:
        area = db.query(Area).filter_by(id=a.area_id).first()
        product = db.query(Product).filter_by(id=area.product_id).first() if area else None
        city = db.query(City).filter_by(id=product.city_id).first() if product else None
        area_name = area.name if area else "Unknown"
        city_label = city.name if city else "Unknown"
        msg += f"{a.id}. {a.price}€ (Location: {area_name}, {city_label})\n"
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.remove_amount)

@router.message(AdminState.remove_amount)
async def remove_amount_execute(message: Message, state: FSMContext):
    try:
        amount_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Invalid ID. Please enter a number.")
        return

    with get_session() as db:
        amount = db.query(Amount).filter_by(id=amount_id).first()
        if amount:
            db.delete(amount)
            db.commit()
            await message.answer("✅ Amount removed.")
            await state.set_state(AdminState.choose_action)
        else:
            await message.answer("❌ Amount not found.")
    await state.set_state(AdminState.choose_action)

@router.message(AdminState.choose_action, F.text == "🖼 Set Amount Image")
async def admin_start_edit_image(message: Message, state: FSMContext):
    with get_session() as db:
        amounts = db.query(Amount).all()
    if not amounts:
        await message.answer("⚠️ No amounts available.")
        return
    msg = "🖼 Select amount to upload an image:\n"
    for a in amounts:
        area = db.query(Area).filter_by(id=a.area_id).first()
        product = db.query(Product).filter_by(id=area.product_id).first() if area else None
        city = db.query(City).filter_by(id=product.city_id).first() if product else None
        area_name = area.name if area else "Unknown"
        city_label = city.name if city else "Unknown"
        msg += f"{a.id}. {a.label} ({a.price}€) – (Area: {area_name}, {city_label})\n"
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.edit_amount_image)

@router.message(AdminState.edit_amount_image)
async def admin_upload_image(message: Message, state: FSMContext):
    try:
        amount_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Invalid amount ID. Please enter a number.")
        return
    await state.update_data(amount_id=amount_id)
    await message.answer("📸 Now send the photo to use for this amount:", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]], resize_keyboard=True
    ))
    await state.set_state(AdminState.edit_amount_select)

@router.message(AdminState.edit_amount_select, F.photo)
async def admin_save_amount_image(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("❌ Please send an actual photo.")
        return
    data = await state.get_data()
    amount_id = data.get("amount_id")
    file_id = message.photo[-1].file_id
    with get_session() as db:
        amount = db.query(Amount).filter_by(id=amount_id).first()
        if amount:
            amount.image_file_id = file_id
            db.commit()
    await message.answer("✅ Image saved for this amount.", reply_markup=get_admin_keyboard())
    await state.set_state(AdminState.choose_action)

@router.message(AdminState.choose_action, F.text == "✏️ Set Amount Description")
async def admin_start_edit_description(message: Message, state: FSMContext):
    with get_session() as db:
        amounts = db.query(Amount).all()
    if not amounts:
        await message.answer("⚠️ No amounts available.")
        return
    msg = "✏️ Select amount to edit its description:\n"
    for a in amounts:
        area = db.query(Area).filter_by(id=a.area_id).first()
        product = db.query(Product).filter_by(id=area.product_id).first() if area else None
        city = db.query(City).filter_by(id=product.city_id).first() if product else None
        area_name = area.name if area else "Unknown"
        city_label = city.name if city else "Unknown"
        msg += f"{a.id}. {a.label} ({a.price}€) – (Area ID: {area_name}, {city_label})\n"
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]], resize_keyboard=True
    ))
    await state.set_state(AdminState.edit_amount_description)

@router.message(AdminState.edit_amount_description)
async def admin_enter_description(message: Message, state: FSMContext):
    try:
        amount_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Invalid amount ID.")
        return
    await state.update_data(amount_id=amount_id)
    await message.answer("✏️ Enter description text:", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]], resize_keyboard=True
    ))
    await state.set_state(AdminState.edit_amount_description_write)

@router.message(AdminState.edit_amount_description_write)
async def admin_save_description(message: Message, state: FSMContext):
    data = await state.get_data()
    amount_id = data.get("amount_id")
    text = message.text.strip()
    with get_session() as db:
        amount = db.query(Amount).filter_by(id=amount_id).first()
        if amount:
            amount.description = text
            db.commit()
    await state.clear()
    await message.answer("✅ Description updated.", reply_markup=get_admin_keyboard())
    await state.set_state(AdminState.choose_action)

@router.message(AdminState.choose_action, F.text == "📝 Add stock")
async def admin_start_delivery_note(message: Message, state: FSMContext):
    with get_session() as db:
        amounts = db.query(Amount).all()
    if not amounts:
        await message.answer("⚠️ No amounts available.")
        return
    msg = "📝 Select amount to edit its delivery note:\n"
    for a in amounts:
        area = db.query(Area).filter_by(id=a.area_id).first()
        product = db.query(Product).filter_by(id=area.product_id).first() if area else None
        city = db.query(City).filter_by(id=product.city_id).first() if product else None
        area_name = area.name if area else "Unknown"
        city_label = city.name if city else "Unknown"
        msg += f"{a.id}. {a.label} ({a.price}€) – (Area: {area_name}, {city_label})\n"
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]], resize_keyboard=True
    ))
    await state.set_state(AdminState.edit_amount_note)

@router.message(AdminState.edit_amount_note)
async def admin_save_note(message: Message, state: FSMContext):
    try:
        amount_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Invalid amount ID.")
        return
    await state.update_data(amount_id=amount_id, photos=[])
    await message.answer("📸 Send one or more delivery photos. Then type your note. When done, send ✅ Done.", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✅ Done")], [KeyboardButton(text="❌ Cancel")]], resize_keyboard=True
    ))
    await state.set_state(AdminState.edit_delivery_step)

@router.message(AdminState.edit_delivery_step, F.photo)
async def admin_collect_delivery_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get("photos", [])
    photos.append(message.photo[-1].file_id)
    await state.update_data(photos=photos)
    await message.answer("📎 Photo saved. Send more or press ✅ Done.")

@router.message(AdminState.edit_delivery_step, F.text == "✅ Done")
async def admin_finish_delivery_note(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data.get("photos"):
        await message.answer("⚠️ Please send at least one photo before continuing.")
        return
    await message.answer("📝 Now enter delivery note (description, instructions, etc.):")
    await state.set_state(AdminState.save_delivery_note)

@router.message(AdminState.save_delivery_note)
async def admin_save_delivery_note(message: Message, state: FSMContext):
    note = message.text.strip()
    if not note:
        await message.answer("⚠️ Note cannot be empty. Please enter it:")
        return
    await state.update_data(note=note)
    await message.answer("📍 Now enter delivery location (or type - to leave empty):")
    await state.set_state(AdminState.save_delivery_location)

@router.message(AdminState.save_delivery_location)
async def admin_save_delivery_location(message: Message, state: FSMContext):
    location = message.text.strip()
    if not location:
        await message.answer("⚠️ Location cannot be empty. Please enter it:")
        return
    data = await state.get_data()
    note = data.get("note")
    photos = data.get("photos", [])
    amount_id = data.get("amount_id")
    if not (amount_id and photos and note and location):
        await message.answer("❌ Missing required data to save item.")
        return
    with get_session() as db:
        stock_item = StockItem(
            amount_id=amount_id,
            note=note,
            location=location,
            photos=",".join(photos)
        )
        db.add(stock_item)
        db.commit()
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="➕ Add Another Item"), KeyboardButton(text="✅ Done")]], resize_keyboard=True
    )
    await message.answer("✅ Stock item saved. Add another or finish?", reply_markup=keyboard)
    await state.set_state(AdminState.ask_add_another_item)

@router.message(AdminState.ask_add_another_item)
async def admin_handle_add_another_item(message: Message, state: FSMContext):
    if message.text == "➕ Add Another Item":
        await state.update_data(photos=[])
        await message.answer("📸 Send one or more delivery photos for the item. When done, send ✅ Done.", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="✅ Done"), KeyboardButton(text="❌ Cancel")]], resize_keyboard=True
        ))
        await state.set_state(AdminState.edit_delivery_step)
    else:
        await message.answer("✅ All stock items saved.", reply_markup=get_admin_keyboard())
        await state.clear()
        await state.set_state(AdminState.choose_action)   

@router.message(AdminState.choose_action, F.text == "♻️ Remove Image/Note")
async def admin_start_removal(message: Message, state: FSMContext):
    with get_session() as db:
        amounts = db.query(Amount).all()
    if not amounts:
        await message.answer("⚠️ No amounts available.")
        return
    msg = "♻️ Select amount to remove a field:\n"
    for a in amounts:
        area = db.query(Area).filter_by(id=a.area_id).first()
        product = db.query(Product).filter_by(id=area.product_id).first() if area else None
        city = db.query(City).filter_by(id=product.city_id).first() if product else None
        area_name = area.name if area else "Unknown"
        city_label = city.name if city else "Unknown"
        msg += f"{a.id}. {a.label} ({a.price}€) – (Area: {area_name}, {city_label})\n"
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]], resize_keyboard=True
    ))
    await state.set_state(AdminState.edit_amount_remove_option)

@router.message(AdminState.edit_amount_remove_option)
async def admin_choose_removal_field(message: Message, state: FSMContext):
    try:
        amount_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Invalid amount ID.")
        return
    await state.update_data(amount_id=amount_id)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🖼 Image"), KeyboardButton(text="✏️ Description")],
            [KeyboardButton(text="♻️ Remove Stock Item")],
            [KeyboardButton(text="❌ Cancel")]
        ], resize_keyboard=True
    )
    await message.answer("What would you like to remove from this amount?", reply_markup=keyboard)
    await state.set_state(AdminState.edit_amount_remove_choice)

@router.message(AdminState.edit_amount_remove_choice)
async def admin_execute_removal_choice(message: Message, state: FSMContext):
    choice = message.text.strip()
    data = await state.get_data()
    amount_id = data.get("amount_id")
    with get_session() as db:
        amount = db.query(Amount).filter_by(id=amount_id).first()
        if not amount:
            await message.answer("⚠️ Amount not found.")
            return
        if choice == "🖼 Image":
            amount.image_file_id = None
            db.commit()
            await message.answer("✅ Removed image.", reply_markup=get_admin_keyboard())
        elif choice == "✏️ Description":
            amount.description = ""
            db.commit()
            await message.answer("✅ Removed description.", reply_markup=get_admin_keyboard())
        elif choice == "♻️ Remove Stock Item":
            stock_items = db.query(StockItem).filter_by(amount_id=amount.id).all()
            if not stock_items:
                await message.answer("⚠️ No stock items found for this amount.")
                return
            for item in stock_items:
                caption = f"🧾 <b>StockItem ID:</b> {item.id}\n"
                caption += f"📍 Location: {item.location or 'N/A'}\n"
                caption += f"📝 Note: {item.note or 'N/A'}\n"
                photo_ids = item.photos.split(",") if item.photos else []
                if photo_ids:
                    media = [InputMediaPhoto(media=pid) for pid in photo_ids[:10]]
                    await message.answer_media_group(media)
                await message.answer(caption, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="❌ Remove this item", callback_data=f"remove_stock_{item.id}")]]
                ))
            return
        else:
            await message.answer("❌ Invalid option.")
            return
        await state.clear()
        await state.set_state(AdminState.choose_action)

@router.callback_query(F.data.startswith("remove_stock_"))
async def admin_execute_stockitem_removal(callback: CallbackQuery, state: FSMContext):
    stock_id = int(callback.data.split("_")[-1])
    with get_session() as db:
        item = db.query(StockItem).filter_by(id=stock_id).first()
        if not item:
            await callback.message.answer("❌ Stock item not found.")
        else:
            db.delete(item)
            db.commit()
            await callback.message.answer(f"✅ Stock item {stock_id} removed from inventory.")
    await callback.answer()
    await state.clear()
    await callback.message.answer("↩️ Back to admin menu.", reply_markup=get_admin_keyboard())
    await state.set_state(AdminState.choose_action)

@router.message(AdminState.choose_action, F.text == "📢 Announcement")
async def admin_start_announcement(message: Message, state: FSMContext):
    await message.answer("📨 Enter the message you want to send to all users:")
    await state.set_state(AdminState.enter_announcement)

@router.message(AdminState.enter_announcement)
async def admin_send_announcement(message: Message, state: FSMContext):
    text = message.text.strip()
    if not text:
        await message.answer("⚠️ Message cannot be empty.")
        return
    await message.answer("⏳ Sending announcement to all users...")
    success = 0
    with get_session() as db:
        users = db.query(User).all()
        for user in users:
            try:
                await message.bot.send_message(user.id, text)
                success += 1
            except:
                continue
    await message.answer(f"✅ Announcement sent to {success} users.", reply_markup=get_admin_keyboard())
    await state.clear()
    await state.set_state(AdminState.choose_action)

@router.message(AdminState.choose_action, F.text == "📢 Announcement")
async def admin_start_announcement(message: Message, state: FSMContext):
    await message.answer("📨 Enter the message you want to send to all users:")
    await state.set_state(AdminState.enter_announcement)

@router.message(AdminState.enter_announcement)
async def admin_send_announcement(message: Message, state: FSMContext):
    text = message.text.strip()
    if not text:
        await message.answer("⚠️ Message cannot be empty.")
        return
    await message.answer("⏳ Sending announcement to all users...")
    success = 0
    with get_session() as db:
        users = db.query(User).all()
        for user in users:
            try:
                await message.bot.send_message(user.id, text)
                success += 1
            except:
                continue
    await message.answer(f"✅ Announcement sent to {success} users.", reply_markup=get_admin_keyboard())
    await state.clear()
    await state.set_state(AdminState.choose_action)

@router.message(AdminState.choose_action, F.text == "👥 Referral")
async def admin_referral_stats(message: Message, state: FSMContext):
    with get_session() as db:
        total_with_referrals = db.query(func.count(User.id)).filter(User.referred_by != None).scalar()
        top_referrers = db.query(User.referred_by, func.count(User.id).label("count"))\
            .filter(User.referred_by != None)\
            .group_by(User.referred_by)\
            .order_by(func.count(User.id).desc())\
            .limit(10).all()
        msg = f"👥 Total referred users: {total_with_referrals}\n\n"
        msg += "🏆 Top Referrers:\n"
        for ref in top_referrers:
            msg += f"🔗 User ID: <code>{ref.referred_by}</code> — {ref.count} referrals\n"
        await message.answer(msg, parse_mode="HTML")
    await state.set_state(AdminState.choose_action)