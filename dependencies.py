from sqlalchemy.orm import sessionmaker, Session
from models import db, User
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema


def get_db_session():
    Session = sessionmaker(bind=db)
    session = Session()
    try:
        yield session
    finally:
        session.close()


def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_db_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id= int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Access denied!, verify validation of the token")
    user = session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Access denied!")
    return user