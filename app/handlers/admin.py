# handlers/admin.py
from aiogram import Router, types, F, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, Filter
from sqlalchemy.orm import Session
from app.states.admin import AdminState
from app.config import ADMINS
from app.database import engine, get_session
from app.models import Base, City, Product, Area, Amount, User
from app.keyboards.admin_menu import get_admin_keyboard #ADMIN_KB, CANCEL_KB 

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
    await state.update_data(city_id=int(message.text))
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
async def add_area_prompt_product(message: Message, state: FSMContext):
    with get_session() as db:
        products = db.query(Product).all()
    msg = "Select product ID:\n" + "\n".join(f"{p.id}. {p.name}" for p in products)
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
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
    await message.answer("📝 Enter area/district name:", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
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
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
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
    await message.answer("📝 Enter amount label (1peace, 10EUR, etc.):", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
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
    msg = "Send the purchase info you'd like to set (this will show after a purchase)."
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.edit_purchase_note)

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
    msg = "Enter Telegram User ID to lookup:"
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
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

@router.message(AdminState.choose_action, F.text == "🗑 Remove Product")
async def remove_product_prompt(message: Message, state: FSMContext):
    with get_session() as db:
        products = db.query(Product).all()
    if not products:
        await message.answer("⚠️ No products found.")
        return
    msg = "📋 Enter product ID to remove:\n" + "\n".join(f"{p.id}. {p.name}" for p in products)
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

@router.message(AdminState.choose_action, F.text == "🗑 Remove Area")
async def remove_area_prompt(message: Message, state: FSMContext):
    with get_session() as db:
        areas = db.query(Area).all()
    if not areas:
        await message.answer("⚠️ No areas found.")
        return
    msg = "📋 Enter area ID to remove:\n" + "\n".join(f"{a.id}. {a.name}" for a in areas)
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

@router.message(AdminState.choose_action, F.text == "🗑 Remove Amount")
async def remove_amount_prompt(message: Message, state: FSMContext):
    with get_session() as db:
        amounts = db.query(Amount).all()
    if not amounts:
        await message.answer("⚠️ No amounts found.")
        return
    msg = "📋 Enter amount ID to remove:\n" + "\n".join(
        f"{a.id}. {a.amount}€ (Area ID: {a.area_id})" for a in amounts
    )
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

    msg = "🖼 Select amount to upload an image:\n" + "\n".join(
        f"{a.id}. {a.label} ({a.price}€) – Area ID: {a.area_id}" for a in amounts
    )
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.edit_amount_image)

@router.message(AdminState.edit_amount_image)
async def admin_upload_image(message: Message, state: FSMContext):
    if message.text == "❌ Cancel":
        await message.answer("❌ Cancelled", reply_markup=get_admin_keyboard())
        return await state.set_state(AdminState.choose_action)

    try:
        amount_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Invalid ID. Please enter a number.")
        return

    with get_session() as db:
        amount = db.query(Amount).filter_by(id=amount_id).first()

    if not amount:
        await message.answer("❌ Amount not found.")
        return

    await state.update_data(amount_id=amount_id)
    await message.answer("📸 Now send the photo to use for this amount, or /cancel to abort.")
    await state.set_state(AdminState.edit_amount_select)

@router.message(AdminState.edit_amount_select, F.photo)
async def admin_save_amount_image(message: Message, state: FSMContext):
    data = await state.get_data()
    amount_id = data.get("amount_id")

    photo = message.photo[-1]
    file_id = photo.file_id

    with get_session() as db:
        amount = db.query(Amount).filter_by(id=amount_id).first()
        if amount:
            amount.image_file_id = file_id
            db.commit()

    await message.answer("✅ Image saved for this amount.", reply_markup=get_admin_keyboard())
    await state.set_state(AdminState.choose_action)

@router.message(AdminState.edit_amount_select)
async def admin_image_required(message: Message, state: FSMContext):
    await message.answer("❌ Please send an actual photo.")

@router.message(AdminState.choose_action, F.text == "✏️ Set Amount Description")
async def admin_start_edit_description(message: Message, state: FSMContext):
    with get_session() as db:
        amounts = db.query(Amount).all()
    if not amounts:
        await message.answer("⚠️ No amounts available.")
        return

    msg = "✏️ Select amount to edit its description:\n" + "\n".join(
        f"{a.id}. {a.label} ({a.price}€) – Area ID: {a.area_id}" for a in amounts
    )
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True
    ))
    await state.set_state(AdminState.edit_amount_description)

@router.message(AdminState.edit_amount_description)
async def admin_enter_description(message: Message, state: FSMContext):
    if message.text == "❌ Cancel":
        await message.answer("❌ Cancelled", reply_markup=get_admin_keyboard())
        return await state.set_state(AdminState.choose_action)

    try:
        amount_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Invalid ID.")
        return

    with get_session() as db:
        amount = db.query(Amount).filter_by(id=amount_id).first()

    if not amount:
        await message.answer("❌ Amount not found.")
        return

    await state.update_data(amount_id=amount_id)
    await message.answer("📝 Now send the new description text.")
    await state.set_state(AdminState.edit_amount_select)

