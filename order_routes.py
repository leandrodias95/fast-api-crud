from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def orders():
    """Rota de pedidos que retorna a lista de pedidos. Todas as rotas de pedidos precisam de autenticação."""
    return {"message": "Você acessou a rota de pedidos"}