from fastapi import Form, UploadFile, File
from typing import List, Dict, Annotated
from pydantic import BaseModel, Field


class AddProductCategorySchema(BaseModel):
    name: str = Field(min_length=4)


class AddNewProductSchema(BaseModel):
    product_category: str = Form("product_category")
    name: str = Form()
    image: UploadFile = File(...)
    description: str = Form()
    price: float = Form()
    length: Dict[str, int] = Form()
    style: Dict[str, str] = Form()
    stock_qty: int = Form()
