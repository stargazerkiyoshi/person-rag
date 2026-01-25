from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ActionResult:
    name: str
    status: str
    detail: str


class ActionExecutor:
    def __init__(self, data_dir: Path | None = None) -> None:
        self._data_dir = data_dir or Path("data")

    def execute(self, actions: list[dict]) -> list[ActionResult]:
        results: list[ActionResult] = []
        for action in actions:
            name = str(action.get("name") or action.get("type") or "").strip()
            if not name:
                results.append(ActionResult(name="unknown", status="skipped", detail="缺少动作名称"))
                continue
            if name == "save_note":
                results.append(self._save_note(action))
                continue
            results.append(ActionResult(name=name, status="failed", detail="不支持的动作"))
        return results

    def _save_note(self, action: dict) -> ActionResult:
        content = str(action.get("content") or action.get("input") or "").strip()
        if not content:
            return ActionResult(name="save_note", status="failed", detail="缺少内容")
        target = action.get("path") or "agent_notes.txt"
        base_dir = self._data_dir.resolve()
        target_path = (self._data_dir / target).resolve()
        if not str(target_path).startswith(str(base_dir)):
            return ActionResult(name="save_note", status="failed", detail="非法路径")
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with target_path.open("a", encoding="utf-8") as handle:
            handle.write(f"{content}\n")
        return ActionResult(name="save_note", status="success", detail=str(target_path))
