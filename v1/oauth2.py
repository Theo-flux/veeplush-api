from typing import Dict
from os import environ
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import JWTError,jwt


load_dotenv()

SECRET_KEY = environ.get('SECRET_KEY')
ALGORITHM = environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))


def generate_token(data: Dict) -> str:
    payload = data.copy()
    exp = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": exp})

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token
