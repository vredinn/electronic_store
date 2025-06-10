from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from security import check_admin_role
from . import crud, schemas

router = APIRouter(prefix="/categories", tags=["Категории"])


@router.get(
    "/", response_model=List[schemas.Category], description="Получить список категорий"
)
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categories(db, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=schemas.Category,
    dependencies=[Depends(check_admin_role)],
    description="Добавить категорию (только для администраторов)",
)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category=category)


@router.get(
    "/{category_id}",
    response_model=schemas.CategoryWithProducts,
    description="Получить информацию о категории",
)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return db_category


@router.put(
    "/{category_id}",
    response_model=schemas.Category,
    dependencies=[Depends(check_admin_role)],
    description="Обновить информацию о категории (только для администраторов)",
)
def update_category(
    category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db)
):
    db_category = crud.update_category(
        db, category_id=category_id, category_update=category
    )
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return db_category


@router.delete(
    "/{category_id}",
    dependencies=[Depends(check_admin_role)],
    description="Удалить категорию (только для администраторов)",
)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.delete_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return HTMLResponse(
        status_code=status.HTTP_200_OK, detail="Category deleted successfully"
    )
