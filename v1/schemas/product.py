from fastapi import Form, UploadFile, File
from typing import List, Dict, Annotated
from pydantic import BaseModel, Field


class AddProductCategorySchema(BaseModel):
    name: str = Field(..., min_length=4)


class ProductCategorySchema(BaseModel):
    name: str = Field(..., min_length=4)
