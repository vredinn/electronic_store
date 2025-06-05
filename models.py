from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum


class UserRole(str, Enum):
    BUYER = "Покупатель"
    MANAGER = "Менеджер"
    ADMIN = "Администратор"


class OrderStatus(str, Enum):
    PENDING = "В обработке"
    PROCESSING = "В доставке"
    SHIPPED = "Доставлен"
    DELIVERED = "Получен"
    CANCELLED = "Отменен"


class ReviewStatus(str, Enum):
    PENDING = "В обработке"
    APPROVED = "Одобрен"
    REJECTED = "Отклонен"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.BUYER, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship(
        "Review", back_populates="user", cascade="all, delete-orphan"
    )


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    products = relationship(
        "Product", back_populates="category", cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    description = Column(String, nullable=False)
    stock = Column(Integer)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship("Category", back_populates="products")
    order_items = relationship(
        "OrderItem", back_populates="product", cascade="all, delete-orphan"
    )
    reviews = relationship(
        "Review", back_populates="product", cascade="all, delete-orphan"
    )


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="orders")
    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id = Column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True
    )
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True
    )
    quantity = Column(Integer, default=1, nullable=False)
    price_at_order = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    rating = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    status = Column(Enum(ReviewStatus), default=ReviewStatus.PENDING, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
