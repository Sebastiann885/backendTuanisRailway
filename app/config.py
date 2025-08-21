from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"

settings = Settings()