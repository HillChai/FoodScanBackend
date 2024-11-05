from fastapi import FastAPI, HTTPException, Query, Depends
from redis.asyncio import Redis
from utils import logger, REDIS_HOST, REDIS_PORT, REDIS_DB, get_current_user, async_session, select
import json
from models import History

app = FastAPI()

@app.on_event("startup")
async def startup():
    global redis_client
    redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

@app.get("/result")
async def poll(
    task_id: str = Query(...),     
    current_user_openid: str = Depends(get_current_user)  # 添加 JWT 认证
):
    try:
        result_json = await redis_client.get(task_id)

        if result_json:
            result = json.loads(result_json)  # 使用 json.loads
            inference_result = result.get("inference_result")
            weight_result = result.get("weight_result")
            corrected = result.get("corrected")

            if inference_result and weight_result:
                return {"inference_result": inference_result, "weight_result": weight_result, "corrected":corrected}
            else:
                if not inference_result:
                    return {"detail": "inference_result not found", "weight_result": weight_result, "corrected":corrected}
                if not weight_result:
                    return {"detail": "weight_result not found", "inference_result": inference_result, "corrected":corrected}
                raise HTTPException(status_code=404, detail="No result for the task_id")
        else:
            raise HTTPException(status_code=404, detail="No result for the task_id")
    except Exception as e:
        logger.error(f"No result for task_id: {task_id}, and error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@app.get("/currentuser")
async def poll_current_user_history(current_user_openid: str = Depends(get_current_user)):
    try:
        async with async_session() as session:
            result = await session.execute(select(History).where(History.openid==current_user_openid))
            current_user_history = result.scalars().all()

            if current_user_history:
                return [{"created_at": instance.created_at,
                    "image_path": instance.image_path,
                    "presigned_url": instance.presigned_url,
                    "inference_result": instance.inference_result,
                    "weight_result": instance.weight_result} 
                    for instance in current_user_history]
            else:
                raise HTTPException(status_code=404, detail="No history found for the current user")
    except Exception as e:
        logger.error(f"Error fetch history for openid: {current_user_openid}, error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# 在应用关闭时关闭 Redis 连接
@app.on_event("shutdown")
async def shutdown_event():
    await redis_client.close()
