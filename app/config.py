from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    REDIS_URL: str  # ✅ nueva variable

    class Config:
        env_file = ".env"

settings = Settings()
