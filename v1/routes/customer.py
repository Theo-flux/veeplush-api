from typing import List
from pydantic import EmailStr
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from oauth2 import generate_token, get_current_customer
from utils.db import get_db
from utils.pwd_hash import get_pwd_hash, verify_pwd
import models
from schemas import TokenSchema
from schemas.customer import (
    NewCustomerSchema,
    CustomerLoginSchema,
    CustomerResponseSchema,
    CustomerInfoSchema,
)


router = APIRouter(prefix="/customer", tags=["customer"])


@router.get("/all", response_model=int)
async def customers(db: Session = Depends(get_db)):
    """get the number of customers available"""
    customers = db.query(models.Customer).count()

    return customers


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomerResponseSchema,
)
async def create_customer(customer: NewCustomerSchema, db: Session = Depends(get_db)):
    """create a new customer"""
    customer_email_exists = (
        db.query(models.Customer)
        .filter(models.Customer.email == customer.email)
        .first()
    )

    if customer_email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"email: {customer.email} exists.",
        )

    customer_username_exists = (
        db.query(models.Customer)
        .filter(models.Customer.username == customer.username)
        .first()
    )

    if customer_username_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username: {customer.username} taken. Try a new one.",
        )

    hashed_pwd = get_pwd_hash(customer.password)
    customer.password = hashed_pwd

    new_customer = models.Customer(**customer.dict())

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


@router.post("/login", response_model=TokenSchema)
async def login_customer(
    credentials: CustomerLoginSchema, db: Session = Depends(get_db)
):
    """a path operation to login customers via their credentials."""
    print(credentials)
    customer = {}
    if credentials.username:
        customer = (
            db.query(models.Customer)
            .filter(models.Customer.username == credentials.username)
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="invalid details!"
            )

    if credentials.email:
        customer = (
            db.query(models.Customer)
            .filter(models.Customer.email == credentials.email)
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="invalid details!"
            )

    if not verify_pwd(credentials.password, customer.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid details!"
        )

    token = generate_token({"id": customer.id})

    return {"access_token": token, "token_type": "Bearer"}


@router.get("/me", response_model=CustomerResponseSchema)
async def get_customer(customer=Depends(get_current_customer)):
    """get a customer"""
    return customer


@router.post(
    "/update_info",
    response_model=CustomerResponseSchema,
)
async def update_customer_info(
    info: CustomerInfoSchema,
    db: Session = Depends(get_db),
    customer=Depends(get_current_customer),
):
    """update customer info"""
    print(info)
    customer_info = db.query(models.Customer).filter(models.Customer.id == customer.id)

    if not customer_info.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if customer_info.first():
        customer_info.update(info.dict(), synchronize_session=False)
        db.commit()
        return customer
