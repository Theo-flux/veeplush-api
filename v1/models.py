#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String, Sequence, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type
from utils.db import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, Sequence('customer_seq'), primary_key=True, nullable=False) 
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

    # one-to-many
    orders = relationship('Order', back_populates='customer')


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, Sequence('product_cat_seq'), primary_key=True, nullable=False) 
    name = Column(String, nullable=False)

    # one-to-many relationship from product to product categories
    products = relationship('Product', back_populates='category')

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, Sequence('product_seq'), primary_key=True, nullable=False) 
    product_category_id = Column(Integer, ForeignKey('product_categories.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    length = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=False)
    style = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=False)
    stock_qty = Column(Integer)

    # many-to-one relationship from product to product categories
    category = relationship('ProductCategory', back_populates = 'products')


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, Sequence('order_seq'), primary_key=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    order_status = Column(Enum('Pending', 'delivered', 'canceled', 'shipped', name='order_status'))
    order_date = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    total_amount = Column(Float, nullable=False)

    # many-to-one relationship from order to customer
    customer = relationship('Customer', back_populates='orders')


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, Sequence('order_seq'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    sub_total = Column(Float, nullable=False)
    qty = Column(Integer, nullable=False)

    # many-to-one relationship from order to customer
    customer = relationship('Customer', back_populates='orders')