import logging

from settings import settings


def get_openapi_url():
    OPENAPI_URL = None
    if settings.FASTAPI_ENV != "production":
        OPENAPI_URL = "/api/openapi.json"

    return OPENAPI_URL


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    console = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s %(name)s] %(message)s")
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger
