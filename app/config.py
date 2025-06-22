from pydantic_core import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # Database configuration
POSTGRES_DB: str
POSTGRES_PASSWORD: str
POSTGRES_USER: str
POSTGRES_HOST: str = 'db'
POSTGRES_PORT: int = 5432
POSTGRES_URL: str = "postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Json Web Token (JWT) configuration
JWT_SECRET_KEY: str
JWT_ALGORITHM: str = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

# NLP configuration
SPACE_MODE: str = 'en_core_web_sm'


def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.POSTGRES_URL = self.POSTGRES_URL.format(
        POSTGRES_URL=self.POSTGRES_URL
    )


settings = Settings()
