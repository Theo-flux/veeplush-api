#!/usr/bin/env python3
"""app instance"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from utils.db import engine
from routes import customer, user, products, product_category, cart
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

app.include_router(user.router)
app.include_router(customer.router)
app.include_router(products.router)
app.include_router(product_category.router)
app.include_router(cart.router)


@app.get("/")
def root():
    return {"message": "root route"}
