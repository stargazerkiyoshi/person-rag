from pathlib import Path

from src.agent.sessions import SessionStore


def test_session_store_rounds(tmp_path: Path) -> None:
    db_path = tmp_path / "sessions.db"
    store = SessionStore(str(db_path), max_rounds=2)
    session_id = store.get_or_create(None)

    for idx in range(5):
        store.add_message(session_id, "user", f"user-{idx}")
        store.add_message(session_id, "assistant", f"assistant-{idx}")

    messages = store.recent_messages(session_id)
    assert len(messages) == 4
    assert messages[0].content == "user-3"
    assert messages[-1].content == "assistant-4"
