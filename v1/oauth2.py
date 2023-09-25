from os import environ
from typing import Dict
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from utils.db import get_db
import models
from schemas.users import UserResponseSchema
from schemas.customers import CustomerResponseSchema


load_dotenv()

SECRET_KEY = environ.get('SECRET_KEY')
ALGORITHM = environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

oauth2_user_scheme = OAuth2PasswordBearer(tokenUrl="user_login")
oauth2_customer_scheme = OAuth2PasswordBearer(tokenUrl="login")


def generate_token(data: Dict) -> str:
    payload = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": exp})

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")

        if id is None:
            raise credentials_exception

        return id
    except JWTError:
        raise credentials_exception


def get_current_user(
    token: str = Depends(oauth2_user_scheme),
    db: Session = Depends(get_db)
) -> UserResponseSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="unauthorized!",
        headers={"WWW-Authenticate": "Bearer"}
    )
    user_id = verify_token(token, credentials_exception)
    current_user: UserResponseSchema = db.query(models.User).filter(models.User.id == user_id).first()

    return current_user    


def get_current_customer(
    token: str = Depends(oauth2_customer_scheme),
    db: Session = Depends(get_db)
) -> CustomerResponseSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="unauthorized!",
        headers={"WWW-Authenticate": "Bearer"}
    )
    customer_id = verify_token(token, credentials_exception)
    current_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()

    return current_customer
