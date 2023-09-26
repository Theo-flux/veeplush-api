from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from utils.db import engine
from routes import customer, user, products, product_category, cart
import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Veeplush api",
    description="Veeplush Ecommerce API Service.",
    summary="ALX Webstack-project: backend specialization.",
    version="0.0.1",
    contact={
        "name": "Theo Flux",
        "url": "http://www.github.com/Theo-flux",
        "email": "tifluse@gmail.com",
    },
    # license_info={
    #     "name": "BSD 2 Clause",
    #     "url": "https://opensource.org/license/bsd-2-clause/",
    # },
)


@app.get("/", tags=["Welcome"])
def welcome():
    return {"message": "welcome to my world"}


app.include_router(user.router)
app.include_router(customer.router)
app.include_router(products.router)
app.include_router(product_category.router)
app.include_router(cart.router)
