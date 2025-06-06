from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from models import ReviewStatus


class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    text: str = Field(..., min_length=10, max_length=1000)


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    text: Optional[str] = Field(None, min_length=10, max_length=1000)


class Review(ReviewBase):
    id: int
    product_id: int
    product_name: str
    user_id: int
    user_name: str
    status: ReviewStatus
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
