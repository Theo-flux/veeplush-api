#!/usr/bin/env python3
"""app instance"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from utils.db import engine, get_db
import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "Hello World"}
