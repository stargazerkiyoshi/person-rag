from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone

from langchain_core.prompts import ChatPromptTemplate

from src.agent.actions import ActionExecutor, ActionResult
from src.agent.providers import LlmProvider
from src.agent.retriever import (
    Chunk,
    ChromaVectorRetriever,
    KnowledgeRetriever,
    LocalKeywordRetriever,
)
from src.agent.sessions import SessionStore, format_history
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
    session_id: str


@dataclass(frozen=True)
class RetrievalDecision:
    need_retrieval: bool
    reason: str


class AgentRunner:
    def __init__(
        self,
        provider: LlmProvider,
        retriever: KnowledgeRetriever | None = None,
        actions: ActionExecutor | None = None,
        sessions: SessionStore | None = None,
        top_k: int = 5,
    ) -> None:
        self._provider = provider
        self._retriever = retriever or LocalKeywordRetriever("data")
        self._actions = actions or ActionExecutor()
        self._sessions = sessions
        self._top_k = top_k

    def run(self, task: str, session_id: str | None = None) -> AgentResult:
        trace: list[TraceEntry] = []
        llm = self._provider.get_llm()
        session_id = self._ensure_session(session_id)
        history = self._load_history(session_id)

        decision = self._decide_retrieval(llm, task, history)
        trace.append(self._trace("decide_retrieval", "success", decision.reason or "已完成检索判定"))

        if not decision.need_retrieval:
            answer = self._answer_without_retrieval(llm, task, history)
            trace.append(self._trace("answer", "success", "已返回纯对话结果"))
            self._store_turn(session_id, task, answer)
            return AgentResult(result=answer, sources=[], trace=trace, actions=[], session_id=session_id)

        chunks = self._retriever.retrieve(task, self._top_k)
        trace.append(self._trace("retrieve", "success", f"命中 {len(chunks)} 条片段"))

        if not chunks:
            return AgentResult(
                result="未找到相关资料，无法完成任务。",
                sources=[],
                trace=trace,
                actions=[],
                session_id=session_id,
            )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你是一个智能体，请基于给定资料完成任务。"
                    "只输出 JSON，不要包含任何解释或代码块。"
                    "JSON fields: summary, analysis_steps, actions, result, sources_used。",
                ),
                (
                    "human",
                    """历史对话:
{history}

任务:
{task}

资料:
{context}

actions 为数组，可为空。sources_used 为来源列表。""",
                ),
            ]
        )
        context = self._render_context(chunks)
        response = llm.invoke(prompt.format_messages(task=task, context=context, history=history))
        trace.append(self._trace("analyze", "success", "模型已返回结果"))

        payload = self._parse_payload(response.content)
        actions = self._actions.execute(payload.get("actions", []))
        if actions:
            trace.append(self._trace("actions", "success", f"执行动作 {len(actions)} 项"))

        sources = self._normalize_sources(payload.get("sources_used", []), chunks)
        result_text = str(payload.get("result") or "").strip() or "模型未返回有效结果。"
        self._store_turn(session_id, task, result_text)
        return AgentResult(result=result_text, sources=sources, trace=trace, actions=actions, session_id=session_id)

    def _decide_retrieval(self, llm, task: str, history: str) -> RetrievalDecision:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你负责判断是否需要检索资料才能回答。"
                    "只输出 JSON，不要包含任何解释或代码块。"
                    "JSON fields: need_retrieval (true/false), reason。",
                ),
                ("human", "历史对话:\n{history}\n\n问题:\n{task}"),
            ]
        )
        response = llm.invoke(prompt.format_messages(task=task, history=history))
        payload = self._parse_payload(response.content)
        return RetrievalDecision(
            need_retrieval=bool(payload.get("need_retrieval")),
            reason=str(payload.get("reason") or ""),
        )

    def _answer_without_retrieval(self, llm, task: str, history: str) -> str:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你是一个对话助手，请直接回答用户问题。"
                    "不要编造来源或引用资料。",
                ),
                ("human", "历史对话:\n{history}\n\n问题:\n{task}"),
            ]
        )
        response = llm.invoke(prompt.format_messages(task=task, history=history))
        return str(response.content or "").strip() or "模型未返回有效结果。"

    def _render_context(self, chunks: list[Chunk]) -> str:
        lines: list[str] = []
        for idx, chunk in enumerate(chunks, start=1):
            lines.append(f"[{idx}] {chunk.text}\n来源: {chunk.source}")
        return "\n\n".join(lines)

    def _parse_payload(self, content: str) -> dict:
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            trimmed = self._extract_json(content)
            if trimmed:
                try:
                    return json.loads(trimmed)
                except json.JSONDecodeError as nested_exc:
                    raise ValueError("模型返回非 JSON 内容") from nested_exc
            raise ValueError("模型返回非 JSON 内容") from exc

    def _normalize_sources(self, sources: list[str], chunks: list[Chunk]) -> list[str]:
        if sources:
            return [str(source) for source in sources]
        return [chunk.source for chunk in chunks]

    def _extract_json(self, content: str) -> str | None:
        start = content.find("{")
        end = content.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None
        return content[start : end + 1]

    def _trace(self, step: str, status: str, detail: str) -> TraceEntry:
        return TraceEntry(
            step=step,
            status=status,
            detail=detail,
            at=datetime.now(tz=timezone.utc).isoformat(),
        )

    def _ensure_session(self, session_id: str | None) -> str:
        if not self._sessions:
            return session_id or "stateless"
        return self._sessions.get_or_create(session_id)

    def _load_history(self, session_id: str) -> str:
        if not self._sessions or session_id == "stateless":
            return ""
        messages = self._sessions.recent_messages(session_id)
        return format_history(messages)

    def _store_turn(self, session_id: str, user_text: str, assistant_text: str) -> None:
        if not self._sessions or session_id == "stateless":
            return
        self._sessions.add_message(session_id, "user", user_text)
        self._sessions.add_message(session_id, "assistant", assistant_text)


def build_agent_runner(settings: Settings) -> AgentRunner:
    from src.agent.providers import build_provider

    provider = build_provider(settings)
    sessions = SessionStore(settings.session_db_path, settings.session_max_rounds)
    retriever_type = settings.retriever_type.lower()
    if retriever_type == "chroma":
        retriever: KnowledgeRetriever = ChromaVectorRetriever(
            chroma_path=settings.chroma_path,
            collection_name=settings.chroma_collection,
            embedding_model=settings.embedding_model,
        )
    else:
        retriever = LocalKeywordRetriever(settings.data_dir)
    return AgentRunner(provider=provider, retriever=retriever, sessions=sessions)
