from fastapi import FastAPI, Depends, __version__
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from utils.db import engine
from routes import customer, user, product, product_category, cart
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
    license_info={
        "name": "MIT",
        "url": "https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt",
    },
)

origins = ["http://localhost:5173", "https://veeplush-frontend.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI on Vercel</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>Hello from FastAPI@{__version__}</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
            </ul>
            <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""


@app.get("/", tags=["Welcome"])
def welcome():
    return HTMLResponse(html)


app.include_router(user.router)
app.include_router(customer.router)
app.include_router(product.router)
app.include_router(product_category.router)
app.include_router(cart.router)
