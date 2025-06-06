from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from security import get_current_user, check_manager_role
from . import crud, schemas
from models import User, UserRole

router = APIRouter(prefix="/orders", tags=["Заказы"])


@router.get(
    "/",
    response_model=List[schemas.Order],
    description="Получить заказы пользователя или все заказы (для менеджера или администратора)",
)
def read_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role in [UserRole.MANAGER, UserRole.ADMIN]:
        return crud.get_orders(db, skip=skip, limit=limit)
    return crud.get_orders(db, user_id=current_user.id, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Order, description="Создать заказ")
def create_order(
    order: schemas.OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.create_order(db, order=order, user_id=current_user.id)


@router.get(
    "/{order_id}",
    response_model=schemas.Order,
    description="Получить информацию о заказе",
)
def read_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    if (
        current_user.role not in [UserRole.MANAGER, UserRole.ADMIN]
        and db_order.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return db_order


@router.patch(
    "/{order_id}/status",
    response_model=schemas.Order,
    dependencies=[Depends(check_manager_role)],
    description="Обновить статус заказа (только для администратора и менеджера)",
)
def update_order_status(
    order_id: int,
    status_update: schemas.OrderUpdate,
    db: Session = Depends(get_db),
):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return crud.update_order_status(db, order_id=order_id, status=status_update.status)


@router.delete(
    "/{order_id}",
    dependencies=[Depends(check_manager_role)],
    description="Удалить заказ (только для администратора и менеджера)",
)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    crud.delete_order(db, order_id=order_id)
    return HTMLResponse(
        status_code=status.HTTP_200_OK, detail="Order deleted successfully"
    )
