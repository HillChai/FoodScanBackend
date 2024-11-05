import logging
import os
from minio import Minio, S3Error
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from cryptography.hazmat.primitives import serialization
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("/app/Log/app.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(pathname)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# 从环境变量读取 MinIO 和 Kafka 配置
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "foodkafka:9092")
BUCKET_NAME = os.getenv("BUCKET_NAME", "photos")

EXTERNAL_MINIO_ENDPOINT = os.getenv("EXTERNAL_MINIO_ENDPOINT")
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "minioadmin")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "minio123")

# 初始化 内部容器用的MinIO 客户端
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ROOT_USER,
    secret_key=MINIO_ROOT_PASSWORD,
    secure=False
)

# 初始化 内部容器用的MinIO 客户端
external_minio_client = Minio(
    EXTERNAL_MINIO_ENDPOINT,
    access_key=MINIO_ROOT_USER,
    secret_key=MINIO_ROOT_PASSWORD,
    secure=False
)

from datetime import timedelta
# 生成签名 URL，过期时间设为30天，30天下载一次到训练数据库
def generate_presigned_url(bucket_name, object_name, expiry=timedelta(days=7)):
    logger.info(f"EXTERNAL_MINIO_ENDPOINT: {EXTERNAL_MINIO_ENDPOINT}")
    try:
        url = external_minio_client.presigned_get_object(bucket_name, object_name, expires=expiry)
        logger.info(f"presigned_url:{url}")
    except Exception as e:
        logger.error(f"Error while generating external url:{e}")
        raise e
    return url

# 检查并创建桶（如果不存在）
async def check_and_create_bucket():
    try:
        if not minio_client.bucket_exists(BUCKET_NAME):
            minio_client.make_bucket(BUCKET_NAME)
            print(f"已创建桶 '{BUCKET_NAME}'。")
        else:
            print(f"桶 '{BUCKET_NAME}' 已存在。")
    except S3Error as e:
        print("发生错误：", e)


producer = None

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


KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "image_topic")


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
POSTGRES_URL = os.environ.get("POSTGRES_URL")

engine = create_async_engine(POSTGRES_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)