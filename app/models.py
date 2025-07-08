# models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    language = Column(String(5), default="en")
    balance = Column(Float, default=0.0)
    referred_by = Column(Integer, ForeignKey("users.telegram_id"), nullable=True)

    purchases = relationship("Purchase", back_populates="user")

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    is_active = Column(Boolean, default=True)

    products = relationship("Product", back_populates="city")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    name = Column(String)
    description = Column(Text)
    price = Column(Float)
    stock = Column(Integer)
    is_active = Column(Boolean, default=True)

    city = relationship("City", back_populates="products")

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    timestamp = Column(DateTime, default=func.now())
    details = Column(Text)

    user = relationship("User", back_populates="purchases")
    product = relationship("Product")
