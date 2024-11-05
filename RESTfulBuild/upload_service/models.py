from sqlalchemy import Integer, Float, ForeignKey, Column, String, TIMESTAMP, func, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from enums import PERMISSION
from datetime import datetime
from pydantic import BaseModel, EmailStr

Base = declarative_base()

class UserInfoUpdateRequest(BaseModel):
    name: str
    phone_number: str
    email: EmailStr
    signature: str
    gold_coin: int
    experience : int

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
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    image_path = Column(String(255), nullable=False)
    inference_result = Column(String(50), nullable=False)  # 可根据需要调整长度
    presigned_url = Column(String(2048), nullable=False)
    weight_result = Column(Float, nullable=False)
    openid = Column(String, ForeignKey('users.openid'), nullable=False)  # 与 User 表保持一致
