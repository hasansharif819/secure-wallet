from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.schemas.user import UserOut


async def create_user(db: AsyncSession, name: str, email: str, password: str):
    try:
        hashed = hash_password(password)
        user = User(name=name, email=email, hashed_password=hashed)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except Exception as e:
        await db.rollback()
        raise e


async def authenticate_user(db: AsyncSession, email: str, password: str):
    try:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user and verify_password(password, user.hashed_password):
            return user
        return None
    except Exception as e:
        raise e


async def get_user_by_id(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    except Exception as e:
        raise e


async def get_users_paginated(db: AsyncSession, page: int, limit: int) -> dict:
    try:
        offset = (page - 1) * limit

        # Get total count of users
        total_result = await db.execute(select(func.count()).select_from(User))
        total = total_result.scalar()

        # Get paginated users
        users_result = await db.execute(
            select(User)
            .order_by(User.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        users = users_result.scalars().all()

        return {
            "data": [UserOut.from_orm(user) for user in users],
            "meta": {
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": (total + limit - 1) // limit
            }
        }
    except Exception as e:
        raise RuntimeError(f"Failed to fetch users: {str(e)}")
