from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings


settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Live and historical World Cup intelligence API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Confirm that the API process is available."""

    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_env,
    }
