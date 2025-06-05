from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_name: str
    secret_key: str
    salt: str

    class Config:
        env_file = ".env"


settings = Settings()
