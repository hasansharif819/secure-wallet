from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserOut, Token, UserLogin
from app.database.db import get_db
from app.crud import user as crud_user
from app.core.security import create_access_token

router = APIRouter(prefix="/auth")

@router.post("/register", response_model=UserOut)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud_user.create_user(db, data.name, data.email, data.password)

@router.post("/login", response_model=Token)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await crud_user.authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}