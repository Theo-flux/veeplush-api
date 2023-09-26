from enum import Enum
from typing import Optional
from pydantic import EmailStr, BaseModel, Field
from datetime import datetime


class Role(str, Enum):
    SALESPERSON = "salesperson"
    ADMIN = "admin"


class NewUserSchema(BaseModel):
    email: EmailStr
    username: str = Field(min_length=4)
    password: str = Field(min_length=8)


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Role
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerLoginSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str
