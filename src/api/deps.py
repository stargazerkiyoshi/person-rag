from fastapi import Request

from src.agent.runner import AgentRunner
from src.core.config import Settings


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_agent_runner(request: Request) -> AgentRunner:
    return request.app.state.agent_runner
