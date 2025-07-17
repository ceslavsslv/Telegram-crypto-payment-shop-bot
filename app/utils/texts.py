# utils/texts.py

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
    }
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

BUY_BY_BALANCE = {
    "en": "✅ Buy by Balance",
    "lv": "✅ Pirkt ar bilanci",
    "ru": "✅ Купить с баланса"
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


def t(key: str, lang: str = "en", **kwargs):
    lang_data = texts.get(key)
    if not lang_data:
        return f"[Missing text: {key}]"
    return lang_data.get(lang, lang_data.get("en", "")).format(**kwargs)