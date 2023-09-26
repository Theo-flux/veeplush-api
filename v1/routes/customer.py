from typing import List
from pydantic import EmailStr
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from oauth2 import generate_token
from utils.db import get_db
from utils.pwd_hash import get_pwd_hash, verify_pwd
import models
from schemas import TokenSchema
from schemas.customer import (
    NewCustomerSchema,
    CustomerLoginSchema,
    CustomerResponseSchema,
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
            detail=f"a user with this email: {customer.email} already exists.",
        )

    customer_username_exists = (
        db.query(models.Customer)
        .filter(models.Customer.username == customer.username)
        .first()
    )

    if customer_username_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username: {customer.username} already taken. Try a new one.",
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


@router.get("/", response_model=CustomerResponseSchema)
async def get_customer(email: EmailStr, db: Session = Depends(get_db)):
    """get a particular customer by their email"""
    customer_by_mail = (
        db.query(models.Customer).filter(models.Customer.email == email).first()
    )

    if customer_by_mail is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"user with this email:{email} does not exist!",
        )

    return customer_by_mail
