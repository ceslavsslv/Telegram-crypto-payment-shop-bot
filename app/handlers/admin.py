# handlers/admin.py
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from app.states.admin import AdminState
from app.config import ADMINS
from app.database import engine, get_session
from app.models import Base, City, Product, Area, Amount
from app.keyboards.admin_menu import get_admin_keyboard

router = Router()

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

#new Add city flow

@router.message(AdminState.choose_action, F.text == "➕ Add City")
async def add_city_prompt(message: Message, state: FSMContext):
    await message.answer("🏙 Enter city name:")
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

# ➕ Add Product Flow

@router.message(AdminState.choose_action, F.text == "➕ Add Product")
async def add_product_prompt_city(message: Message, state: FSMContext):
    with get_session() as db:
        cities = db.query(City).all()
    if not cities:
        await message.answer("❌ No cities found. Add a city first.")
        return
    msg = "Select city ID:\n" + "\n".join(f"{c.id}. {c.name}" for c in cities)
    await message.answer(msg)
    await state.set_state(AdminState.product_city)

@router.message(AdminState.product_city)
async def add_product_prompt_name(message: Message, state: FSMContext):
    await state.update_data(city_id=int(message.text))
    await message.answer("📝 Enter product name:")
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
async def add_area_prompt_product(message: Message, state: FSMContext):
    with get_session() as db:
        products = db.query(Product).all()
    msg = "Select product ID:\n" + "\n".join(f"{p.id}. {p.name}" for p in products)
    await message.answer(msg)
    await state.set_state(AdminState.area_product)

@router.message(AdminState.area_product)
async def add_area_prompt_name(message: Message, state: FSMContext):
    try:
        product_id = int(message.text)
    except ValueError:
        await message.answer("❌ Invalid product ID. Please enter a number.")
        return

    with get_session() as db:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            await message.answer("❌ Product not found. Try again.")
            return

    await state.update_data(product_id=product_id)
    await message.answer("📝 Enter area/district name:")
    await state.set_state(AdminState.area_name)

@router.message(AdminState.area_name)
async def add_area_save(message: Message, state: FSMContext):
    data = await state.get_data()
    with get_session() as db:
        db.add(Area(name=message.text, product_id=data["product_id"]))
        db.commit()
    await state.clear()
    await message.answer("✅ Area added.", reply_markup=get_admin_keyboard())
    await state.set_state(AdminState.choose_action)

# ➕ Add Amount Flow

@router.message(AdminState.choose_action, F.text == "➕ Add Amount")
async def add_amount_prompt_area(message: Message, state: FSMContext):
    with get_session() as db:
        areas = db.query(Area).all()
    msg = "Select area ID:\n" + "\n".join(f"{a.id}. {a.name}" for a in areas)
    await message.answer(msg)
    await state.set_state(AdminState.amount_area)

@router.message(AdminState.amount_area)
async def add_amount_prompt_label(message: Message, state: FSMContext):
    try:
        area_id = int(message.text)
    except ValueError:
        await message.answer("❌ Invalid area ID. Please enter a number.")
        return

    with get_session() as db:
        area = db.query(Area).filter(Area.id == area_id).first()
        if not area:
            await message.answer("❌ Area not found. Try again.")
            return

    await state.update_data(area_id=area_id)
    await message.answer("📝 Enter amount label (e.g., 0.5g):")
    await state.set_state(AdminState.amount_label)

@router.message(AdminState.amount_label)
async def add_amount_prompt_price(message: Message, state: FSMContext):
    await state.update_data(label=message.text)
    await message.answer("💰 Enter price (EUR):")
    await state.set_state(AdminState.amount_price)

@router.message(AdminState.amount_price)
async def add_amount_save(message: Message, state: FSMContext):
    try:
        price = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("❌ Invalid price. Please enter a numeric value.")
        return

    data = await state.get_data()
    with get_session() as db:
        db.add(Amount(area_id=data["area_id"], label=data["label"], price=price))
        db.commit()

    await state.clear()
    await message.answer("✅ Amount added.", reply_markup=get_admin_keyboard())
    await state.set_state(AdminState.choose_action)

@router.message(F.text == "📝 Edit Purchase Info")
async def edit_purchase_note(message: Message, state: FSMContext):
    await message.answer("Send the purchase info you'd like to set (this will show after a purchase).")
    await state.set_state(AdminState.edit_purchase_note)