@router.message(AdminState.edit_amount_select)
async def admin_save_description(message: Message, state: FSMContext):
    data = await state.get_data()
    amount_id = data.get("amount_id")

    with get_session() as db:
        amount = db.query(Amount).filter_by(id=amount_id).first()
        if amount:
            amount.description = message.text
            db.commit()

    await message.answer("✅ Description updated.", reply_markup=get_admin_keyboard())
    await state.set_state(AdminState.choose_action)

@router.message(AdminState.choose_action, F.text == "📝 Set Delivery Note")
async def admin_start_delivery_note(message: Message, state: FSMContext):
    with get_session() as db:
        amounts = db.query(Amount).all()
    if not amounts:
        await message.answer("⚠️ No amounts available.")
        return

    msg = "📝 Select amount to edit its delivery note:\n" + "\n".join(
        f"{a.id}. {a.label} ({a.price}€) – Area ID: {a.area_id}" for a in amounts
    )
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]], resize_keyboard=True
    ))
    await state.set_state(AdminState.edit_amount_note)

@router.message(AdminState.edit_amount_note)
async def admin_save_note(message: Message, state: FSMContext):
    if message.text == "❌ Cancel":
        await message.answer("❌ Cancelled", reply_markup=get_admin_keyboard())
        return await state.set_state(AdminState.choose_action)

    try:
        amount_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Invalid ID.")
        return

    with get_session() as db:
        amount = db.query(Amount).filter_by(id=amount_id).first()

    if not amount:
        await message.answer("❌ Amount not found.")
        return

    await state.update_data(amount_id=amount_id)
    await message.answer("💬 Now send the delivery note to show after payment.")
    await state.set_state(AdminState.edit_amount_select)

@router.message(AdminState.edit_amount_select)
async def admin_save_delivery_note(message: Message, state: FSMContext):
    data = await state.get_data()
    amount_id = data.get("amount_id")

    with get_session() as db:
        amount = db.query(Amount).filter_by(id=amount_id).first()
        if amount:
            amount.purchase_info = message.text
            db.commit()

    await message.answer("✅ Delivery note saved.", reply_markup=get_admin_keyboard())
    await state.set_state(AdminState.choose_action)

@router.message(AdminState.choose_action, F.text == "♻️ Remove Image/Note")
async def admin_start_removal(message: Message, state: FSMContext):
    with get_session() as db:
        amounts = db.query(Amount).all()
    if not amounts:
        await message.answer("⚠️ No amounts available.")
        return

    msg = "♻️ Select amount to remove a field:\n" + "\n".join(
        f"{a.id}. {a.label} ({a.price}€) – Area ID: {a.area_id}" for a in amounts
    )
    await message.answer(msg, reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]], resize_keyboard=True
    ))
    await state.set_state(AdminState.edit_amount_remove_option)

@router.message(AdminState.edit_amount_remove_option)
async def admin_choose_removal_field(message: Message, state: FSMContext):
    if message.text == "❌ Cancel":
        await message.answer("❌ Cancelled", reply_markup=get_admin_keyboard())
        return await state.set_state(AdminState.choose_action)

    try:
        amount_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Invalid ID.")
        return

    with get_session() as db:
        amount = db.query(Amount).filter_by(id=amount_id).first()

    if not amount:
        await message.answer("❌ Amount not found.")
        return

    await state.update_data(amount_id=amount_id)
    await message.answer(
        "♻️ What do you want to remove?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🖼 Remove Image")],
                [KeyboardButton(text="✏️ Remove Description")],
                [KeyboardButton(text="📝 Remove Delivery Note")],
                [KeyboardButton(text="❌ Cancel")]
            ],
            resize_keyboard=True
        )
    )
    await state.set_state(AdminState.edit_amount_select)

@router.message(AdminState.edit_amount_select)
async def admin_remove_selected_field(message: Message, state: FSMContext):
    data = await state.get_data()
    amount_id = data.get("amount_id")

    field = None
    label = None

    if message.text == "🖼 Remove Image":
        field = "image_file_id"
        label = "image"
    elif message.text == "✏️ Remove Description":
        field = "description"
        label = "description"
    elif message.text == "📝 Remove Delivery Note":
        field = "purchase_info"
        label = "delivery note"
    elif message.text == "❌ Cancel":
        await message.answer("❌ Cancelled", reply_markup=get_admin_keyboard())
        return await state.set_state(AdminState.choose_action)
    else:
        await message.answer("❌ Unknown option.")
        return

    with get_session() as db:
        amount = db.query(Amount).filter_by(id=amount_id).first()
        if amount and hasattr(amount, field):
            setattr(amount, field, None)
            db.commit()
            await message.answer(f"✅ {label.capitalize()} removed.", reply_markup=get_admin_keyboard())
        else:
            await message.answer("⚠️ Failed to update.")

    await state.set_state(AdminState.choose_action)
