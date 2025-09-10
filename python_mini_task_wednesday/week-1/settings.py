from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_POST: str
    FASTAPI_ENV: str
    DEBUG: bool = True
    ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
