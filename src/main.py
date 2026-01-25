from fastapi import FastAPI

from src.api.routes import agent as agent_routes
from src.api.routes import auth as auth_routes
from src.api.routes import health as health_routes
from src.api.routes import protected as protected_routes
from src.agent.runner import build_agent_runner
from src.core.config import load_settings
from src.core.logging import setup_logging


def create_app() -> FastAPI:
    settings = load_settings()
    setup_logging(settings.log_level)

    app = FastAPI()
    app.state.settings = settings
    app.state.agent_runner = build_agent_runner(settings)

    app.include_router(health_routes.router)
    app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
    app.include_router(protected_routes.router, prefix="/protected", tags=["protected"])
    app.include_router(agent_routes.router, tags=["agent"])

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=False)
