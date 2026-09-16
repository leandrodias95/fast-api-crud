from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_db_session
from security import hash_password
from schemas import UserSchema
from sqlalchemy.orm import Session
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """Rota de autenticação que retorna se o usuário está autenticado ou não."""
    return {"message": "Você acessou a rota de autenticação", "authenticated": False}

@auth_router.post("/register")
async def register(user_schema: UserSchema, session: Session = Depends(get_db_session)):
    user = None
    user = session.query(User).filter_by(email=user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    else:
        crypted_password = hash_password(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, crypted_password)
        session.add(new_user)
        session.commit()
    return {"message": f"Usuário registrado com sucesso {new_user.email}"}
