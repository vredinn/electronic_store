from sqlalchemy.orm import Session
from typing import Optional
from . import schemas
import models


def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(
    db: Session,
    page: int = 1,
    limit: int = 10,
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "asc",
) -> dict:
    query = db.query(models.Product)

    if name:
        query = query.filter(models.Product.name.ilike(f"%{name}%"))

    if category:
        query = query.join(models.Category).filter(models.Category.name == category)
    if min_price:
        query = query.filter(models.Product.price >= min_price)
    if max_price:
        query = query.filter(models.Product.price <= max_price)
    if in_stock:
        query = query.filter(models.Product.stock > 0)
    if sort_by:
        order_column = None
        if sort_by == "name":
            order_column = models.Product.name
        elif sort_by == "price":
            order_column = models.Product.price
        elif sort_by == "rating":
            order_column = models.Product.rating

        if order_column:
            if sort_order.lower() == "desc":
                query = query.order_by(order_column.desc())
            else:
                query = query.order_by(order_column.asc())
    total = query.count()
    if page < 1:
        page = 1
    offset = (page - 1) * limit

    items = query.offset(offset).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
    }


def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(
    db: Session, product_id: int, product_update: schemas.ProductUpdate
) -> Optional[models.Product]:
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )
    if db_product:
        update_data = product_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> Optional[models.Product]:
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
