from fastapi import APIRouter, Depends
from models import User
from dependencies import get_db_session
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """Rota de autenticação que retorna se o usuário está autenticado ou não."""
    return {"message": "Você acessou a rota de autenticação", "authenticated": False}

@auth_router.post("/register")
async def register(email: str, password: str, name: str, session = Depends(get_db_session)):
    user = None
    user = session.query(User).filter_by(email=email).first()
    if user:
        return {"message": "Usuário já existe"}
    else:
        new_user = User(name, email, password)
        session.add(new_user)
        session.commit()
    return {"message": "Usuário registrado com sucesso"}
