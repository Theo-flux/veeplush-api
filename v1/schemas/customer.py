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
