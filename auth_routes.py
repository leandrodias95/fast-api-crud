from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_db_session, verify_token
from main import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

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
    """Authentication route that returns whether the user is authenticated or not."""
    return {"message": "You accessed the authentication route", "authenticated": False}

@auth_router.post("/register")
async def register(user_schema: UserSchema, session: Session = Depends(get_db_session)):
    user = None
    user = session.query(User).filter_by(email=user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        crypted_password = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, crypted_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return {"message": f"User registered successfully {new_user.email}"}

@auth_router.post("/login")
async def login(login: LoginSchema, session: Session = Depends(get_db_session)):
    user = authenticate_user(login.email, login.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User not found or invalid credentials")
    else:
        access_token = create_token(user.id, token_type="access")
        refresh_token = create_token(user.id, token_duration=timedelta(days=7), token_type="refresh")
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}

@auth_router.post("/login-form")
async def login(data_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db_session)):
    user = authenticate_user(data_form.username, data_form.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User not found or invalid credentials")
    else:
        access_token = create_token(user.id, token_type="access")
        refresh_token = create_token(user.id, token_duration=timedelta(days=7), token_type="refresh")
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}


@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(verify_token)):
    access_token = create_token(user.id, token_type="access")

    return {"access_token": access_token, "token_type": "Bearer"}