@router.message(F.text == "💸 Refund Buyer")
async def refund_buyer(message: Message, state: FSMContext):
    await message.answer("Send the user ID and refund amount (e.g. 123456789 5.00).")
    await state.set_state(AdminState.refund)

@router.message(F.text == "💰 Add Balance")
async def add_balance(message: Message, state: FSMContext):
    await message.answer("Send the user ID and amount to add (e.g. 123456789 10.00).")
    await state.set_state(AdminState.add_balance)

@router.callback_query(F.data.startswith("edit_note:"))
async def edit_purchase_note(callback: types.CallbackQuery, state: FSMContext):
    amount_id = int(callback.data.split(":")[1])
    await state.update_data(amount_id=amount_id)
    await state.set_state(AdminState.editing_note)
    await callback.message.answer("📝 Send new post-purchase message (or type 'cancel'):")

@router.message(AdminState.editing_note)
async def save_note(message: types.Message, state: FSMContext):
    if message.text.lower() == "cancel":
        await state.clear()
        return await message.answer("❌ Cancelled.")
    data = await state.get_data()
    amount_id = data.get("amount_id")
    with get_session() as db:
        amount = db.query(Amount).filter_by(id=amount_id).first()
        if amount:
            amount.purchase_note = message.text
            db.commit()
    await state.clear()
    await message.answer("✅ Saved post-purchase message.")

@router.message(AdminState.choose_action, F.text == "🔄 Refund User")
async def ask_user_id_for_refund(message: Message, state: FSMContext):
    await message.answer("Enter User ID to refund:")
    await state.set_state(AdminState.refund_user_id)

@router.message(AdminState.refund_user_id)
async def process_refund(message: Message, state: FSMContext):
    user_id = int(message.text)
    with get_session() as db:
        from app.models import User
        user = db.query(User).filter_by(telegram_id=user_id).first()
        if not user:
            await message.answer("❌ User not found.")
        else:
            user.balance += 10.0  # Or use state to specify amount
            db.commit()
            await message.answer(f"✅ Refunded $10 to user {user_id}.")
    await state.set_state(AdminState.choose_action)

@router.message(AdminState.choose_action, F.text == "💰 Edit Balance")
async def ask_balance_user_id(message: Message, state: FSMContext):
    await message.answer("Enter User ID to change balance:")
    await state.set_state(AdminState.balance_user_id)

@router.message(AdminState.balance_user_id)
async def ask_balance_amount(message: Message, state: FSMContext):
    await state.update_data(user_id=int(message.text))
    await message.answer("Enter amount to add (negative to subtract):")
    await state.set_state(AdminState.balance_amount)

@router.message(AdminState.balance_amount)
async def update_user_balance(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    amount = float(message.text)
    with get_session() as db:
        from app.models import User
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
    await message.answer("Enter Telegram User ID to lookup:")
    await state.set_state(AdminState.lookup_user)

@router.message(AdminState.lookup_user)
async def lookup_user_data(message: Message, state: FSMContext):
    user_id = int(message.text)
    with get_session() as db:
        from app.models import User, Purchase
        user = db.query(User).filter_by(telegram_id=user_id).first()
        if not user:
            await message.answer("❌ User not found.")
        else:
            purchases = db.query(Purchase).filter_by(user_id=user.id).count()
            await message.answer(
                f"👤 User ID: {user.telegram_id}\nBalance: ${user.balance:.2f}\nLanguage: {user.language}\nPurchases: {purchases}"
            )
    await state.set_state(AdminState.choose_action)

@router.message(AdminState.choose_action, F.text == "📦 View Stock")
async def view_stock_summary(message: Message, state: FSMContext):
    with get_session() as db:
        from app.models import Product
        products = db.query(Product).all()
        if not products:
            await message.answer("❌ No products found.")
            return
        lines = []
        for p in products:
            lines.append(f"{p.name}: Stock = {p.stock} | Price = ${p.price}")
        await message.answer("📦 Product Inventory:\n\n" + "\n".join(lines))

@router.message(AdminState.choose_action, F.text == "📊 Bot Stats")
async def show_bot_stats(message: Message, state: FSMContext):
    with get_session() as db:
        from app.models import User, Purchase, Product
        users = db.query(User).count()
        purchases = db.query(Purchase).count()
        total_sales = sum(p.product.price for p in db.query(Purchase).all() if p.product)
        products = db.query(Product).count()

    await message.answer(
        f"📊 Stats:\n\n👥 Users: {users}\n🛍 Purchases: {purchases}\n📦 Products: {products}\n💵 Revenue: ${total_sales:.2f}"
    )
