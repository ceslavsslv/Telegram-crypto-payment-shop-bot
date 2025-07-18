# utils/texts.py
from aiogram.types import Message, CallbackQuery
from app.database import get_db
from app.utils.helpers import get_or_create_user

texts = {
    "start": {
        "en": "Welcome to the shop! Use the buttons below to navigate.",
        "ru": "Добро пожаловать в магазин! Используйте кнопки ниже для навигации.",
        "lv": "Laipni lūdzam veikalā! Izmantojiet pogas zemāk, lai pārvietotos."
    },
    "language_set": {
        "en": "🇺🇸 English language has been successfully installed",
        "ru": "🇷🇺 Русский язык успешно установлен",
        "lv": "🇱🇻 Latviešu valoda veiksmīgi uzstādīta"
    },
    "menu_buttons": {
        "shopping": {
            "en": "🛍️ Shopping", "ru": "🛍️ Покупки", "lv": "🛍️ Iepirkšanās"
            },
        "add_funds": {
            "en": "💶 Add funds", "ru": "💶 Пополнить баланс", "lv": "💶 Pievienot līdzekļus"
            },
        "account": {
            "en": "🛒 Account", "ru": "🛒 Аккаунт", "lv": "🛒 Konts"
            },
        "support": {
            "en": "☎️ Support", "ru": "☎️ Поддержка", "lv": "☎️ Atbalsts"
            },
        "news": {
            "en": "📰 News", "ru": "📰 Новости", "lv": "📰 Ziņas"
            },
        "referral": {
            "en": "🔷 Referral system", "ru": "🔷 Реферальная система", "lv": "🔷 Ieteikumu sistēma"
            },
        "language": {
            "en": "🇷🇺 Change language", "ru": "🇺🇸 Сменить язык", "lv": "🇬🇧 Mainīt valodu"
            }
    },
    "account_info": {
        "en": "👤 Balance: EUR{balance:.2f}\nUser ID: {user_id}\nTotal purchases: {total} EUR\n{history}",
        "ru": "👤 Баланс: EUR{balance:.2f}\nID пользователя: {user_id}\nВсего покупок: {total} EUR\n{history}",
        "lv": "👤 Bilance: EUR{balance:.2f}\nLietotāja ID: {user_id}\nKopējie pirkumi: {total} EUR\n{history}"
    },
    "history_entry": {
        "en": "🛒 {product} - ${price} ({timestamp})",
        "ru": "🛒 {product} - ${price} ({timestamp})",
        "lv": "🛒 {product} - ${price} ({timestamp})"
    },
    "no_purchases": {
        "en": "No purchases yet.",
        "ru": "Пока нет покупок.",
        "lv": "Vēl nav veikti pirkumi."
    },
    "ref_info": {
        "en": "🔗 You invited {count} users.\nEarned: EUR{earned:.2f}",
        "ru": "🔗 Вы пригласили {count} пользователей.\nЗаработано: EUR{earned:.2f}",
        "lv": "🔗 Tu uzaicināji {count} lietotājus.\nNopelnīts: EUR{earned:.2f}"
    },
    "NO_CITIES" : {
        "en": "No cities available at the moment.",
        "lv": "Pagaidām nav pieejamu pilsētu.",
        "ru": "На данный момент нет доступных городов."
    },

    "NO_PRODUCTS" : {
        "en": "No products available in this city.",
        "lv": "Šajā pilsētā nav pieejamu produktu.",
        "ru": "В этом городе нет доступных товаров."
    },

    "NO_AREAS" : {
        "en": "No districts available for this product.",
        "lv": "Nav pieejamu rajonu šim produktam.",
        "ru": "Для этого продукта нет доступных районов."
    },

    "NO_AMOUNTS" : {
        "en": "No product amounts available in this area.",
        "lv": "Šajā rajonā nav pieejamu produktu daudzumu.",
        "ru": "В этом районе нет доступных вариантов товара."
    },

    "CHOOSE_CITY" : {
        "en": "🌆 Choose your city:",
        "lv": "🌆 Izvēlies pilsētu:",
        "ru": "🌆 Выберите город:"
    },

    "CHOOSE_PRODUCT" : {
        "en": "🛍 Choose a product:",
        "lv": "🛍 Izvēlies produktu:",
        "ru": "🛍 Выберите товар:"
    },

    "CHOOSE_AREA" : {
        "en": "📍 Choose an area/district:",
        "lv": "📍 Izvēlies rajonu:",
        "ru": "📍 Выберите район:"
    },

    "CHOOSE_AMOUNT" : {
        "en": "💸 Choose amount:",
        "lv": "💸 Izvēlies summu:",
        "ru": "💸 Выберите сумму:"
    },

    "CONFIRM_PURCHASE" : {
        "en": "✅ Confirm your purchase or navigate:",
        "lv": "✅ Apstiprini pirkumu vai pārvietojies:",
        "ru": "✅ Подтвердите покупку или выберите действие:"
    },

    "PAY_WITH_BALANCE" : {
        "en": "💳 Pay with Balance",
        "lv": "💳 Maksāt ar bilanci",
        "ru": "💳 Купить с баланса"
    },

    "BACK" : {
        "en": "🔙 Back",
        "lv": "🔙 Atpakaļ",
        "ru": "🔙 Назад"
    },

    "MAIN_MENU" : {
        "en": "🏠 Main Menu",
        "lv": "🏠 Galvenā izvēlne",
        "ru": "🏠 Главное меню"
    },
    "INSUFFICIENT_FUNDS" : {
        "en": "❌ Insufficient balance.",
        "lv": "❌ Nepietiekama bilance.",
        "ru": "❌ Недостаточно средств.",
    },

    "PURCHASE_SUCCESS" : {
        "en": "✅ Purchase successful!",
        "lv": "✅ Pirkums veiksmīgs!",
        "ru": "✅ Покупка успешна!",
    },

    "INVALID_SELECTION" : {
        "en": "Invalid purchase selection.",
        "lv": "Nederīga izvēle.",
        "ru": "Неверный выбор покупки.",
    },

    "OUT_OF_STOCK" : {
        "en": "❌ Product is out of stock.",
        "lv": "❌ Produkts nav pieejams.",
        "ru": "❌ Товар отсутствует на складе.",
    },

    "NO_SUCH_AMOUNT" : {
        "en": "This product amount is no longer available.",
        "lv": "Šī produkta summa vairs nav pieejama.",
        "ru": "Этот номинал товара больше недоступен.",
    },
    "AREA_NOT_FOUND": {
        "en": "❌ Area not found. It might have been removed.",
        "lv": "❌ Rajons nav atrasts. Tas varētu būt izdzēsts.",
        "ru": "❌ Район не найден. Возможно, он был удален."
    },
    "INVALID_SELECTION": {
        "en": "❌ Invalid selection. Please try again from the menu.",
        "lv": "❌ Invalid selection. Please try again from the menu.",
        "ru": "❌ Неверный выбор. Пожалуйста, попробуйте снова из меню."
    },
    "PRODUCT_NOT_FOUND": {
        "en": "❌ Product not found. It may have been removed.",
        "lv": "❌ Produkts nav atrasts.",
        "ru": "❌ Продукт не найден. Возможно, он был удален."
    },
    "AMOUNT_NOT_FOUND": {
        "en": "❌ Amount not found. Please choose another option.",
        "lv": "❌ Daudzums nav atrasts",
        "ru": "❌ Сумма не найдена. Пожалуйста, выберите другой вариант."
    },

}
NO_CITIES = {
    "en": "No cities available at the moment.",
    "lv": "Pagaidām nav pieejamu pilsētu.",
    "ru": "На данный момент нет доступных городов."
}

