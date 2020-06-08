import os


class ApplicationConfig:
    LOGGING_LEVEL = os.getenv("LOG_LEVEL")
    REDIS_URL = os.getenv("REDIS_URL") or "redis_service"
