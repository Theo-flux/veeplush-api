from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import cast, String

from schemas.cart import (
    AddToCartSchema,
    GetCartResponseSchema,
    OrderItemSchema,
    OrderStatusSchema,
)
from schemas.customer import CustomerResponseSchema
from utils.db import get_db
from oauth2 import get_current_customer
import models


router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/orders")
async def get_cart(
    db: Session = Depends(get_db),
    current_customer: CustomerResponseSchema = Depends(get_current_customer),
):
    customer_orders = (
        db.query(models.Order)
        .filter(models.Order.customer_id == current_customer.id)
        .all()
    )

    if customer_orders:
        order_items_list = []
        for order in customer_orders:
            custormer_order_items = (
                db.query(models.OrderItem)
                .filter(models.OrderItem.order_id == order.id)
                .all()
            )

            order_items_list.append({order.order_status: custormer_order_items})

        return order_items_list

    return []


@router.post("/add_order_item")
async def add_to_cart(
    order_item: OrderItemSchema,
    db: Session = Depends(get_db),
    current_customer: CustomerResponseSchema = Depends(get_current_customer),
):
    # check if there are pending orders.
    customer_pending_orders = (
        db.query(models.Order)
        .filter(
            models.Order.customer_id == current_customer.id,
            cast(models.Order.order_status, String).ilike(OrderStatusSchema.PENDING),
        )
        .first()
    )

    if customer_pending_orders:
        # check if order_item already exists.
        customer_order_item_exists = db.query(models.OrderItem).filter(
            models.OrderItem.product_id == order_item.product_id
        )

        # if it exists just update it.
        if customer_order_item_exists.first():
            customer_order_item_exists.update(
                {
                    "length": order_item.length,
                    "style": order_item.style,
                    "qty": order_item.qty,
                    "sub_total": order_item.sub_total,
                },
                synchronize_session=False,
            )
            db.commit()

            return

        # if it doesn't exist add it to the order_item table
        order_item = order_item.dict()
        order_item.update({"order_id": customer_pending_orders.id})
        customer_order_item = models.OrderItem(**order_item)

        db.add(customer_order_item)
        db.commit()
        db.refresh(customer_order_item)

        return

    order_dict = {
        "customer_id": current_customer.id,
        "order_status": OrderStatusSchema.PENDING,
        "total_amount": 0.00,
    }

    # create an order
    customer_order = models.Order(**order_dict)

    db.add(customer_order)
    db.commit()
    db.refresh(customer_order)

    # add order_item to order
    order_item = order_item.dict()
    order_item.update({"order_id": customer_order.id})
    customer_order_item = models.OrderItem(**order_item)

    db.add(customer_order_item)
    db.commit()
    db.refresh(customer_order_item)

    return


@router.delete("/")
async def delete_item_from_cart(id: int):
    return {"message": "delete an item from cart"}
