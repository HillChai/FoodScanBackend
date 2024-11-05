from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from utils import logger, get_openid
from fastapi import HTTPException
from utils import check_user_from_db, create_jwt_token, get_db
from models import PERMISSION, LoginRequest, Base
from utils import engine

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)   

@app.post("/auth")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    code = request.code
    logger.info(f"Received code: {code}")

    openid = await get_openid(code)

    if not openid:
        logger.error("Failed to get openid")
        raise HTTPException(status_code=400, detail="Failed to get openid")
    
    user = await check_user_from_db(openid, db)
    logger.info(f"Current user permission: {user.permission}, created_at: {user.created_at}, updated_at: {user.updated_at}")

    if user.permission == PERMISSION.NO_PERMISSION:
        raise HTTPException(status_code=403, detail="No permission")
    
    token = create_jwt_token(openid, user.permission)
    created_at = user.created_at.strftime("%Y-%m-%d %H:%M:%S")  
    updated_at = user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"openid: {openid}, permission: {user.permission}, token: {token}, created_at: {created_at}, updated_at: {updated_at}")

    return {"openid": openid, "head_url":user.head_url, "name":user.name, "gold_coin":user.gold_coin, "experience":user.experience,
             "permission": user.permission, "token": token, "created_at": created_at, "updated_at": updated_at, 
             "email":user.email, "phone_number":user.phone_number, "signature":user.signature}
