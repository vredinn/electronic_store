from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from models import OrderStatus


class OrderItemBase(BaseModel):
    product_id: int
    product_name: str
    quantity: int = Field(..., gt=0)
    price_at_order: Decimal = Field(..., gt=0, decimal_places=2)


class OrderBase(BaseModel):
    status: OrderStatus = Field(default=OrderStatus.PENDING)


class OrderCreate(OrderBase):
    items: List[OrderItemBase]


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus]


class Order(OrderBase):
    id: int
    user_id: int
    amount: Decimal
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[OrderItemBase]

    class Config:
        from_attributes = True
