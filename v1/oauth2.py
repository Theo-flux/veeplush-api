from typing import Dict
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from os import environ
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import JWTError, jwt


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


def get_current_user(token: str = Depends(oauth2_user_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="unauthorized!",
        headers={"WWW-Authenticate": "Bearer"}
    )

    return verify_token(token, credentials_exception)


def get_current_customer(token: str = Depends(oauth2_customer_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="unauthorized!",
        headers={"WWW-Authenticate": "Bearer"}
    )

    return verify_token(token, credentials_exception)