from fastapi import APIRouter, Depends, HTTPException
from models import Order, User
from sqlalchemy.orm import Session
from dependencies import get_db_session, verify_token
from schemas import OrderSchema


order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verify_token)])

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

@order_router.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(get_db_session), user:User=Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if user.admin is False and order.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to cancel this order")
    order.status = "CANCELED"
    session.commit()
    return {
            "message": f"Order canceled successfully, number order {order.id}",
            "order": order
            }