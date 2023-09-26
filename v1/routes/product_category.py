from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends

import models
from utils.db import get_db
from schemas.product import AddProductCategorySchema
from schemas.users import UserResponseSchema
from oauth2 import get_current_user


router = APIRouter(prefix="/product_category", tags=["product_category"])


@router.get("/")
async def get_all_category(db: Session = Depends(get_db)):
    """get all product categories"""
    categories = db.query(models.ProductCategory).all()

    category_list = [category.name for category in categories]

    return category_list


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_category(
    category: AddProductCategorySchema,
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    """add a product category"""
    category_exists = (
        db.query(models.ProductCategory)
        .filter(models.ProductCategory.name == category.name)
        .first()
    )

    if category_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"category: {category.name} already exists",
        )

    new_category = models.ProductCategory(**category.dict())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    name: str,
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    """delete a product category by it's name"""
    to_delete = db.query(models.ProductCategory).filter(
        models.ProductCategory.name == name
    )

    if to_delete.first() is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"category: {name} doesn't exist",
        )

    to_delete.delete(synchronize_session=False)
    db.commit()
