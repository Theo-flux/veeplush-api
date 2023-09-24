from typing import List, Union
from pydantic import BaseModel, Field


class AddProductCategorySchema(BaseModel):
    name: str = Field(min_length=4)
