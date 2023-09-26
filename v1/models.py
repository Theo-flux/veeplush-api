#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String, Sequence, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type
from utils.db import Base


class User(Base):
    """User for accessing database products

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "users"

    id = Column(Integer, Sequence("user_seq"), primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum("admin", "salesperson", name="role", nullable=False))
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), onupdate=text("now()")
    )


class Customer(Base):
    """customers account.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "customers"

    id = Column(Integer, Sequence("customer_seq"), primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, default="")
    last_name = Column(String, default="")
    phone_number = Column(String, default="")
    shipping_address = Column(String, default="")
    country = Column(String, default="")
    city = Column(String, default="")
    state = Column(String, default="")
    postal_code = Column(String, default="")
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), onupdate=text("now()")
    )

    # one-to-many
    orders = relationship("Order", back_populates="customer")
    payment = relationship("Payment", back_populates="customer")


class ProductCategory(Base):
    """product category table.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "product_categories"

    id = Column(Integer, Sequence("product_cat_seq"), primary_key=True, nullable=False)
    name = Column(String, nullable=False)

    # one-to-many relationship from product to product categories
    products = relationship("Product", back_populates="category")


class Product(Base):
    """product table.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "products"

    id = Column(Integer, Sequence("product_seq"), primary_key=True, nullable=False)
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    product_category_id = Column(
        Integer, ForeignKey("product_categories.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    length = Column(JSONB)
    style = Column(JSONB)
    stock_qty = Column(Integer, nullable=False)

    # a particular product can only belong to one category
    category = relationship("ProductCategory", back_populates="products")


class Order(Base):
    """Orders table.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "orders"

    id = Column(Integer, Sequence("order_seq"), primary_key=True, nullable=False)
    customer_id = Column(
        Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False
    )
    order_status = Column(
        String,
        nullable=False,
    )
    order_date = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    total_amount = Column(Float, nullable=False)

    # one-to-one relationship from order to customer
    customer = relationship("Customer", back_populates="orders")
    order_item = relationship("OrderItem", back_populates="order")
    shipment = relationship("Shipment", back_populates="orders")
    payment = relationship("Payment", back_populates="order")


class OrderItem(Base):
    """Individual order item table.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "order_items"

    id = Column(Integer, Sequence("order_seq"), primary_key=True)
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    sub_total = Column(Float, nullable=False)
    length = Column(Integer, nullable=False)
    style = Column(String, nullable=False)
    qty = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_item")


class Shipment(Base):
    """shipment table for a particular order.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "shipments"

    id = Column(Integer, Sequence("order_seq"), primary_key=True)
    order_id = Column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )

    orders = relationship("Order", back_populates="shipment")


class Payment(Base):
    """Payment table

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "payments"

    id = Column(Integer, Sequence("order_seq"), primary_key=True)
    customer_id = Column(
        Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False
    )
    order_id = Column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    payment_date = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    payment_method = Column(String, nullable=False)
    transaction_id = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="payment")
    customer = relationship("Customer", back_populates="payment")
