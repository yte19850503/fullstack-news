from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://news:news123@localhost:3306/news_db"
    redis_url: str = "redis://localhost:6379"
    jwt_secret: str = "fallback-secret"
    jwt_expires_in: str = "7d"
    port: int = 8000

    model_config = {"env_file": ".env"}


settings = Settings()
