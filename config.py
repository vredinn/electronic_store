from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    salt: str
    db_name: str
    token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
