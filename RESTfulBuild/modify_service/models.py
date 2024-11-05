from pydantic import BaseModel
from sqlalchemy import Integer, Float, ForeignKey, Column, String, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

class ResultUpdateRequest(BaseModel):
    inference_result:str
    weight_result:float

Base = declarative_base()

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