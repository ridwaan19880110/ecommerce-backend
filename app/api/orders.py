# app/api/orders.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import models
from uuid import UUID
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter()


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic schema for creating an order
class OrderCreate(BaseModel):
    buyer_id: UUID
    product_id: int
    quantity: int
    delivery_slot: datetime


# GET all orders
@router.get("/orders", response_model=List[dict])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return [order.__dict__ for order in orders]


# POST new order
@router.post("/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_price = product.price * order.quantity
    new_order = models.Order(
        buyer_id=order.buyer_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total_price,
        status='pending',
        delivery_slot=order.delivery_slot,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"message": "Order created", "order_id": new_order.id}
