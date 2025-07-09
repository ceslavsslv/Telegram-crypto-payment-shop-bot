# utils/helpers.py
from sqlalchemy.orm import Session
from app.models import User, Product, City, Purchase

def get_or_create_user(db: Session, telegram_id: int, language: str = "en") -> User:
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id, language=language)
        db.add(user)
        try:
            db.commit()
            db.refresh(user)
        except Exception:
            db.rollback()
    return user


def get_cities(db: Session):
    try:
        return db.query(City).filter_by(is_active=True).all()
    except Exception:
        return []

def get_products_by_city(db: Session, city_id: int):
    try:
        return db.query(Product).filter_by(city_id=city_id, is_active=True).all()
    except Exception:
        return []
    
def get_product(db: Session, product_id: int):
    try:
        return db.query(Product).filter_by(id=product_id, is_active=True).first()
    except Exception:
        return None
    
def deduct_balance(db: Session, user: User, amount: float) -> bool:
    try:
        if user.balance >= amount:
            user.balance -= amount
            db.commit()
            return True
    except Exception:
        db.rollback()
    return False

def add_purchase(db: Session, user_id: int, product_id: int, details: str):
    try:
        purchase = Purchase(user_id=user_id, product_id=product_id, info=info)
        db.add(purchase)
        db.commit()
    except Exception:
        db.rollback()

