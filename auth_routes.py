from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    """Rota de autenticação que retorna se o usuário está autenticado ou não."""
    return {"message": "Você acessou a rota de autenticação", "authenticated": False}
