from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from product import Product


class CategoryBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Смартфоны", "Ноутбуки", "Наушники"],
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=100, examples=["Смартфоны", "Ноутбуки"]
    )


class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class CategoryWithProducts(Category):
    products: Optional[list[Product]]
