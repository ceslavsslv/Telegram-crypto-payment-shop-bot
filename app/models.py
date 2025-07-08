from dataclasses import dataclass
from typing import Optional

@dataclass
class City:
    id: int
    name: str

@dataclass
class Product:
    id: int
    city_id: int
    name: str
    description: str

@dataclass
class ProductOption:
    id: int
    product_id: int
    amount: str
    price: float

@dataclass
class User:
    id: int
    telegram_id: int
    balance: float = 0.0

@dataclass
class Order:
    id: int
    user_id: int
    option_id: int
    status: str
    created: str
