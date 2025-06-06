from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from models import UserRole


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["username"])
    email: EmailStr = Field(..., examples=["user@example.com"])


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, examples=["Password123"])


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None, min_length=3, max_length=50, examples=["username"]
    )
    email: Optional[EmailStr] = Field(None, examples=["user@example.com"])
    password: Optional[str] = Field(None, min_length=6, examples=["Password123"])


class User(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
