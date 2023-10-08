from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class NewCustomerSchema(BaseModel):
    username: str = Field(min_length=4)
    password: str = Field(min_length=8)
    email: EmailStr


class CustomerResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    shipping_address: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerLoginSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str


class CustomerInfoSchema(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    phone_number: str = Field(..., min_length=11)
    shipping_address: str = Field(...)
    country: str = Field(...)
    city: str = Field(...)
    state: str = Field(...)
    postal_code: str = Field(...)
