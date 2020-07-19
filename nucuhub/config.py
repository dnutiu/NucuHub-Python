import os


class ApplicationConfig:
    BACKEND_DEBUG = bool(os.getenv("BACKEND_DEBUG", False))
    LOGGING_LEVEL = os.getenv("LOG_LEVEL")
    REDIS_URL = os.getenv("REDIS_URL") or "redis_service"
    FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
    FIREBASE_AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN")
    FIREBASE_DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL")
    FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET")
    FIREBASE_USER_EMAIL = os.getenv("FIREBASE_USER_EMAIL")
    FIREBASE_USER_PASSWORD = os.getenv("FIREBASE_USER_PASSWORD")
