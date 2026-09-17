from fastapi import APIRouter, Depends, HTTPException
from models import Order
from sqlalchemy.orm import Session
from dependencies import get_db_session
from schemas import OrderSchema


order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def orders():
    """Rota de pedidos que retorna a lista de pedidos. Todas as rotas de pedidos precisam de autenticação."""
    return {"message": "Você acessou a rota de pedidos"}

@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_db_session)):
    new_order = Order(
        user_id=order_schema.user_id, 
    )
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return {"message": "Pedido criado com sucesso", "order": {"id": new_order.id}}