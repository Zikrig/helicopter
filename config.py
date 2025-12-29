from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: List[int]
    WEBHOOK_URL: str
    WEB_SERVER_HOST: str = "127.0.0.1"
    WEB_SERVER_PORT: int = 8080
    WEBHOOK_PATH: str = "/webhook"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Settings()

