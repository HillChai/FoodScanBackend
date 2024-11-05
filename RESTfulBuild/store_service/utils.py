import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from models import Base, History, User
from datetime import datetime
from sqlalchemy import select

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("/app/Log/app.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(pathname)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


POSTGRES_URL = os.environ.get("POSTGRES_URL")
engine = create_async_engine(POSTGRES_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # 自动创建表

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
HISTORY_TOPIC = os.getenv("HISTORY_TOPIC", "history_topic")

async def process_message(image_path, presigned_url, inference_result, weight_result, openid, task_id):
    try:
        async with async_session() as session:
            # 检查 openid 是否存在于 users 表中
            user_exists = await session.execute(
                select(User).where(User.openid == openid)
            )
            if not user_exists.scalars().first():
                logger.error(f"User with openid '{openid}' does not exist.")
                return  # 或者抛出异常
            new_entry = History(
                created_at = datetime.now(),
                image_path = image_path,
                presigned_url = presigned_url,
                inference_result = inference_result,
                weight_result = weight_result,    
                openid = openid,
                task_id=task_id
            )
            session.add(new_entry)
            await session.commit()
        logger.info(f"Store history success");
    except Exception as e:
        logger.error(f"Store history failed: {e}")