from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import Transaction
from app.models.user import User

async def top_up_wallet(db: AsyncSession, user: User, amount: float):
    user.balance += amount
    transaction = Transaction(user_id=user.id, amount=amount)
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction

async def withdraw_wallet(db: AsyncSession, user: User, amount: float):
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

async def get_transactions(db: AsyncSession, user_id: int):
    result = await db.execute(select(Transaction).where(Transaction.user_id == user_id))
    return result.scalars().all()