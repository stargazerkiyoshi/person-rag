from dataclasses import dataclass
from typing import Any

from src.agent.runner import AgentRunner
from src.agent.retriever import Chunk, KnowledgeRetriever


@dataclass
class FakeResponse:
    content: str


class FakeLLM:
    def __init__(self, responses: list[str]) -> None:
        self._responses = responses
        self.calls: list[Any] = []

    def invoke(self, messages: Any) -> FakeResponse:
        self.calls.append(messages)
        return FakeResponse(self._responses.pop(0))


class FakeProvider:
    def __init__(self, responses: list[str]) -> None:
        self._llm = FakeLLM(responses)

    def get_llm(self) -> FakeLLM:
        return self._llm


class SpyRetriever(KnowledgeRetriever):
    def __init__(self, chunks: list[Chunk]) -> None:
        self._chunks = chunks
        self.calls = 0

    def retrieve(self, query: str, top_k: int) -> list[Chunk]:
        self.calls += 1
        return self._chunks


def test_agent_skip_retrieval() -> None:
    provider = FakeProvider(['{"need_retrieval": false, "reason": "不需要"}', "直接回复"])
    retriever = SpyRetriever([Chunk(text="data", source="data.txt")])
    runner = AgentRunner(provider=provider, retriever=retriever)

    result = runner.run("你好", session_id="s1")

    assert result.result == "直接回复"
    assert result.sources == []
    assert retriever.calls == 0
    assert result.trace[0].step == "decide_retrieval"


def test_agent_trigger_retrieval() -> None:
    provider = FakeProvider(
        [
            '{"need_retrieval": true, "reason": "需要资料"}',
            '{"summary":"s","analysis_steps":[],"actions":[],"result":"ok","sources_used":["data.txt"]}',
        ]
    )
    retriever = SpyRetriever([Chunk(text="data", source="data.txt")])
    runner = AgentRunner(provider=provider, retriever=retriever)

    result = runner.run("需要资料的问题", session_id="s1")

    assert result.result == "ok"
    assert result.sources == ["data.txt"]
    assert retriever.calls == 1
