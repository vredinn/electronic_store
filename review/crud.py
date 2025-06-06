from sqlalchemy.orm import Session
from typing import List, Optional
from . import schemas
import models


def get_review(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id).first()


def get_reviews(
    db: Session,
    product_id: Optional[int] = None,
    user_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(models.Review)
    if product_id:
        query = query.filter(models.Review.product_id == product_id)
    if user_id:
        query = query.filter(models.Review.user_id == user_id)
    if status:
        query = query.filter(models.Review.status == status)
    return query.offset(skip).limit(limit).all()


def create_review(
    db: Session, review: schemas.ReviewCreate, product_id: int, user_id: int
):
    db_review = models.Review(
        **review.model_dump(), product_id=product_id, user_id=user_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def update_review(db: Session, review_id: int, review_update: schemas.ReviewUpdate):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review:
        update_data = review_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_review, key, value)
        db.commit()
        db.refresh(db_review)
    return db_review


def delete_review(db: Session, review_id: int):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
    return db_review
