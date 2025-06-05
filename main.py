from fastapi import FastAPI

app = FastAPI(title="API Магазина электроники", version="0.0.1")


@app.get("/")
def root():
    return {"message": "Добро пожаловать в API Магазина электроники!"}
