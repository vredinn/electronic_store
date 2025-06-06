from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from enum import Enum


class SortBy(str, Enum):
    NAME = "name"
    PRICE = "price"
    RATING = "rating"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class ProductPage(BaseModel):
    items: List["Product"]
    total: int
    page: int
    limit: int
    pages: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=250,
        examples=[
            "Смартфон iPhone 13",
            "Ноутбук ASUS ROG Strix G15",
            "Наушники Sony WH-1000XM4",
        ],
    )
    price: Decimal = Field(
        ...,
        gt=0,
        decimal_places=2,
        max_digits=12,
        examples=[Decimal("50000.99"), Decimal("120000.99"), Decimal("35000.99")],
    )
    category_id: int = Field(
        ...,
        examples=[1, 2, 3],
        description="ID категории товара. Должен соответствовать существующей категории.",
    )
    description: Optional[str] = Field(
        ...,
        examples=[
            "Смартфон с 6.1-дюймовым дисплеем, процессором A15 Bionic и камерой 12 МП.",
            "Игровой ноутбук с процессором Intel Core i7, видеокартой NVIDIA RTX 3060 и 16 ГБ ОЗУ.",
            "Беспроводные наушники с активным шумоподавлением и длительным временем работы от батареи.",
        ],
    )
    stock: int = Field(
        ...,
        examples=[100, 50, 200],
        description="Количество товара на складе. Не может быть отрицательным.",
    )


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=250,
        examples=[
            "Смартфон iPhone 13",
            "Ноутбук ASUS ROG Strix G15",
            "Наушники Sony WH-1000XM4",
        ],
    )
    price: Optional[Decimal] = Field(
        None,
        gt=0,
        decimal_places=2,
        max_digits=12,
        examples=[Decimal("50000.99"), Decimal("120000.99"), Decimal("35000.99")],
    )
    category_id: Optional[int] = Field(
        None,
        examples=[1, 2, 3],
        description="ID категории товара. Должен соответствовать существующей категории.",
    )
    description: Optional[str] = Field(
        None,
        examples=[
            "Смартфон с 6.1-дюймовым дисплеем, процессором A15 Bionic и камерой 12 МП.",
            "Игровой ноутбук с процессором Intel Core i7, видеокартой NVIDIA RTX 3060 и 16 ГБ ОЗУ.",
            "Беспроводные наушники с активным шумоподавлением и длительным временем работы от батареи.",
        ],
    )
    stock: Optional[int] = Field(
        None,
        examples=[100, 50, 200],
        description="Количество товара на складе. Не может быть отрицательным.",
    )


class Product(ProductBase):
    id: int
    category_name: str
    created_at: datetime
    updated_at: Optional[datetime]
    rating: int

    class Config:
        from_attributes = True
