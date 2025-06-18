from sqlalchemy.orm import Session
from . import schemas
import models
from product import crud as prod_crud


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders(db: Session, user_id: int = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Order)
    if user_id:
        query = query.filter(models.Order.user_id == user_id)
    return query.offset(skip).limit(limit).all()


def create_order(db: Session, order: schemas.OrderCreate, user_id: int):
    db_order = models.Order(
        user_id=user_id, status=models.OrderStatus.PENDING, amount=0
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    amount = 0
    for item in order.items:
        price_at_order = prod_crud.get_product(db, item.product_id).price
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_order=price_at_order,
        )
        amount += price_at_order * item.quantity
        db.add(db_item)

    db_order.amount = amount
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order_status(db: Session, order_id: int, status: str):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order
