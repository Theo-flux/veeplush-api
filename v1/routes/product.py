import json
from os import getenv
from typing import Dict
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader as cloud_uploader
from PIL import Image
from io import BytesIO

from oauth2 import get_current_user
import models
from schemas.user import UserResponseSchema
from utils.db import get_db


load_dotenv()

CLOUDINARY_NAME = getenv("CLOUDINARY_NAME")
CLOUDINARY_API_KEY = getenv("CLOUDINARY_API_KEY")
CLOUDINARY_SECRET_KEY = getenv("CLOUDINARY_SECRET_KEY")

cloudinary.config(
    cloud_name=CLOUDINARY_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_SECRET_KEY,
)


router = APIRouter(prefix="/product", tags=["product"])


def get_json_from_bytes(data: bytes):
    """converts byte to json serializable format"""
    return json.loads(data.decode("utf-8"))


async def get_url(picture: File):
    """uploads product image and returns the url"""
    product_image = Image.open(picture.file)
    cloud_image = BytesIO()
    img_format = picture.filename.split(".")[1].upper()

    if img_format == "JPG":
        img_format = "JPEG"

    product_image.save(cloud_image, img_format)
    cloud_image.seek(0)

    result = cloud_uploader.upload(
        cloud_image, folder="veeplush", crop="scale", width=800
    )

    return result.get("url")


@router.post("/create")
async def add_product(
    product_category_name: str = Form(...),
    name: str = Form(...),
    image: UploadFile = File(...),
    description: str = Form(...),
    price: float = Form(...),
    length: bytes = Form(...),
    style: bytes = Form(...),
    stock_qty: int = Form(...),
    db: Session = Depends(get_db),
    user: UserResponseSchema = Depends(get_current_user),
):
    """path params for adding product to database.
    only admins can access this route.
    """
    prod_cat = (
        db.query(models.ProductCategory)
        .filter(models.ProductCategory.name == product_category_name)
        .first()
    )

    if not prod_cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product category: {product_category_name} doesn't exist",
        )

    image_url: str = await get_url(image)

    length_data = get_json_from_bytes(length)
    style_data = get_json_from_bytes(style)

    product_dict = {
        "owner_id": user.id,
        "product_category_id": prod_cat.id,
        "name": name,
        "image": image_url,
        "description": description,
        "price": price,
        "length": length_data,
        "style": style_data,
        "stock_qty": stock_qty,
    }

    new_product = models.Product(**product_dict)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product
