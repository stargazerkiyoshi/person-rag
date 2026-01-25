import pytest

from src.agent.providers import OpenAIProvider, ProviderConfigError, build_provider
from src.core.config import Settings


def _settings(provider: str) -> Settings:
    return Settings(
        app_username="admin",
        app_password="admin",
        jwt_secret="secret",
        jwt_algorithm="HS256",
        jwt_expire_minutes=60,
        log_level="INFO",
        llm_provider=provider,
        llm_api_key="key",
        llm_model="gpt-4o-mini",
        llm_base_url="",
        llm_timeout_seconds=60,
    )


def test_build_provider_chatgpt_alias() -> None:
    provider = build_provider(_settings("chatgpt"))
    assert isinstance(provider, OpenAIProvider)


def test_build_provider_unknown() -> None:
    with pytest.raises(ProviderConfigError):
        build_provider(_settings("unknown"))
