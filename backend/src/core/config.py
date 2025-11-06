from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME = "SPARK API"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Sports Performance Analysis and Ranking Kit"
    DEBUG = True

    POSTGRES_HOST = "localhost"
    POSTGRES_PORT = 5432
    POSTGRES_DB = "spark_db"
    POSTGRES_PASSWORD = "spark_password_2024"

    API_V1_PREFIX = "api/v1"

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    class Config:
        env_file = "../.env"
        case_sensitive = True

@lru_cache
def get_settings():
    return Settings()