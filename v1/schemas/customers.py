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
    first_name: str
    last_name: str
    phone_number: str
    country: str
    city: str
    state: str
    postal_code: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm = True

class CustomerLoginSchema(BaseModel):
    username: Optional[str]  = None
    email: Optional[EmailStr]  = None
    password: str
