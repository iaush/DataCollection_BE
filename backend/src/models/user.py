from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from src.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    contact_num = Column(Integer, nullable=True)
    company = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    is_member = Column(Boolean, nullable=True)
    role = Column(String(50), nullable=True)