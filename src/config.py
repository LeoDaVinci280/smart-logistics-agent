"""
Application configuration.

This module loads environment variables from the .env file
using Pydantic Settings.

The resulting settings object can be imported anywhere
within the project.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global application settings.
    Values are loaded automatically from the .env file.
    """

    OPENAI_API_KEY: str

    DATABASE_URL: str = "sqlite:///./data/logistics.db"

    OPENAI_MODEL: str = "gpt-4o-mini"

    DEFAULT_CURRENCY: str = "AUD"

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()