from fastapi import FastAPI
from app.api.router import router as api_router
from app.core.error_handlers import install_exception_handlers

def create_app() -> FastAPI:
    app = FastAPI(title="llm-api")
    install_exception_handlers(app)
    app.include_router(api_router)
    return app

app = create_app()