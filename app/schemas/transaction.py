from pydantic import BaseModel
from datetime import datetime

class TopUpRequest(BaseModel):
    amount: float

class TransactionOut(BaseModel):
    id: int
    amount: float
    created_at: datetime

    class Config:
        orm_mode = True