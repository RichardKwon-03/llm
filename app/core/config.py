from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "local"

    POSTGRES_DSN: str

    REDIS_URL: str
    PROMPT_CACHE_TTL_SECONDS: int = 300

    MONGO_URL: str

    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()