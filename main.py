from fastapi import FastAPI, Depends
from security import get_current_user
import auth

app = FastAPI(title="API Магазина электроники", version="0.0.1")
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Добро пожаловать в API Магазина электроники!"}


@app.get("/secure", dependencies=[Depends(get_current_user)])
async def secure_endpoint():
    return {"message": "Это защищенный эндпоинт"}
