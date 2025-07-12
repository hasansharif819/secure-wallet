from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from fastapi.security import APIKeyHeader
from app.database.db import get_db
from app.crud.user import get_user_by_id
from app.crud.transaction import top_up_wallet, get_transactions, withdraw_wallet
from app.schemas.transaction import TopUpRequest, TransactionOut
from typing import List, Dict, Any

SECRET_KEY = "xFoGdlV-JYu7iHvS0eJp2ZJW2X3AfXDL"
ALGORITHM = "HS256"

router = APIRouter(prefix="/wallet")
oauth2_scheme = APIKeyHeader(name="Authorization")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid token format")
    try:
        token = token.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        user = await get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except (JWTError, ValueError, TypeError) as e:
        raise HTTPException(status_code=403, detail="Invalid token")


@router.get("/balance")
async def get_balance(current_user=Depends(get_current_user)):
    try:
        return {"balance": current_user.balance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/top-up", response_model=TransactionOut)
async def top_up(data: TopUpRequest, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        return await top_up_wallet(db, current_user, data.amount)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/withdraw", response_model=TransactionOut)
async def withdraw(data: TopUpRequest, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        return await withdraw_wallet(db, current_user, data.amount)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/transactions")
async def transactions(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    try:
        result = await get_transactions(db, current_user.id, page, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
