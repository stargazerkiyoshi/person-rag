from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Chunk:
    text: str
    source: str


class KnowledgeRetriever(Protocol):
    def retrieve(self, query: str, top_k: int) -> list[Chunk]:
        raise NotImplementedError


class EmptyRetriever:
    def retrieve(self, query: str, top_k: int) -> list[Chunk]:
        return []
