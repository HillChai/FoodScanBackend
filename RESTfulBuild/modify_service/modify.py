from fastapi import FastAPI, Depends, HTTPException, status
from redis.asyncio import Redis
from utils import REDIS_HOST, REDIS_PORT, REDIS_DB, get_current_user,logger,expiration_time, async_session
import json
from models import ResultUpdateRequest, History
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text

app = FastAPI()

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


@app.on_event("startup")
async def startup():
    asyncio.create_task(check_expiring_keys())

async def check_expiring_keys():
    while True:
        # logger.info(f"Checking now...")
        # 获取 Redis 中的所有键
        keys = await redis_client.keys('*')  # 根据需要指定键的模式
        for key in keys:
            # logger.info(f"keys is not empty")
            # 获取每个键的剩余生存时间（TTL）
            ttl = await redis_client.ttl(key)
            # logger.info(f"ttl:{ttl}")
            # 检查键是否即将过期（例如，剩余时间小于或等于60秒）
            if 0 < ttl <= 60:  # 根据需要调整时间
                try:
                    logger.info(f"Key {key} is about to expire in {ttl} seconds.")
                    await update_postgres(key)
                except Exception as e:
                    logger.error(f"Error:{e}")

        await asyncio.sleep(20)  # 每60秒检查一次，调整为所需时间


async def update_postgres(task_id):
    try:
        # 从 Redis 中获取过期的数据
        result_json = await redis_client.get(task_id)
    except Exception as e:
        logger.info(f"Unable to fetch redis data")
        return
    try:
        if result_json:
            result = json.loads(result_json)
            inference_result = result.get("inference_result")
            weight_result = result.get("weight_result")
            corrected = result.get("corrected")

            if corrected:
                # 更新 PostgreSQL 中的记录
                async with async_session() as session:
                    async with session.begin():
                        # 查询相应的记录
                        query = select(History).where(History.task_id == task_id)
                        existing_record = await session.execute(query)
                        history_record = existing_record.scalars().first()

                        # 如果记录存在，则进行更新
                        if history_record:
                            await session.execute(
                                text("""
                                UPDATE history 
                                SET inference_result = :inference_result,
                                    weight_result = :weight_result
                                WHERE task_id = :task_id
                                """),
                                {
                                    "inference_result": inference_result,
                                    "weight_result": weight_result,
                                    "task_id": task_id
                                }
                            )
                            logger.info(f"Updated PostgreSQL for expired task_id: {task_id}")
                        else:
                            logger.info(f"No data found in PostgreSQL for task_id: {task_id}")
            else:
                logger.info(f"Task {task_id} is expired in Redis but not corrected.")
        else:
            logger.info(f"No data found in Redis for task_id: {task_id}")

    except Exception as e:
        logger.error(f"Error updating PostgreSQL for task_id {task_id}: {str(e)}")


@app.put("/cache_result/{task_id}")
async def set_cache_result(task_id, request: ResultUpdateRequest,  current_user_openid: str = Depends(get_current_user)):

    new_inference_result = request.inference_result
    new_weight_result = request.weight_result

    result_json = await redis_client.get(task_id)

    if result_json:
        result = json.loads(result_json)  # 使用 json.loads
        inference_result = result.get("inference_result")
        weight_result = result.get("weight_result")
        corrected = result.get("corrected")
     
        logger.info(f"Before modifying: {inference_result}, {weight_result}, {corrected}")
    
        if new_inference_result != inference_result:
            corrected = True
            inference_result = new_inference_result

        if new_weight_result != weight_result:
            corrected = True
            weight_result = new_weight_result

        if corrected:
            try:
                result = {
                    "inference_result": inference_result,
                    "weight_result": weight_result,
                    "corrected": corrected
                }
                await redis_client.set(task_id, json.dumps(result), ex=expiration_time)
                logger.info(f"Cache_result updated in Redis for task_id: {task_id}")
                return {"message": "Cache_result updated successfully"}
            except Exception as e:
                logger.error(f"Error updating result in Redis: {e}")
                return
        else:
            logger.info(f"No change in cache_result, task_id: {task_id}")


    else:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="task not found"
        )
    



    