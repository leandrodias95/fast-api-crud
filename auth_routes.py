from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_db_session
from main import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(id: str, token_duration: Any | None = None, token_type: str = "access"):
    # JWT
    # user id
    # experation_date
    if not token_duration: 
        token_duration = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expiration = datetime.now(timezone.utc) + token_duration
    payload = {"sub": str(id), "exp": expiration, "type": token_type}
    encode_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

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
        access_token = create_token(user.id, token_type="access")
        refresh_token = create_token(user.id, token_duration=timedelta(days=7), token_type="refresh")
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}

@auth_router.get("/refresh")
async def use_refresh_token(refresh_token: str, session: Session = Depends(get_db_session)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Token inválido")

        user = verify_refresh_token(payload, session)

        if not user:
            raise HTTPException(status_code=400, detail="Token inválido")

        access_token = create_token(user.id, token_type="access")

        return {"access_token": access_token, "token_type": "Bearer"}

    except JWTError:
        raise HTTPException(status_code=400, detail="Token inválido")

def verify_refresh_token(token, session: Session = Depends(get_db_session)):
    user = session.query(User).filter_by(id=int(token.get("sub"))).first()
    if not user:
        return False
    return user