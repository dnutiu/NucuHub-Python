import os


class ApplicationConfig:
    # If true the backend will run in debug mode.
    BACKEND_DEBUG = bool(os.getenv("BACKEND_DEBUG", False))
    # Affects the logging level across all modules.
    LOGGING_LEVEL = os.getenv("LOG_LEVEL")
    # Override the REDIS_URL, useful for testing & debugging.
    REDIS_URL = os.getenv("REDIS_URL") or "redis_service"
    # Firebase related config.
    FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
    FIREBASE_AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN")
    FIREBASE_DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL")
    FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET")
    FIREBASE_USER_EMAIL = os.getenv("FIREBASE_USER_EMAIL")
    FIREBASE_USER_PASSWORD = os.getenv("FIREBASE_USER_PASSWORD")
