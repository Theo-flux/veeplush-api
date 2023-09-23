#!/usr/bin/env python3
"""app instance"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from utils.db import engine
from routes import customer
import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Veeplush api",
    description="This is my ALX webstack portfolio project",
    summary="My first attempt at implementing api service. Also my first attempt at implementing an ecommerce api service as well",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Theo Flux",
        "url": "http://www.github.com/Theo-flux",
        "email": "tifluse@gmail.com",
    },
    license_info={
        "name": "BSD 2 Clause",
        "url": "https://opensource.org/license/bsd-2-clause/",
    },
)

app.include_router(customer.router)

@app.get("/")
def root():
    return {"message": "root route"}
