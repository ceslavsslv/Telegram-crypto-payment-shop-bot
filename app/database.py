import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db():
    conn = sqlite3.connect("shop.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()

def init_db():
    with get_db() as conn:
        cur = conn.cursor()
        cur.executescript('''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            city_id INTEGER,
            name TEXT,
            description TEXT,
            FOREIGN KEY(city_id) REFERENCES cities(id)
        );

        CREATE TABLE IF NOT EXISTS product_options (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            amount TEXT,
            price REAL,
            FOREIGN KEY(product_id) REFERENCES products(id)
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            telegram_id INTEGER UNIQUE,
            balance REAL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            option_id INTEGER,
            status TEXT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        ''')

def get_user_balance(telegram_id):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT balance FROM users WHERE telegram_id = ?", (telegram_id,))
        row = cur.fetchone()
        return row["balance"] if row else 0

def update_user_balance(telegram_id, new_balance):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET balance = ? WHERE telegram_id = ?", (new_balance, telegram_id))

def create_or_get_user(telegram_id):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (telegram_id,))

def credit_user_balance(telegram_id, amount):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET balance = balance + ? WHERE telegram_id = ?", (amount, telegram_id))