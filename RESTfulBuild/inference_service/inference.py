import asyncio
from utils import REDIS_HOST, REDIS_PORT, REDIS_DB, IMAGE_TOPIC, KAFKA_BROKER
from redis.asyncio import Redis
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
from utils import logger,minio_client,BUCKET_NAME, classifier, weight_estimator, HISTORY_TOPIC, expiration_time
from PIL import Image
import io


async def process_message(message):
    message_data = json.loads(message.value.decode("utf-8"))
    logger.info(f"message_data:{message_data}")
    task_id = message_data["task_id"]
    image_path = message_data["image_path"]
    openid = message_data["openid"]
    presigned_url = message_data["presigned_url"]

    logger.info(f"Processing message for task_id: {task_id}, image_path: {image_path}")

    image_file = image_path.split("/")[-1]

    try:
        # 从 MinIO 获取对象：
        response = await asyncio.to_thread(minio_client.get_object, BUCKET_NAME, image_file)
        # 读取图像数据：
        image_data = await asyncio.to_thread(response.read)
        # 关闭响应对象：
        await asyncio.to_thread(response.close)
        # 释放连接：
        await asyncio.to_thread(response.release_conn)
    except Exception as e:
        logger.error(f"Error fetching image from MinIO: {e}")
        return
    
    try:
        image = Image.open(io.BytesIO(image_data))
        inference_result = await asyncio.to_thread(classifier.predict_image, image)
        weight_result = await asyncio.to_thread(weight_estimator.estimate_weight, image)
        logger.info(f"Inference result: {inference_result}, Weight result: {weight_result}")
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return  
    
    try:
        result = {
            "inference_result": inference_result,
            "weight_result": weight_result,
            "corrected": False
        }
        await redis_client.set(task_id, json.dumps(result), ex=expiration_time)
        logger.info(f"Result stored in Redis for task_id: {task_id}")
    except Exception as e:
        logger.error(f"Error storing result in Redis: {e}")
        return
    
    # 存入数据库的是7天有效期的
    try: 
        save_message = {
            "image_path": image_path,
            "presigned_url": presigned_url,
            "inference_result": inference_result,
            "weight_result": weight_result,
            "openid": openid,
            "task_id": task_id
        }
        logger.info(f"Sending to history_topic: {save_message}")
        await producer.send_and_wait(HISTORY_TOPIC, value=save_message)
        logger.info(f"Sent to history_topic: {save_message}")
    except Exception as e:
        logger.error(f"Error saving to history_topic: {e}")
        return


async def main():
    global redis_client
    redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    consumer = AIOKafkaConsumer(
        IMAGE_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        group_id="inference_service",
        auto_offset_reset="earliest",
        enable_auto_commit=True
    )
    
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    await consumer.start()
    await producer.start()

    try:
        async for message in consumer:
            await process_message(message)
    finally:
        await consumer.stop()
        await producer.stop()
        await redis_client.close()

if __name__ == "__main__":
    asyncio.run(main())