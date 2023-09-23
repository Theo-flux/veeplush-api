from typing import List
from pydantic import EmailStr
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from oauth2 import generate_token
from utils.db import get_db
from utils.pwd_hash import get_pwd_hash, verify_pwd
import models
from schemas.customers_schema import (
    NewCustomer,
    CustomerLogin,
    CustomerResponse
)


router = APIRouter(prefix="/customer", tags=['customers'])

@router.get("/all", response_model=int)
async def customers(db: Session = Depends(get_db)):
    """get the number of customers available

    Args:
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    customers = db.query(models.Customer).count()

    return customers


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=CustomerResponse)
async def create_customer(customer: NewCustomer, db:Session = Depends(get_db)):
    """create a new customer

    Args:
        customer (NewCustomer): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    customer_email_exists = db.query(models.Customer).filter(models.Customer.email == customer.email).first()

    if customer_email_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"a user with this email: {customer.email} already exists.")
    
    customer_username_exists = db.query(models.Customer).filter(models.Customer.username == customer.username).first()

    if customer_username_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Username: {customer.username} already taken. Try a new one.")
    

    # hash pwd
    hashed_pwd = get_pwd_hash(customer.password)
    customer.password = hashed_pwd

    # create customer
    new_customer = models.Customer(**customer.dict())

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer

@router.post("/login")
async def login_customer(credentials: CustomerLogin, db: Session = Depends(get_db)):
    customer = {}
    if credentials.username:
        customer = db.query(models.Customer).filter(models.Customer.username == credentials.username).first()

        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user doesn't exist!")
    
    if credentials.email:
        customer_email = db.query(models.Customer).filter(models.Customer.email == credentials.email).first()

        if not customer_email:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user doesn't exist!")

    if not verify_pwd(credentials.password, customer.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user doesn't exist!")
    
    token = generate_token({"user_id": customer.id})

    return {"access_token": token, "type": "Bearer"}


@router.get('/', response_model=CustomerResponse)
async def get_customer(email: EmailStr, db: Session = Depends(get_db)):

    customer_by_mail = db.query(models.Customer).filter(models.Customer.email == email).first()

    if customer_by_mail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with this email:{email} does not exist!")
    
    return customer_by_mail
