from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Any

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: List[int]

    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def parse_admin_ids(cls, v: Any):
        if isinstance(v, str):
            if not v.strip():
                return []
            # Split by comma and convert to int
            return [int(x.strip()) for x in v.split(",") if x.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

config = Settings()

