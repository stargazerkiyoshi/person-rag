from pathlib import Path

from src.agent.retriever import LocalKeywordRetriever


def test_local_keyword_retriever(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "note.txt").write_text("Apple banana.\n\nOrange fruit.", encoding="utf-8")
    (data_dir / "readme.md").write_text("This is a banana note.", encoding="utf-8")

    retriever = LocalKeywordRetriever(data_dir)
    results = retriever.retrieve("banana", top_k=5)
    assert results
    assert any("banana" in chunk.text.lower() for chunk in results)


def test_local_keyword_retriever_no_match(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "note.txt").write_text("Apple banana.", encoding="utf-8")

    retriever = LocalKeywordRetriever(data_dir)
    results = retriever.retrieve("kiwi", top_k=5)
    assert results == []


def test_local_keyword_retriever_chinese(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "note.txt").write_text("技能要点：提升攻击与速度。", encoding="utf-8")

    retriever = LocalKeywordRetriever(data_dir)
    results = retriever.retrieve("整理技能要点", top_k=5)
    assert results
