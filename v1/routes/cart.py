from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.cart import AddToCartSchema
from utils.db import get_db
from oauth2 import get_current_customer


router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/")
async def get_cart():
    return {"message": "all items in cart"}


@router.post("/")
async def add_to_cart(
    db: Session = Depends(get_db),
    current_customer: CustomerResponseSchema = Depends(get_current_customer),
):
    return {"message": "add items to cart"}


@router.delete("/")
async def delete_item_from_cart(id: int):
    return {"message": "delete an item from cart"}
