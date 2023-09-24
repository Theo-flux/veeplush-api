from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from oauth2 import get_current_user
import models


router = APIRouter(prefix="/product", tags=['product'])


@router.post("/create")
async def add_product(user_id: int = Depends(get_current_user)):
    return user_id