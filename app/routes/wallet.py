from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from fastapi.security import APIKeyHeader
from app.database.db import get_db
from app.crud.user import get_user_by_id
from app.crud.transaction import top_up_wallet, get_transactions
from app.schemas.transaction import TopUpRequest, TransactionOut

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
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=403, detail="Invalid token")
    
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/balance")
async def get_balance(current_user=Depends(get_current_user)):
    return {"balance": current_user.balance}

@router.post("/top-up", response_model=TransactionOut)
async def top_up(data: TopUpRequest, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await top_up_wallet(db, current_user, data.amount)

@router.get("/transactions", response_model=list[TransactionOut])
async def transactions(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await get_transactions(db, current_user.id)