import os


class ApplicationConfig:
    BACKEND_DEBUG = bool(os.getenv("BACKEND_DEBUG", False))
    LOGGING_LEVEL = os.getenv("LOG_LEVEL")
    REDIS_URL = os.getenv("REDIS_URL") or "redis_service"
