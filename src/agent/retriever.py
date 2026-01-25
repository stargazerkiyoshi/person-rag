from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable, Protocol


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


class LocalKeywordRetriever:
    def __init__(self, data_dir: Path | str, extensions: Iterable[str] | None = None) -> None:
        self._data_dir = Path(data_dir)
        self._extensions = tuple(extensions or (".txt", ".md"))

    def retrieve(self, query: str, top_k: int) -> list[Chunk]:
        keywords = self._tokenize(query)
        if not keywords:
            return []

        chunks = list(self._load_chunks())
        scored: list[tuple[int, Chunk]] = []
        for chunk in chunks:
            haystack = chunk.text.lower()
            score = sum(haystack.count(keyword) for keyword in keywords)
            if score > 0:
                scored.append((score, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored[:top_k]]

    def _load_chunks(self) -> Iterable[Chunk]:
        if not self._data_dir.exists():
            return []
        chunks: list[Chunk] = []
        for path in self._data_dir.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in self._extensions:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            except UnicodeDecodeError:
                text = path.read_text(encoding="utf-8", errors="ignore")

            for block in self._split_blocks(text):
                chunks.append(Chunk(text=block, source=str(path)))
        return chunks

    def _split_blocks(self, text: str) -> list[str]:
        blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
        return blocks

    def _tokenize(self, query: str) -> list[str]:
        query = query.strip()
        if not query:
            return []

        tokens: list[str] = []
        for match in re.findall(r"[a-zA-Z0-9]+|[\u4e00-\u9fff]+", query):
            if re.fullmatch(r"[a-zA-Z0-9]+", match):
                tokens.append(match.lower())
                continue
            if len(match) == 1:
                tokens.append(match)
                continue
            tokens.extend(match[idx : idx + 2] for idx in range(len(match) - 1))

        deduped = []
        seen = set()
        for token in tokens:
            if token not in seen:
                deduped.append(token)
                seen.add(token)
        return deduped
