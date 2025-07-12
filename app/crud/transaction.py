from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import Transaction
from app.models.user import User


async def top_up_wallet(db: AsyncSession, user: User, amount: float):
    try:
        user.balance += amount
        transaction = Transaction(user_id=user.id, amount=amount)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction
    except Exception as e:
        await db.rollback()
        raise e


async def withdraw_wallet(db: AsyncSession, user: User, amount: float):
    try:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than 0")

        if user.balance < amount:
            raise ValueError("Insufficient balance")

        user.balance -= amount
        transaction = Transaction(user_id=user.id, amount=-amount)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction
    except Exception as e:
        await db.rollback()
        raise e


async def get_transactions(db: AsyncSession, user_id: int, page: int = 1, limit: int = 20):
    try:
        offset = (page - 1) * limit

        total_query = await db.execute(
            select(func.count()).select_from(Transaction).where(Transaction.user_id == user_id)
        )
        total = total_query.scalar()

        query = await db.execute(
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        transactions = query.scalars().all()

        return {
            "data": transactions,
            "meta": {
                "total": total,
                "total_pages": (total + limit - 1) // limit,
                "page": page,
                "limit": limit
            }
        }
    except Exception as e:
        raise e
