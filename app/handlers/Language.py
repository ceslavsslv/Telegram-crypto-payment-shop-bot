from aiogram import Router, types, F
from app.keyboards.common import main_menu_keyboard, get_menu_button_values
from app.utils.texts import texts
from app.database import get_db
from app.utils.helpers import get_or_create_user

router=Router()

@router.message(F.text.in_(get_menu_button_values("language")))
async def language_switch(message: types.Message):
    try:
        db = next(get_db())
        user = get_or_create_user(db, telegram_id=message.from_user.id)
        user.language = "ru" if user.language == "en" else "en"
        db.commit()
        await message.answer(
            texts["language_set"].get(user.language, "Language updated."),
            reply_markup=main_menu_keyboard(user.language)
        )
    except Exception:
        await message.answer("⚠️ Language change failed.")
