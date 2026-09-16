##incia o servidor: 
##uvicorn main:app --reload  

from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)
#endpoint

#orders
