from sqlalchemy.orm import Session
import models
from . import schemas


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(
    db: Session, category_id: int, category_update: schemas.CategoryUpdate
):
    db_category = (
        db.query(models.Category).filter(models.Category.id == category_id).first()
    )
    if db_category:
        update_data = category_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = (
        db.query(models.Category).filter(models.Category.id == category_id).first()
    )
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category
