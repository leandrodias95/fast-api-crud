from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    admin: Optional[bool] = False
    active: Optional[bool] = True

    class Config:
        from_attributes = True

class OrderSchema(BaseModel):
    user_id: int
    status: Optional[str] = "PENDING"
    price: Optional[float] = 0


    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True