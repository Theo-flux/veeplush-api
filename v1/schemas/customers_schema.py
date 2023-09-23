from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class NewCustomer(BaseModel):
    username: str
    password: str
    email: EmailStr

class CustomerResponse(BaseModel):
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

class CustomerLogin(BaseModel):
    username: Optional[str]  = None
    email: Optional[EmailStr]  = None
    password: str
