from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    anthropic_api_key: str
    model_name: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096
    cors_origins: list[str] = ["http://localhost:3000"]
    environment: str = "development"


settings = Settings()
