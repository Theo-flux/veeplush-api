from typing import List
from enum import Enum
from pydantic import BaseModel, Field


class OrderStatusSchema(str, Enum):
    PENDING = "PENDING"
    CANCELED = "CANCELED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"


class OrderItemSchema(BaseModel):
    product_id: int = Field(...)
    sub_total: float = Field(...)
    length: int = Field(...)
    style: str = Field(...)
    qty: int = Field(...)


class AddToCartSchema(BaseModel):
    customer_id: int = Field(...)
    order_status: str = OrderStatusSchema.PENDING
    total_amount: float = Field(...)
    order_items: List[OrderItemSchema] = Field(...)


class GetCartResponseSchema(BaseModel):
    pass
