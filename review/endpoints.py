from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from security import get_current_user, check_manager_role, get_optional_current_user
from . import crud, schemas
from models import User, UserRole, ReviewStatus

router = APIRouter(prefix="/reviews", tags=["Отзывы"])


@router.get(
    "/", response_model=List[schemas.Review], description="Получить список отзывов"
)
async def read_reviews(
    product_id: Optional[int] = Query(None, gt=0, description="ID Товара"),
    user_id: Optional[int] = Query(None, gt=0, description="ID Пользователя"),
    skip: int = Query(0, description="Сколько отзывов пропустить"),
    limit: int = Query(100, gt=0, description="Сколько отзывов получить"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    if current_user and current_user.role in [
        UserRole.ADMIN,
        UserRole.MANAGER,
    ]:
        status = None
    else:
        status = ReviewStatus.APPROVED
    return crud.get_reviews(
        db,
        product_id=product_id,
        user_id=user_id,
        status=status,
        skip=skip,
        limit=limit,
    )


@router.post(
    "/products/{product_id}",
    response_model=schemas.Review,
    description="Добавить отзыв",
)
def create_review(
    product_id: int,
    review: schemas.ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.create_review(
        db, review=review, product_id=product_id, user_id=current_user.id
    )


@router.get("/{review_id}", response_model=schemas.Review)
def read_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )
    return db_review


@router.put(
    "/{review_id}",
    response_model=schemas.Review,
    description="Обновить информацию об отзыве",
)
def update_review(
    review_id: int,
    review: schemas.ReviewUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_review = crud.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )
    if (
        current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]
        and db_review.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return crud.update_review(db, review_id=review_id, review_update=review)


@router.patch(
    "/{review_id}/status",
    response_model=schemas.Review,
    dependencies=[Depends(check_manager_role)],
    description="Изменить статус отзыва (только для администратора и менджера)",
)
def update_review_status(
    review_id: int,
    status_update: ReviewStatus = Query(..., description="Новый статус отзыва"),
    db: Session = Depends(get_db),
):
    return crud.update_review_status(db, review_id=review_id, status=status_update)


@router.delete("/{review_id}", description="Удалить отзыв")
def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_review = crud.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )
    if (
        current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]
        and db_review.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    crud.delete_review(db, review_id=review_id)
    return HTMLResponse(
        status_code=status.HTTP_200_OK, detail="Review deleted successfully"
    )
