from __future__ import annotations

from dataclasses import dataclass

from langchain_openai import ChatOpenAI

from src.core.config import Settings


class ProviderConfigError(ValueError):
    pass


class LlmProvider:
    def get_llm(self) -> ChatOpenAI:
        raise NotImplementedError


@dataclass(frozen=True)
class OpenAIProvider(LlmProvider):
    api_key: str
    model: str
    base_url: str
    timeout_seconds: int

    def get_llm(self) -> ChatOpenAI:
        if not self.api_key:
            raise ProviderConfigError("未配置 LLM_API_KEY")
        kwargs: dict = {"api_key": self.api_key, "model": self.model, "timeout": self.timeout_seconds}
        if self.base_url:
            kwargs["base_url"] = self.base_url
        return ChatOpenAI(**kwargs)


def build_provider(settings: Settings) -> LlmProvider:
    provider = settings.llm_provider.strip().lower()
    if provider == "openai" or provider == "chatgpt":
        return OpenAIProvider(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
            base_url=settings.llm_base_url,
            timeout_seconds=settings.llm_timeout_seconds,
        )
    raise ProviderConfigError(f"不支持的提供方: {settings.llm_provider}")
