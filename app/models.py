# models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    language = Column(String(5), default="en")
    balance = Column(Float, default=0.0)
    referred_by = Column(Integer, ForeignKey("users.telegram_id"), nullable=True)
    referral_bonus_claimed = Column(Boolean, default=False)

    purchases = relationship("Purchase", back_populates="user")

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    is_active = Column(Boolean, default=True)

    products = relationship("Product", back_populates="city", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    name = Column(String)
    is_active = Column(Boolean, default=True)

    city = relationship("City", back_populates="products")
    areas = relationship("Area", back_populates="product", cascade="all, delete-orphan")

class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    is_active = Column(Boolean, default=True)

    city = relationship("City")
    product = relationship("Product", back_populates="areas")
    amounts = relationship("Amount", back_populates="area", cascade="all, delete-orphan")

class Amount(Base):
    __tablename__ = "amounts"

    id = Column(Integer, primary_key=True, index=True)
    area_id = Column(Integer, ForeignKey("areas.id"))
    label = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    image_file_id = Column(String, nullable=True)
    purchase_info = Column(Text, nullable=True)
    description = Column(Text, default="")

    area = relationship("Area", back_populates="amounts")
    
class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount_id = Column(Integer, ForeignKey("amounts.id"))
    timestamp = Column(DateTime, default=func.now())
    delivery_note = Column(String, nullable=True)
    delivery_location = Column(String, nullable=True)
    delivery_photos = Column(String, nullable=True)
    total_price = Column(Float, nullable=False)


    user = relationship("User", back_populates="purchases")
    product = relationship("Product")
    amount = relationship("Amount")
    
class StockItem(Base):
    __tablename__ = "stock_items"

    id = Column(Integer, primary_key=True)
    amount_id = Column(Integer, ForeignKey("amounts.id"))
    note = Column(Text)
    photos = Column(Text)
    location = Column(Text)
    created_at = Column(DateTime, default=func.now)

    amount = relationship("Amount", back_populates="stock_items")
