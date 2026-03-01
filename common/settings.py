from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    env: str = Field(default="dev", alias="AGENTIC_ENV")
    database_url: str = Field(
        default="sqlite+pysqlite:///./data/agentic.db", alias="AGENTIC_DATABASE_URL"
    )
    redis_url: str = Field(default="redis://localhost:6379/0", alias="AGENTIC_REDIS_URL")
    secret_key: str = Field(default="development-secret", alias="AGENTIC_SECRET_KEY")
    artifact_root: Path = Field(default=Path("./data/artifacts"), alias="AGENTIC_ARTIFACT_ROOT")
    storage_mode: str = Field(default="filesystem", alias="AGENTIC_STORAGE_MODE")
    composite_score_enabled: bool = Field(
        default=False, alias="AGENTIC_COMPOSITE_SCORE_ENABLED"
    )
    default_repeats: int = Field(default=10, alias="AGENTIC_DEFAULT_REPEATS")
    max_repeats: int = Field(default=10, alias="AGENTIC_MAX_REPEATS")
    default_timeout_sec: int = Field(default=1800, alias="AGENTIC_DEFAULT_TIMEOUT_SEC")
    standard_cpus: int = Field(default=2, alias="AGENTIC_STANDARD_CPUS")
    standard_memory_mb: int = Field(default=4096, alias="AGENTIC_STANDARD_MEMORY_MB")
    standard_pids_limit: int = Field(default=512, alias="AGENTIC_STANDARD_PIDS_LIMIT")
    standard_concurrency: int = Field(default=3, alias="AGENTIC_STANDARD_CONCURRENCY")
    docker_image: str = Field(default="python:3.11-slim", alias="AGENTIC_DOCKER_IMAGE")
    docker_network: str = Field(default="bridge", alias="AGENTIC_DOCKER_NETWORK")
    otel_exporter_endpoint: str = Field(
        default="http://localhost:4318", alias="AGENTIC_OTEL_EXPORTER_ENDPOINT"
    )

    def ensure_dirs(self) -> None:
        self.artifact_root.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_dirs()
    return settings
