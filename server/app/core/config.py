from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "crawler_system"
    api_prefix: str = "/v1"
    database_url: str = "sqlite:///./data.db"
    max_retry: int = 3
    timeout: int = 30
    snapshot_dir: str = "storage/snapshots"
    export_dir: str = "storage/exports"
    default_admin_username: str = "运营管理员"
    default_admin_password: str = "admin123"
    session_ttl_days: int = 7

    model_config = SettingsConfigDict(
        env_prefix="CRAWLER_",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
