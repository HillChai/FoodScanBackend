import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from cryptography.hazmat.primitives import serialization
from jose.exceptions import ExpiredSignatureError
from jose import JWTError, jwt
import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("/app/Log/app.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(pathname)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

JWT_PUBLIC_KEY = os.environ.get("JWT_PUBLIC_KEY")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_current_user(token: str = Depends(oauth2_scheme)):
    if not JWT_PUBLIC_KEY:
        raise HTTPException(status_code=401, detail="JWT_PUBLIC_KEY is not set")
    # Read the private key from the file
    with open(JWT_PUBLIC_KEY, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    try:
        payload = jwt.decode(token, public_key, algorithms=[JWT_ALGORITHM])
        logger.info(f"JWT decode success")

    except ExpiredSignatureError:
        # Token 过期
        logger.error(f"JWT token has expired")
        raise HTTPException(status_code=401, detail="Token has expired")
    
    except JWTError as e:
        logger.info(f"JWT decode failed: {e}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user_openid = payload.get("openid")
    if not user_openid:
        raise HTTPException(status_code=401, detail="Could not validate user_openid")
    return user_openid

#过期时间单位(秒)
expiration_time = 60


POSTGRES_URL = os.environ.get("POSTGRES_URL")
engine = create_async_engine(POSTGRES_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

