from fastapi import FastAPI, Depends, APIRouter
from security import get_current_user
import auth, category, product, review, user, order

app = FastAPI(title="API Магазина электроники", version="1.0.0")

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router)
api_router.include_router(category.router)
api_router.include_router(product.router)
api_router.include_router(review.router)
api_router.include_router(user.router)
api_router.include_router(order.router)

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Добро пожаловать в API Магазина электроники!"}


@app.get("/secure", dependencies=[Depends(get_current_user)])
async def secure_endpoint():
    return {"message": "Вы вошли на защищенный эндпоинт"}
