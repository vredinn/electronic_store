from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Optional
from enum import Enum
from database import get_db, SessionLocal
from security import check_manager_role
from . import crud, schemas
from models import Category

router = APIRouter(prefix="/products", tags=["Товары"])


def get_category_enum():
    db = SessionLocal()
    try:
        categories = db.query(Category.name).all()
        category_dict = {cat[0].replace(" ", "_"): cat[0] for cat in categories}
        return Enum("CategoryEnum", category_dict)
    finally:
        db.close()


CategoryEnum = get_category_enum()


@router.get(
    "/", response_model=schemas.ProductPage, description="Получить список товаров"
)
async def read_products(
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(10, ge=1, le=100, description="Количество товаров на странице"),
    name: Optional[str] = Query(None, description="Фильтр по названию"),
    category: Optional[CategoryEnum] = Query(None, description="Фильтр по категории"),
    min_price: Optional[float] = Query(None, ge=1, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, ge=1, description="Максимальная цена"),
    in_stock: Optional[bool] = Query(None, description="Фильтр по наличию в наличии"),
    sort_by: Optional[schemas.SortBy] = Query(
        None, description="Параметр для сортировки"
    ),
    sort_order: Optional[schemas.SortOrder] = Query(
        schemas.SortOrder.ASC, description="Порядок сортировки"
    ),
    db: Session = Depends(get_db),
):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The minimum price cannot be higher than the maximum",
        )
    return crud.get_products(
        db,
        page=page,
        limit=limit,
        name=name,
        category=category.value if category else None,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        sort_by=sort_by.value if sort_by else None,
        sort_order=sort_order.value if sort_order else "asc",
    )


@router.post(
    "/",
    response_model=schemas.Product,
    dependencies=[Depends(check_manager_role)],
    description="Добавить товар (только для менеджера и администратора)",
)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product=product)


@router.get(
    "/{product_id}",
    response_model=schemas.Product,
    description="Получить информацию о товаре",
)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return db_product


@router.put(
    "/{product_id}",
    response_model=schemas.Product,
    dependencies=[Depends(check_manager_role)],
    description="Обновить информацию о товаре (только для менеджера и администратора)",
)
def update_product(
    product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)
):
    db_product = crud.update_product(db, product_id=product_id, product_update=product)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return db_product


@router.delete(
    "/{product_id}",
    dependencies=[Depends(check_manager_role)],
    description="Удалить товар (только для менеджера и администратора)",
)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return HTMLResponse(
        status_code=status.HTTP_200_OK, detail="Product deleted successfully"
    )
