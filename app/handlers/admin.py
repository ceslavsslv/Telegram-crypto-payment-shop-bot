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
        db.add(City(name=city_name))
        db.commit()
    await state.clear()
    await message.answer("✅ City added.", reply_markup=get_admin_keyboard())
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
    await state.update_data(product_id=int(message.text))
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
    await state.update_data(area_id=int(message.text))
    await message.answer("📝 Enter amount label (e.g., 0.5g):")
    await state.set_state(AdminState.amount_label)

@router.message(AdminState.amount_label)
async def add_amount_prompt_price(message: Message, state: FSMContext):
    await state.update_data(label=message.text)
    await message.answer("💰 Enter price (EUR):")
    await state.set_state(AdminState.amount_price)

@router.message(AdminState.amount_price)
async def add_amount_save(message: Message, state: FSMContext):
    data = await state.get_data()
    with get_session() as db:
        db.add(Amount(area_id=data["area_id"], label=data["label"], price=float(message.text)))
        db.commit()
    await state.clear()
    await message.answer("✅ Amount added.", reply_markup=get_admin_keyboard())
    await state.set_state(AdminState.choose_action)

