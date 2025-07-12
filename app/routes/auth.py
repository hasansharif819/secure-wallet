from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserOut, Token, UserLogin
from app.database.db import get_db
from app.crud import user as crud_user
from app.core.security import create_access_token
from typing import List

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserOut)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud_user.create_user(db, data.name, data.email, data.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login", response_model=Token)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        user = await crud_user.authenticate_user(db, data.email, data.password)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users")
async def get_users(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    try:
        return await crud_user.get_users_paginated(db, page, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
