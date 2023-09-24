import json
from typing import Dict
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from oauth2 import get_current_user
import models
from schemas.product import AddNewProductSchema
from schemas.users import UserResponseSchema


router = APIRouter(prefix="/product", tags=['product'])

def dict_to_json(data: Dict):
    return json.dumps(data)

def get_url(img):
    pass


@router.post("/create")
async def add_product(
    product_category: str = Form("product_category"),
    name: str = Form("name"),
    image: UploadFile = File(...),
    description: str = Form("description"),
    price: float = Form("price"),
    length: str = Form(),
    style: str = Form(),
    stock_qty: int = Form("stock_qty"),
    user_id: UserResponseSchema = Depends(get_current_user)
):
    return {product_category, length, style}
