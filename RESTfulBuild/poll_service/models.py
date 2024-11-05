from enum import Enum
from sqlalchemy import Integer, Float, ForeignKey

class PERMISSION(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    NO_PERMISSION = "NO_PERMISSION"

from pydantic import BaseModel
class LoginRequest(BaseModel):
    code: str

from sqlalchemy import Column, String, Enum, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    openid = Column(String, primary_key=True)
    head_url = Column(String, default="")
    name = Column(String, default="")
    gold_coin = Column(Integer, default=0)
    experience = Column(Integer, default=0)
    permission = Column(Enum(PERMISSION), default=PERMISSION.NO_PERMISSION)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    email = Column(String, default="", unique=True)
    phone_number = Column(String, default="", unique=True)
    signature = Column(String, default="")

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now)
    image_path = Column(String(255), nullable=False)
    presigned_url = Column(String(2048), nullable=False)
    inference_result = Column(String(50), nullable=False)
    weight_result = Column(Float, nullable=False)
    openid = Column(String(255), ForeignKey('users.openid'), nullable=False)