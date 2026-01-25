from datetime import datetime, timezone

from fastapi.testclient import TestClient

from src.agent.actions import ActionResult
from src.agent.providers import ProviderConfigError
from src.agent.runner import AgentResult, TraceEntry
from src.api.deps import get_agent_runner
from src.main import create_app


class FakeRunner:
    def run(self, task: str) -> AgentResult:
        trace = [
            TraceEntry(
                step="retrieve",
                status="success",
                detail=f"收到任务: {task}",
                at=datetime.now(tz=timezone.utc).isoformat(),
            )
        ]
        actions = [ActionResult(name="save_note", status="success", detail="data/agent_notes.txt")]
        return AgentResult(result="ok", sources=["source-a"], trace=trace, actions=actions)


class FailingRunner:
    def run(self, task: str) -> AgentResult:
        raise ProviderConfigError("未配置 LLM_API_KEY")


def test_agent_success() -> None:
    app = create_app()
    app.dependency_overrides[get_agent_runner] = lambda: FakeRunner()
    client = TestClient(app)
    response = client.post("/agent", json={"task": "test"})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == "ok"
    assert data["sources"] == ["source-a"]
    assert data["trace"][0]["step"] == "retrieve"
    assert data["actions"][0]["name"] == "save_note"


def test_agent_missing_api_key() -> None:
    app = create_app()
    app.dependency_overrides[get_agent_runner] = lambda: FailingRunner()
    client = TestClient(app)
    response = client.post("/agent", json={"task": "test"})
    assert response.status_code == 400
    assert response.json()["detail"] == "未配置 LLM_API_KEY"
