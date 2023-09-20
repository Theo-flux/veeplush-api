#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String, Sequence, Float, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type
from utils.db import Base


class Customer(Base):
    __tablename__ = "cutsomers"

    id = Column(Integer, Sequence('customer_seq'), primary_key=True) 
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, default="")
    phone_number = Column(String, default="")
    shipping_address = Column(String, default="")
    country = Column(String, default="")
    city = Column(String, default="")
    state = Column(String, default="")
    postal_code = Column(String, default="")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, Sequence('product_cat_seq'), primary_key=True) 
    name = Column(String, nullable=False)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, Sequence('product_seq'), primary_key=True) 
    product_category_id = Column(Integer, ForeignKey('product_categories.id'))
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float)
    length = Column(mutable_json_type(dbtype=JSONB, nested=True))
    style = Column(mutable_json_type(dbtype=JSONB, nested=True))
    stock_qty = Column(Integer)
