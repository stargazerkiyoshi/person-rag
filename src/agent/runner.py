from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone

from langchain_core.prompts import ChatPromptTemplate

from src.agent.actions import ActionExecutor, ActionResult
from src.agent.providers import LlmProvider
from src.agent.retriever import Chunk, EmptyRetriever, KnowledgeRetriever
from src.core.config import Settings


@dataclass(frozen=True)
class TraceEntry:
    step: str
    status: str
    detail: str
    at: str


@dataclass(frozen=True)
class AgentResult:
    result: str
    sources: list[str]
    trace: list[TraceEntry]
    actions: list[ActionResult]


class AgentRunner:
    def __init__(
        self,
        provider: LlmProvider,
        retriever: KnowledgeRetriever | None = None,
        actions: ActionExecutor | None = None,
        top_k: int = 5,
    ) -> None:
        self._provider = provider
        self._retriever = retriever or EmptyRetriever()
        self._actions = actions or ActionExecutor()
        self._top_k = top_k

    def run(self, task: str) -> AgentResult:
        trace: list[TraceEntry] = []
        chunks = self._retriever.retrieve(task, self._top_k)
        trace.append(self._trace("retrieve", "success", f"命中 {len(chunks)} 条片段"))

        if not chunks:
            return AgentResult(
                result="未找到相关资料，无法完成任务。",
                sources=[],
                trace=trace,
                actions=[],
            )

        llm = self._provider.get_llm()
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你是一个智能体，请基于给定资料完成任务。"
                    "只输出 JSON，包含 fields: summary, analysis_steps, actions, result, sources_used。",
                ),
                (
                    "human",
                    "任务:\n{task}\n\n资料:\n{context}\n\n"
                    "actions 为数组，可为空。sources_used 为来源列表。",
                ),
            ]
        )
        context = self._render_context(chunks)
        response = llm.invoke(prompt.format_messages(task=task, context=context))
        trace.append(self._trace("analyze", "success", "模型已返回结果"))

        payload = self._parse_payload(response.content)
        actions = self._actions.execute(payload.get("actions", []))
        if actions:
            trace.append(self._trace("actions", "success", f"执行动作 {len(actions)} 项"))

        sources = self._normalize_sources(payload.get("sources_used", []), chunks)
        result_text = str(payload.get("result") or "").strip() or "模型未返回有效结果。"
        return AgentResult(result=result_text, sources=sources, trace=trace, actions=actions)

    def _render_context(self, chunks: list[Chunk]) -> str:
        lines: list[str] = []
        for idx, chunk in enumerate(chunks, start=1):
            lines.append(f"[{idx}] {chunk.text}\n来源: {chunk.source}")
        return "\n\n".join(lines)

    def _parse_payload(self, content: str) -> dict:
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError("模型返回非 JSON 内容") from exc

    def _normalize_sources(self, sources: list[str], chunks: list[Chunk]) -> list[str]:
        if sources:
            return [str(source) for source in sources]
        return [chunk.source for chunk in chunks]

    def _trace(self, step: str, status: str, detail: str) -> TraceEntry:
        return TraceEntry(
            step=step,
            status=status,
            detail=detail,
            at=datetime.now(tz=timezone.utc).isoformat(),
        )


def build_agent_runner(settings: Settings) -> AgentRunner:
    from src.agent.providers import build_provider

    provider = build_provider(settings)
    return AgentRunner(provider=provider)
