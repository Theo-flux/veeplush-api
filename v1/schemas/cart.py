from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class OrderStatusSchema(str, Enum):
    PENDING = "pending"
    CANCELED = "canceled"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


class OrderItemSchema(BaseModel):
    order_id: int
    product_id: int
    sub_total: float
    length: int
    style: str
    qty: int


class AddToCartSchema(BaseModel):
    customer_id: int = Field(...)
    order_status: str = OrderStatusSchema.PENDING
    order_date: datetime = Field(...)
    total_amount: float = Field(...)
    order_items: List[OrderItemSchema] = Field(...)
