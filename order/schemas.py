from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from models import OrderStatus


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderItem(OrderItemBase):
    product_name: str
    price_at_order: Decimal = Field(..., gt=0, decimal_places=2)


class OrderBase(BaseModel):
    pass


class OrderCreate(OrderBase):
    items: List[OrderItemBase]


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus]


class Order(OrderBase):
    id: int
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    user_id: int
    user_name: str
    amount: Decimal
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[OrderItem]

    class Config:
        from_attributes = True
