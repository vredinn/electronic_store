from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from database import get_db
from security import (
    get_current_user,
    check_admin_role,
)
from . import crud, schemas
from models import User

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get(
    "/me",
    response_model=schemas.User,
    description="Получить информацию о текущем пользователе",
)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get(
    "/",
    response_model=list[schemas.User],
    dependencies=[Depends(check_admin_role)],
    description="Получить список пользователей (только для администратора)",
)
def read_users(
    skip: int = Query(0, description="Смещение результатов"),
    limit: int = Query(100, description="Максимальное количество результатов"),
    db: Session = Depends(get_db),
):
    return crud.get_users(db, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=schemas.User,
    dependencies=[Depends(check_admin_role)],
    description="Создать нового пользователя (только для администратора)",
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    return crud.create_user(db, user=user)


@router.get(
    "/{user_id}",
    response_model=schemas.User,
    dependencies=[Depends(check_admin_role)],
    description="Получить информацию о пользователе по ID (только для администратора)",
)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.put(
    "/{user_id}",
    response_model=schemas.User,
    dependencies=[Depends(check_admin_role)],
    description="Обновить информацию о пользователе по ID (только для администратора)",
)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.delete(
    "/{user_id}",
    dependencies=[Depends(check_admin_role)],
    description="Удалить пользователя по ID (только для администратора)",
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return HTMLResponse(status_code=status.HTTP_200_OK, detail="User deleted")
