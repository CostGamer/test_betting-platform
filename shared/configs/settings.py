from os import environ as env
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, model_validator

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN = "access"
REFRESH_TOKEN = "refresh"


class PostgresSettings(BaseModel):
    host: str = Field(default="localhost", alias="POSTGRES_HOST")
    port: int = Field(default=5432, alias="POSTGRES_PORT")
    user: str = Field(default="user", alias="POSTGRES_USER")
    password: str = Field(default="my_password", alias="POSTGRES_PASSWORD")
    db_name: str = Field(default="my_database", alias="POSTGRES_DB")
    pool_size: int = Field(default=10, alias="DB_POOL_SIZE")
    max_overflow: int = Field(default=10, alias="DB_MAX_OVERFLOW")

    @property
    def db_uri(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class LoggingSettings(BaseModel):
    log_level: str = Field(default="DEBUG", alias="LOG_LEVEL")
    log_file: str = Field(default="app.log", alias="LOG_FILE")
    log_encoding: str = Field(
        default="utf-8",
        alias="LOG_ENCODING",
    )


class RabbitSettings(BaseModel):
    rabbit_host: str = Field(default="localhost", alias="RABBITMQ_HOST")
    rabbit_port: int = Field(default=5672, alias="RABBITMQ_PORT")
    rabbit_password: str = Field(default="guest", alias="RABBITMQ_PASSWORD")
    rabbit_user: str = Field(default="guest", alias="RABBITMQ_USER")
    rabbit_rk: str = Field(default="line_queue", alias="RABBITMQ_RK")
    rabbit_exchange: str = Field(default="betting_lines", alias="RABBITMQ_EXCHANGE")

    @property
    def mq_uri(self) -> str:
        return f"amqp://{self.rabbit_user}:{self.rabbit_password}@{self.rabbit_host}:{self.rabbit_port}/"


class RedisSettings(BaseModel):
    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_db: int = Field(default=0, alias="REDIS_DB")
    redis_max_conn: int = Field(default=1000, alias="REDIS_MAX_CONN")


class JWTSettings(BaseModel):
    jwt_secret: str = Field(default="secret", alias="SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_token_expire_minutes: int = Field(default=20)
    jwt_refresh_token_expire_days: int = Field(default=90)


class OtherSettings(BaseModel):
    line_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:8000", "http://127.0.0.1:8000"],
        alias="ALLOWED_LINE_ORIGINS",
    )
    bet_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:8001", "http://127.0.0.1:8001"],
        alias="ALLOWED_BET_ORIGINS",
    )

    @model_validator(mode="before")
    def split_origins(cls, values: dict[str, Any]) -> dict[str, Any]:
        for key in ["ALLOWED_LINE_ORIGINS", "ALLOWED_BET_ORIGINS"]:
            if key in values and isinstance(values[key], str):
                values[key] = [url.strip() for url in values[key].split(",")]
        return values


class Settings(BaseModel):
    database: PostgresSettings = Field(default_factory=lambda: PostgresSettings(**env))
    logging: LoggingSettings = Field(default_factory=lambda: LoggingSettings(**env))
    different: OtherSettings = Field(default_factory=lambda: OtherSettings(**env))
    rabbit: RabbitSettings = Field(default_factory=lambda: RabbitSettings(**env))
    redis: RedisSettings = Field(default_factory=lambda: RedisSettings(**env))
    jwt: JWTSettings = Field(default_factory=lambda: JWTSettings(**env))


def load_dotenv(path: str | Path) -> None:
    path = Path(path)
    if not path.exists():
        return
    with path.open(mode="r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("#") or line.strip() == "":
                continue
            try:
                key, value = line.strip().split("=", maxsplit=1)
                env.setdefault(key, value)
            except ValueError:
                print(f"Invalid line in .env file: {line.strip()}")


load_dotenv(".env")
