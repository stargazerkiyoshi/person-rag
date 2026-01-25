from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_username: str
    app_password: str
    jwt_secret: str
    jwt_algorithm: str
    jwt_expire_minutes: int
    log_level: str
    llm_provider: str
    llm_api_key: str
    llm_model: str
    llm_base_url: str
    llm_timeout_seconds: int
    session_db_path: str
    session_max_rounds: int


def _load_config_file(path: str) -> dict:
    if not path:
        return {}
    config_path = Path(path)
    if not config_path.exists():
        return {}
    with config_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _get_int(value: str | None, fallback: int) -> int:
    if value is None:
        return fallback
    try:
        return int(value)
    except ValueError:
        return fallback


def load_settings() -> Settings:
    config_path = os.getenv("CONFIG_FILE", "config/config.json")
    config = _load_config_file(config_path)

    return Settings(
        app_username=os.getenv("APP_USERNAME", config.get("app_username", "admin")),
        app_password=os.getenv("APP_PASSWORD", config.get("app_password", "admin")),
        jwt_secret=os.getenv("JWT_SECRET", config.get("jwt_secret", "change-me")),
        jwt_algorithm=os.getenv("JWT_ALGORITHM", config.get("jwt_algorithm", "HS256")),
        jwt_expire_minutes=_get_int(
            os.getenv("JWT_EXPIRE_MINUTES"),
            int(config.get("jwt_expire_minutes", 60)),
        ),
        log_level=os.getenv("LOG_LEVEL", config.get("log_level", "INFO")),
        llm_provider=os.getenv("LLM_PROVIDER", config.get("llm_provider", "openai")),
        llm_api_key=os.getenv("LLM_API_KEY", config.get("llm_api_key", "")),
        llm_model=os.getenv("LLM_MODEL", config.get("llm_model", "gpt-4o-mini")),
        llm_base_url=os.getenv("LLM_BASE_URL", config.get("llm_base_url", "")),
        llm_timeout_seconds=_get_int(
            os.getenv("LLM_TIMEOUT_SECONDS"),
            int(config.get("llm_timeout_seconds", 60)),
        ),
        session_db_path=os.getenv("SESSION_DB_PATH", config.get("session_db_path", "data/sessions.db")),
        session_max_rounds=_get_int(
            os.getenv("SESSION_MAX_ROUNDS"),
            int(config.get("session_max_rounds", 6)),
        ),
    )
