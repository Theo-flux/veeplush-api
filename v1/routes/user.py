from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models
from utils.db import get_db
from utils.pwd_hash import get_pwd_hash, verify_pwd
from schemas import TokenSchema
from schemas.users import (
    NewUserSchema,
    UserResponseSchema
)
from oauth2 import generate_token


router = APIRouter(prefix="/user", tags=['user'])

'''@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
async def create_user(user: NewUserSchema, db: Session = Depends(get_db)):
    """create a new user"""
    user_email_exists = db.query(models.User).filter(models.User.email == user.email).first()

    if user_email_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"a user with this email: {user.email} already exists.")

    user_username_exists = db.query(models.User).filter(models.User.username == user.username).first()

    if user_username_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Username: {user.username} already taken. Try a new one.")
    

    hashed_pwd = get_pwd_hash(user.password)
    user.password = hashed_pwd

    user = user.dict()
    user.update({"role": "salesperson"})
    new_user = models.User(**user)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user'''


@router.post('/user_login', response_model=TokenSchema)
async def login_user(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    current_queried_user = db.query(models.User).filter(models.User.username == credentials.username).first()

    if not current_queried_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid details")

    if not verify_pwd(credentials.password, current_queried_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid details")
    

    token = generate_token({"id": current_queried_user.id})

    return {"access_token": token, "token_type": "beaer"}
