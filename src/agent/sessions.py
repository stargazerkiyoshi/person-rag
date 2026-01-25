from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class SessionMessage:
    role: str
    content: str


class SessionStore:
    def __init__(self, db_path: str, max_rounds: int) -> None:
        self._db_path = Path(db_path)
        self._max_rounds = max_rounds
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def get_or_create(self, session_id: str | None) -> str:
        if session_id:
            if self._session_exists(session_id):
                return session_id
        new_id = self._generate_session_id()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO sessions (id) VALUES (?)",
                (new_id,),
            )
        return new_id

    def add_message(self, session_id: str, role: str, content: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
                (session_id, role, content),
            )

    def recent_messages(self, session_id: str) -> list[SessionMessage]:
        limit = max(0, self._max_rounds * 2)
        if limit == 0:
            return []
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id DESC LIMIT ?",
                (session_id, limit),
            ).fetchall()
        rows.reverse()
        return [SessionMessage(role=row[0], content=row[1]) for row in rows]

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS sessions ("
                "id TEXT PRIMARY KEY,"
                "created_at TEXT DEFAULT (datetime('now'))"
                ")"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS messages ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "session_id TEXT NOT NULL,"
                "role TEXT NOT NULL,"
                "content TEXT NOT NULL,"
                "created_at TEXT DEFAULT (datetime('now')),"
                "FOREIGN KEY(session_id) REFERENCES sessions(id)"
                ")"
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path.as_posix())

    def _session_exists(self, session_id: str) -> bool:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM sessions WHERE id = ?",
                (session_id,),
            ).fetchone()
        return row is not None

    def _generate_session_id(self) -> str:
        import uuid

        return uuid.uuid4().hex


def format_history(messages: Iterable[SessionMessage]) -> str:
    lines: list[str] = []
    for msg in messages:
        role = "用户" if msg.role == "user" else "助手"
        lines.append(f"{role}: {msg.content}")
    return "\n".join(lines)
