from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url : str
    mistral_api_key: str
    gnews_api_key: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    telegram_token: str
    api_url: str = "http://localhost:8000"
    ai_username: str = "ai_assistant"

    model_config= SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
