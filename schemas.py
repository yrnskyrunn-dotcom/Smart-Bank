from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8, max_length=128)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AccountCreate(BaseModel):
    name: str = "Main"
    type: Literal["checking", "savings"] = "checking"

class AccountOut(BaseModel):
    id: int
    name: str
    type: str
    balance: float
    created_at: datetime
    class Config:
        from_attributes = True

class TransferIn(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float = Field(gt=0)
    description: str = ""

class TransactionOut(BaseModel):
    id: int
    from_account_id: Optional[int]
    to_account_id: Optional[int]
    amount: float
    description: str
    created_at: datetime
    class Config:
        from_attributes = True
