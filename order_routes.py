from fastapi import APIRouter, Depends, HTTPException
from models import Order
from sqlalchemy.orm import Session
from dependencies import get_db_session
from schemas import OrderSchema


order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def orders():
    """Orders route that returns the list of orders. All order routes require authentication."""
    return {"message": "You accessed the orders route"}

@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_db_session)):
    new_order = Order(
        user_id=order_schema.user_id, 
    )
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return {"message": "Order created successfully", "order": {"id": new_order.id}}