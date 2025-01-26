from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GITHUB_API_TOKEN: str
    TELEGRAM_API_TOKEN: str

    TIME_TASKS_WAIT: float = Field(default=5)
    TASK_RELEASE_INTERVAL_CHECK: float = Field(default=5 * 60)
    NOTIFY_INTERVAL_CHECK: float = Field(default=10)
    LIMIT_MESSAGES: int = Field(default=2)
    INTERVAL_LIMIT_MESSAGES: int = Field(default=1)
    ADMIN_ID: int = Field(default=1031986686)
    DEBUG: bool = Field(default=True)
    DATABASE_NAME: str = Field(default="database.db")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
