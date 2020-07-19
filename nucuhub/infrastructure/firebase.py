import pyrebase

from nucuhub.config import ApplicationConfig
from nucuhub.logging import get_logger

logger = get_logger("FirebaseService")


class FirebaseConfiguration:
    api_key = None
    auth_domain = None
    database_url = None
    storage_bucket = None

    def __init__(
        self, api_key=None, auth_domain=None, database_url=None, storage_bucket=None
    ):
        self.api_key = api_key or ApplicationConfig.FIREBASE_API_KEY
        self.auth_domain = auth_domain or ApplicationConfig.FIREBASE_AUTH_DOMAIN
        self.database_url = database_url or ApplicationConfig.FIREBASE_DATABASE_URL
        self.storage_bucket = (
            storage_bucket or ApplicationConfig.FIREBASE_STORAGE_BUCKET
        )

    def __str__(self):
        return f"FirebaseConfig: {self.auth_domain};{self.database_url};{self.storage_bucket}"


class FirebaseService:
    __singleton = None
    __client = None

    def __init__(self):
        """
            Don't call this method directly instead use instance.
        """
        pass

    @classmethod
    def _configure(cls, config: FirebaseConfiguration):
        if (
            any(
                (
                    config.api_key,
                    config.auth_domain,
                    config.database_url,
                    config.storage_bucket,
                )
            )
            is None
        ):
            raise ValueError(
                "FirebaseService has invalid config! Please set all environment variables."
            )

        config = {
            "apiKey": config.api_key,
            "authDomain": config.auth_domain,
            "databaseURL": config.database_url,
            "storageBucket": config.storage_bucket,
        }

        cls.__client = pyrebase.initialize_app(config)

    @classmethod
    def instance(cls):
        if cls.__singleton is None:
            config = FirebaseConfiguration()
            cls._configure(config)
            logger.info(f"FirebaseService: Config={config}")
            cls.__singleton = cls()
        return cls.__singleton

    @classmethod
    def set_singleton(cls, singleton):
        cls.__singleton = singleton
