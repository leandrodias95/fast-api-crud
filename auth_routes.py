from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_db_session
from main import bcrypt_context
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(id: str):
    token = f"a95c4b209ff9de1b823788c95aa33f0e4f121e7e609579d552a9ea62f3a948bc{id}"
    return token

def authenticate_user(email: str, password: str, session: Session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user

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
        crypted_password = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, crypted_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return {"message": f"Usuário registrado com sucesso {new_user.email}"}

@auth_router.post("/login")
async def login(login: LoginSchema, session: Session = Depends(get_db_session)):
    user = authenticate_user(login.email, login.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = create_token(user.id)
        return {"access_token": access_token, "token_type": "Bearer"}