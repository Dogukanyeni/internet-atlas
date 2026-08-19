"""Application settings.

Every setting comes from an environment variable. Nothing is hard-coded, so the same
image runs locally, in preview and in production (ADR-013).

If a required variable is missing, the app refuses to start. A loud failure at boot is
much better than a confusing error hours later.
"""

from enum import StrEnum
from functools import lru_cache

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    LOCAL = "local"
    PREVIEW = "preview"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )

    # --- App ---
    env: Environment = Field(default=Environment.LOCAL, alias="ATLAS_ENV")
    debug: bool = Field(default=False, alias="ATLAS_DEBUG")
    secret_key: SecretStr = Field(alias="ATLAS_SECRET_KEY")
    api_url: str = Field(default="http://localhost:8000", alias="ATLAS_API_URL")
    web_url: str = Field(default="http://localhost:3000", alias="ATLAS_WEB_URL")

    # --- Data ---
    database_url: SecretStr = Field(alias="DATABASE_URL")
    redis_url: SecretStr = Field(alias="REDIS_URL")

    # --- Storage ---
    s3_endpoint_url: str = Field(default="", alias="S3_ENDPOINT_URL")
    s3_access_key: SecretStr = Field(default=SecretStr(""), alias="S3_ACCESS_KEY")
    s3_secret_key: SecretStr = Field(default=SecretStr(""), alias="S3_SECRET_KEY")
    s3_bucket: str = Field(default="atlas-local", alias="S3_BUCKET")
    s3_region: str = Field(default="auto", alias="S3_REGION")

    # --- Feature switches ---
    # Off everywhere except production, so a laptop can never start a real crawl
    # and an AI bill can never appear by accident (Phase 4 environment matrix).
    crawler_enabled: bool = Field(default=False, alias="ATLAS_CRAWLER_ENABLED")
    ai_enabled: bool = Field(default=False, alias="ATLAS_AI_ENABLED")

    # --- Email (Phase 8) ---
    email_backend: str = Field(default="console", alias="EMAIL_BACKEND")
    email_from: str = Field(default="noreply@localhost", alias="EMAIL_FROM")

    @field_validator("secret_key")
    @classmethod
    def secret_must_be_real(cls, value: SecretStr) -> SecretStr:
        raw = value.get_secret_value()
        if len(raw) < 32:
            msg = "ATLAS_SECRET_KEY must be at least 32 characters"
            raise ValueError(msg)
        return value

    @property
    def is_production(self) -> bool:
        return self.env is Environment.PRODUCTION

    @property
    def cors_origins(self) -> list[str]:
        return [self.web_url]


@lru_cache
def get_settings() -> Settings:
    """Read settings once per process."""
    return Settings()
