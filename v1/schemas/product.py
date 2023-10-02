from fastapi import Form, UploadFile, File
from typing import List, Dict, Annotated, Dict 
from pydantic import BaseModel, Field


class AddProductCategorySchema(BaseModel):
    name: str = Field(..., min_length=4)


class ProductCategorySchema(BaseModel):
    name: str = Field(..., min_length=4)


class ProductResponseSchema(BaseModel):
    product_category_id: int
    image: str
    price: float
    style: Dict
    name: str
    id: int
    description: str
    length: Dict
    stock_qty: int
