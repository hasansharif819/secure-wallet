from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, func
from app.database.db import Base
from sqlalchemy.orm import relationship


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    users = relationship("User", back_populates="transactions")