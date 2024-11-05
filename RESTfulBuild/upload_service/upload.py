from fastapi import FastAPI, UploadFile, File, Depends, status
from utils import logger, check_and_create_bucket, producer, KAFKA_BROKER, minio_client, BUCKET_NAME, generate_presigned_url
from aiokafka import AIOKafkaProducer
import asyncio
import io
from minio.error import S3Error  # 替换 MinioException
from fastapi import HTTPException
from utils import get_current_user
import uuid
from utils import KAFKA_TOPIC, async_session
import json
from models import User, UserInfoUpdateRequest
from sqlalchemy import select, update

app = FastAPI()

@app.on_event("startup")    
async def startup():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)
    await producer.start()
    await check_and_create_bucket()

@app.on_event("shutdown")
async def shutdown_event():
    if producer:
        await producer.stop()

@app.post("/image")
async def upload(
    file: UploadFile = File(...), 
    current_user_openid: str = Depends(get_current_user)  # 添加 JWT 认证
    ):
    try:
        image_data = await file.read()
        image_name = file.filename
        logger.info(f"User {current_user_openid} sent image: {image_name}")

        # 上传图片到 MinIO
        await asyncio.to_thread(
            minio_client.put_object,
            BUCKET_NAME,
            image_name,
            io.BytesIO(image_data),
            len(image_data),
        )
        logger.info(f"Uploaded image: {image_name}")
    except S3Error as e:  # 使用 S3Error 替代 MinioException
        logger.error(f"Failed to upload image: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload image")
    
    task_id = str(uuid.uuid4())

    try:
        image_path = f"http://minio:9000/{BUCKET_NAME}/{image_name}"

        presigned_url = generate_presigned_url(BUCKET_NAME, image_name)

        message = {
            "task_id": task_id,
            "image_path": image_path,
            "openid": current_user_openid,
            "presigned_url": presigned_url
        }

        await producer.send_and_wait(KAFKA_TOPIC, key=task_id.encode("utf-8"), value=json.dumps(message).encode("utf-8"))
        logger.info(f"Sent message to image_topic: {message}")
    except Exception as e:
        logger.error(f"Failed to send message to Kafka: {e}")
        raise HTTPException(status_code=500, detail="Failed to send message to Kafka")
    
    return {"task_id": task_id}


@app.post("/head")
async def set_head(
    file: UploadFile = File(...), 
    current_user_openid: str = Depends(get_current_user)  # 添加 JWT 认证
    ):
    try:
        image_data = await file.read()
        image_name = file.filename
        logger.info(f"User {current_user_openid} sent image: {image_name}")

        # 上传图片到 MinIO
        await asyncio.to_thread(
            minio_client.put_object,
            BUCKET_NAME,
            image_name,
            io.BytesIO(image_data),
            len(image_data),
        )
        logger.info(f"Uploaded image: {image_name}")
    except S3Error as e:  # 使用 S3Error 替代 MinioException
        logger.error(f"Failed to upload image: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload image")
    
    # 生成头像的 presigned URL
    new_head_url = generate_presigned_url(BUCKET_NAME, image_name)

    try:
        async with async_session() as session:
            async with session.begin():  # 确保事务管理
                # 更新用户头像 URL
                await session.execute(
                    update(User)
                    .where(User.openid == current_user_openid)
                    .values(head_url=new_head_url)
                )
                await session.commit()  # 提交事务

                logger.info(f"Update head_url success for user: {current_user_openid}")
                return {
                    "message": "Head updated successfully",
                    "head_url": new_head_url  # 返回生成的头像 URL
                }

    except Exception as e:
        logger.error(f"Update head_url failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update head"
        )

@app.put("/userinfo")
async def set_userinfo(
    request: UserInfoUpdateRequest, 
    current_user_openid: str = Depends(get_current_user)
):
    new_name = request.name
    new_phone_number = request.phone_number
    new_email = request.email
    new_signature = request.signature

    async with async_session() as session:
        async with session.begin():  # 确保事务管理
            # 获取当前用户信息
            current_user_info = await session.execute(
                select(User).where(User.openid == current_user_openid)
            )
            current_user = current_user_info.scalars().first()

            if not current_user:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # 检查名字,手机号，电邮是否已存在
            if new_name != current_user.name:
                name_exist = await session.execute(
                    select(User).where(User.name == new_name)
                )
                if name_exist.scalars().first():
                    logger.error(f"Name: {new_name} exists.")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, 
                        detail="Name already in use"
                    )
            
            if new_phone_number != current_user.phone_number:
                phone_number_exist = await session.execute(
                    select(User).where(User.phone_number == new_phone_number)
                )
                if phone_number_exist.scalars().first():
                    logger.error(f"Phone_number: {new_phone_number} exists.")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, 
                        detail="Phone number already in use"
                    )

            if new_email != current_user.email:
                email_exist = await session.execute(
                    select(User).where(User.email == new_email)
                )
                if email_exist.scalars().first():
                    logger.error(f"Email: {new_email} exists.")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, 
                        detail="Email already in use"
                    )
            
            try:
                # 更新用户信息
                await session.execute(
                    update(User)
                    .where(User.openid == current_user_openid)
                    .values(name=new_name, 
                            phone_number=new_phone_number,
                            email=new_email,
                            signature=new_signature
                            )
                )
                await session.commit()  # 提交事务
                logger.info(f"Update name success for user: {current_user_openid}")
            except Exception as e:
                logger.error(f"Update name failed: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update name, phone_number, email "
                )
    return {"message": "name, phonenumber, email, signature updated successfully"}
    

@app.put("/gold_coin")
async def set_gold_coin(
    request: UserInfoUpdateRequest,
    current_user_openid: str = Depends(get_current_user)
):
    new_gold_coin = request.gold_coin
    # gold_coin
    try:
        async with async_session() as session:
            async with session.begin():  # Ensure transaction management
                # Check the current gold_coin value
                result = await session.execute(
                    select(User).where(User.openid == current_user_openid)
                )
                user = result.scalar_one_or_none()
                
                if user is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found"
                    )
                
                # Only update if the new value is different
                if user.gold_coin != new_gold_coin:
                    await session.execute(
                        update(User)
                        .where(User.openid == current_user_openid)
                        .values(gold_coin=new_gold_coin)
                    )
                    await session.commit()  # Commit transaction
                    logger.info(f"Update gold_coin success for user: {current_user_openid}")
                else:
                    return {"message": "No change in gold_coin value"}             
    except Exception as e:
        logger.error(f"Update gold_coin failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update gold_coin"
        )
    
    return {"new_gold_coin": new_gold_coin}

@app.put("/experience")
async def set_experience(
    request: UserInfoUpdateRequest,
    current_user_openid: str = Depends(get_current_user)
):
    new_experience = request.experience
    # experience
    try:
        async with async_session() as session:
            async with session.begin():  # Ensure transaction management
                # Check the current experience value
                result = await session.execute(
                    select(User).where(User.openid == current_user_openid)
                )
                user = result.scalar_one_or_none()
                
                if user is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found"
                    )
                
                # Only update if the new value is different
                if user.experience != new_experience:
                    await session.execute(
                        update(User)
                        .where(User.openid == current_user_openid)
                        .values(experience=new_experience)
                    )
                    await session.commit()  # Commit transaction
                    logger.info(f"Update experience success for user: {current_user_openid}")
                else:
                    return {"message": "No change in experience value"}              
    except Exception as e:
        logger.error(f"Update experience failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update experience"
        )

    return {"new_experience": new_experience}
