from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.agent.providers import ProviderConfigError
from src.agent.runner import AgentRunner
from src.api.deps import get_agent_runner

router = APIRouter()


class AgentRequest(BaseModel):
    task: str
    session_id: str | None = None


class TraceEntryModel(BaseModel):
    step: str
    status: str
    detail: str
    at: str


class ActionResultModel(BaseModel):
    name: str
    status: str
    detail: str


class AgentResponse(BaseModel):
    result: str
    sources: list[str]
    trace: list[TraceEntryModel]
    actions: list[ActionResultModel]
    session_id: str


@router.post("/agent", response_model=AgentResponse)
def run_agent(payload: AgentRequest, runner: AgentRunner = Depends(get_agent_runner)) -> AgentResponse:
    try:
        result = runner.run(payload.task, payload.session_id)
    except ProviderConfigError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="模型响应解析失败",
        ) from exc
    return AgentResponse(
        result=result.result,
        sources=result.sources,
        trace=[TraceEntryModel(**asdict(entry)) for entry in result.trace],
        actions=[ActionResultModel(**asdict(item)) for item in result.actions],
        session_id=result.session_id,
    )
