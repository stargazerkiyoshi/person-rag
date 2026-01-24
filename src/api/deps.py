from fastapi import Request

from src.core.config import Settings


def get_settings(request: Request) -> Settings:
    return request.app.state.settings
