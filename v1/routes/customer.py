from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from utils.db import get_db
from utils.pwd_hash import get_pwd_hash
import models
from schemas.customers_schema import NewCustomer, CustomerResponse


router = APIRouter(prefix="/customer", tags=['customers'])

@router.get("/", response_model=List[CustomerResponse])
async def customers(db: Session = Depends(get_db)):
    """get all customers from database

    Args:
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    customers = db.query(models.Customer).all()

    return customers

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CustomerResponse)
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
