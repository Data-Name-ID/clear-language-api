from enum import StrEnum
from functools import cached_property
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL

from app.core.promt import SYSTEM_PROMPT

BASE_DIR = Path(__file__).parent.parent  # app


class LLMProvider(StrEnum):
    YANDEX = "yandex"
    OPENAI = "openai"


class StaticConfig:
    USERNAME_MIN_LENGTH = 3
    PASSWORD_MIN_LENGTH = 8

    SHORT_STR_LENGTH = 20  # Коды, статусы, идентификаторы
    NAME_STR_LENGTH = 100  # Имена, логины, названия, заголовки, теги
    DESCRIPTION_STR_LENGTH = 500  # Краткие описания, аннотации, комментарии
    LONG_STR_LENGTH = 1000  # Длинные тексты, описания, аннотации
    URL_STR_LENGTH = 2048  # Ссылки, адреса, пути
    CREDENTIALS_STR_LENGTH = 255  # Email-адреса, пароли


class AppConfig(BaseModel):
    origins: list = ["http://localhost", "http://localhost:8000"]


class DatabaseConfig(BaseModel):
    user: str | None = "postgres"
    password: str | None = "postgres"  # noqa: S105
    host: str = "localhost"
    port: int = 5432
    name: str = "postgres"

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    @cached_property
    def url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        )


class SentryConfig(BaseModel):
    dsn: str | None = None
    environment: str | None = None


class YandexConfig(BaseModel):
    folder_id: str = ""
    oauth_token: str = ""
    model_name: str = "yandexgpt"


class OpenAIConfig(BaseModel):
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    model_name: str = "gpt-4o-mini"


class ModelConfig(BaseModel):
    provider: LLMProvider = LLMProvider.YANDEX
    temperature: float = 0.6
    instruction: str = SYSTEM_PROMPT
    timeout: int = 360


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR.parent / ".env", BASE_DIR.parent / ".env.dev"),
        case_sensitive=False,
        env_prefix="BACKEND__",
        env_nested_delimiter="__",
        extra="ignore",
    )

    app: AppConfig
    db: DatabaseConfig
    sentry: SentryConfig
    yc: YandexConfig = YandexConfig()
    openai: OpenAIConfig = OpenAIConfig()
    mc: ModelConfig
    static_dir: Path = BASE_DIR / "static"
