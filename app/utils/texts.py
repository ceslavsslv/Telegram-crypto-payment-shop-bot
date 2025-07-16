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

def t(key: str, lang: str = "en", **kwargs):
    lang_data = texts.get(key)
    if not lang_data:
        return f"[Missing text: {key}]"
    return lang_data.get(lang, lang_data.get("en", "")).format(**kwargs)