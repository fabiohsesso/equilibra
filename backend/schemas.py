from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str

class TransactionCreate(BaseModel):
    user_id: int
    mes: int
    valor: float
    descricao: str
    data: Optional[str] = None

class GoalCreate(BaseModel):
    user_id: int
    title: str
    target_amount: float
    current_amount: Optional[float] = 0.0
    target_date: Optional[str] = None
