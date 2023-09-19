#!/usr/bin/env python3
"""app instance"""
from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}
