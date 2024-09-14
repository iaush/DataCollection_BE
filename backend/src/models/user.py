from sqlalchemy import create_engine, Column, Integer, String, Boolean, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from src.database.database import Base
from pydantic import BaseModel, validator
import html

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    contact_num = Column(LargeBinary, nullable=True)
    company = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    is_member = Column(Boolean, nullable=True, default=False)
    role = Column(String(50), nullable=True)

    def to_dict(self):
        return{
            "id": self.id,
            "email": self.email,
            "company": self.company,
            "name": self.name,
            "is_member": self.is_member,
            "role": self.role
        }