NO_PRODUCTS = {
    "en": "No products available in this city.",
    "lv": "Šajā pilsētā nav pieejamu produktu.",
    "ru": "В этом городе нет доступных товаров."
}

NO_AREAS = {
    "en": "No districts available for this product.",
    "lv": "Nav pieejamu rajonu šim produktam.",
    "ru": "Для этого продукта нет доступных районов."
}

NO_AMOUNTS = {
    "en": "No product amounts available in this area.",
    "lv": "Šajā rajonā nav pieejamu produktu daudzumu.",
    "ru": "В этом районе нет доступных вариантов товара."
}

CHOOSE_CITY = {
    "en": "🌆 Choose your city:",
    "lv": "🌆 Izvēlies pilsētu:",
    "ru": "🌆 Выберите город:"
}

CHOOSE_PRODUCT = {
    "en": "🛍 Choose a product:",
    "lv": "🛍 Izvēlies produktu:",
    "ru": "🛍 Выберите товар:"
}

CHOOSE_AREA = {
    "en": "📍 Choose an area/district:",
    "lv": "📍 Izvēlies rajonu:",
    "ru": "📍 Выберите район:"
}

CHOOSE_AMOUNT = {
    "en": "💸 Choose amount:",
    "lv": "💸 Izvēlies summu:",
    "ru": "💸 Выберите сумму:"
}

