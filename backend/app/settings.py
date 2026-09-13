from pydantic_settings import BaseSettings
from sqlalchemy import URL
from functools import cached_property
from pydantic_settings.main import SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    
    DB_DRIVER: str = "postgresql+psycopg"
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    @cached_property
    def DATABASE_URL(self) -> URL:
        return URL.create(
            drivername=self.DB_DRIVER,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )


settings = DatabaseSettings()
