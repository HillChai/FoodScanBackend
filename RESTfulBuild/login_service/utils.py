import logging
import os
import aiohttp
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User, PERMISSION
from datetime import datetime, timedelta
import jwt
from cryptography.hazmat.primitives import serialization
import uuid

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("/app/Log/app.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(pathname)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

APPID = os.environ.get("APPID")
SECRET = os.environ.get("SECRET")
async def get_openid(code: str):
    # url = f"https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={code}&grant_type=authorization_code"
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url) as response:
    #         if response.status == 200:
    #             text = await response.text()
    #             logger.info(f"Received openid: {text}")
    #             try:
    #                 data = json.loads(text)
    #                 openid = data.get("openid")
    #                 logger.info(f"Openid: {openid}")
    #                 return openid
    #             except json.JSONDecodeError:
    #                 logger.error(f"Failed to decode JSON: {text}")
    # logger.error("Failed to get openid")
    return "test2"

async def check_user_from_db(openid: str, db: AsyncSession):
    result = await db.execute(select(User).filter(User.openid == openid))
    user = result.scalar_one_or_none()
    
    if user is None:
        # 如果用户不存在，创建新用户
        new_user = User(
            openid=openid, 
            head_url = "",
            name = "用户"+str(uuid.uuid4()),
            gold_coin = 10,
            experience = 100,
            permission=PERMISSION.USER,
            created_at=datetime.now(), 
            updated_at=datetime.now(),
            email="",
            phone_number="",
            signature=""
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    else:
        # 如果用户存在，更新用户的更新时间
        user.updated_at = datetime.now()
        await db.commit()
        return user


JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "RS256")
JWT_PRIVATE_KEY = os.environ.get("JWT_PRIVATE_KEY", "./keys/private.pem")
JWT_EXPIRATION_DAYS = os.environ.get("JWT_EXPIRATION_DAYS", 1)  
JWT_EXPIRATION_DELTA = timedelta(days=int(JWT_EXPIRATION_DAYS))
def create_jwt_token(openid: str, permission: PERMISSION):
    payload = {
        "openid": openid,
        "permission": permission,
        "exp": datetime.now() + JWT_EXPIRATION_DELTA
    }
    # Read the private key from the file
    with open(JWT_PRIVATE_KEY, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return jwt.encode(payload, private_key, algorithm=JWT_ALGORITHM)
    
        

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

POSTGRES_URL = os.environ.get("POSTGRES_URL")

engine = create_async_engine(POSTGRES_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
# 依赖注入，每个请求都有自己的session，会话使用后被正确关闭
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session