CONFIRM_PURCHASE = {
    "en": "✅ Confirm your purchase or navigate:",
    "lv": "✅ Apstiprini pirkumu vai pārvietojies:",
    "ru": "✅ Подтвердите покупку или выберите действие:"
}

PAY_WITH_BALANCE = {
    "en": "💳 Pay with Balance",
    "lv": "💳 Maksāt ar bilanci",
    "ru": "💳 Купить с баланса"
}

BACK = {
    "en": "🔙 Back",
    "lv": "🔙 Atpakaļ",
    "ru": "🔙 Назад"
}

MAIN_MENU = {
    "en": "🏠 Main Menu",
    "lv": "🏠 Galvenā izvēlne",
    "ru": "🏠 Главное меню"
}
INSUFFICIENT_FUNDS = {
    "en": "❌ Insufficient balance.",
    "lv": "❌ Nepietiekama bilance.",
    "ru": "❌ Недостаточно средств.",
}

PURCHASE_SUCCESS = {
    "en": "✅ Purchase successful!",
    "lv": "✅ Pirkums veiksmīgs!",
    "ru": "✅ Покупка успешна!",
}

INVALID_SELECTION = {
    "en": "Invalid purchase selection.",
    "lv": "Nederīga izvēle.",
    "ru": "Неверный выбор покупки.",
}

OUT_OF_STOCK = {
    "en": "❌ Product is out of stock.",
    "lv": "❌ Produkts nav pieejams.",
    "ru": "❌ Товар отсутствует на складе.",
}

NO_SUCH_AMOUNT = {
    "en": "This product amount is no longer available.",
    "lv": "Šī produkta summa vairs nav pieejama.",
    "ru": "Этот номинал товара больше недоступен.",
}


def get_lang(source) -> str:
    # From language string
    if isinstance(source, str):
        return source
    # From Telegram message or callback
    telegram_id = None
    if isinstance(source, Message):
        telegram_id = source.from_user.id
    elif isinstance(source, CallbackQuery):
        telegram_id = source.from_user.id
    elif hasattr(source, "language"):
        return getattr(source, "language", "en")

    if telegram_id:
        db = next(get_db())
        user = get_or_create_user(db, telegram_id=telegram_id)
        return getattr(user, "language", "en")

    return "en"

def t(key: str, source, **kwargs):
    lang = get_lang(source)
    lang_data = texts.get(key)
    if not lang_data:
        return f"[Missing text: {key}]"
    return lang_data.get(lang, lang_data.get("en", "")).format(**kwargs)
