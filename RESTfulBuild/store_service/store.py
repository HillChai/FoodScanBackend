import asyncio
from utils import create_db_tables, logger, process_message, KAFKA_BROKER, HISTORY_TOPIC
from aiokafka import AIOKafkaConsumer
import json

async def consume_messages():
    await create_db_tables()

    consumer = AIOKafkaConsumer(
        HISTORY_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='store_service'
    )

    await consumer.start()

    try:
        async for message in consumer:
            message_data = json.loads(message.value.decode('utf-8'))
            image_path = message_data['image_path']
            presigned_url = message_data['presigned_url']
            inference_result = message_data['inference_result']
            weight_result = message_data['weight_result']
            openid = message_data['openid']
            task_id = message_data['task_id']

            if not image_path or not inference_result or not weight_result or not openid or not task_id:
                logger.info("Not complicate data: {data}")
                continue

            await process_message(image_path, presigned_url, inference_result, weight_result, openid, task_id)
    except Exception as e:
        logger.error(f"Error in consume_messages: {e}")
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_messages())