from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone_number = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    # العمود الجديد الذي أضفناه للتو بعد تفعيل Alembic للاختبار 
    address = Column(String, nullable=True)

class MenuItem(Base):
    __tablename__ = "items" 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True) 
    price = Column(Float) 
    category = Column(String)
    is_available = Column(Boolean, default=True)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id")) 
    status = Column(String, default="pending")