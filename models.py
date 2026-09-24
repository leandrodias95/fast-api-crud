from sqlalchemy import Boolean, create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ChoiceType

db = create_engine("sqlite:///database.db")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String)
    active = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)

    def __init__(self, name: str, email: str, password: str, active: bool = True, admin: bool = False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

class  Order(Base):
    __tablename__ = "orders"

   # STATUS_ORDERS = [
   #     ("PENDING", "PENDING"),
   #     ("COMPLETED", "COMPLETED"),
   #     ("CANCELLED", "CANCELLED")
   # ]

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total = Column(Integer, nullable=False)
    #ITEMS ORDERED RELATIONSHIP

    def __init__(self, status="PENDING", user_id: int = None, total=0):
        self.status = status
        self.user_id = user_id
        self.total = total

class ItemsOrdered(Base):
    __tablename__ = "items_ordereds"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unity_price = Column(Float, nullable=False)
    size = Column(String, nullable=True)
    flavor = Column(String, nullable=True)

    def __init__(self, order_id: int = None, product_name: str = "", quantity: int = 0, unity_price: float = 0, size: str = None, flavor: str = None):
        self.order_id = order_id
        self.product_name = product_name
        self.quantity = quantity
        self.unity_price = unity_price
