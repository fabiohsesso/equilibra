from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from pydantic import condecimal

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    balance: float = 0.0

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    mes: int
    valor: float
    descricao: str
    categoria: Optional[str] = None
    data: Optional[str] = None

class Goal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str
    target_amount: float
    current_amount: float = 0.0
    target_date: Optional[str] = None  # ISO date string
