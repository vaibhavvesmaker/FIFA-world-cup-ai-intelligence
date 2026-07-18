from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.services.football import FootballClient, FootballProviderError


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


def get_football_client() -> FootballClient:
    if not settings.football_api_base_url or not settings.football_api_key:
        raise HTTPException(
            status_code=503,
            detail="Football data source is not configured",
        )
    return FootballClient(settings.football_api_base_url, settings.football_api_key)


@app.get("/matches/next", tags=["matches"])
async def next_world_cup_match(
    client: FootballClient = Depends(get_football_client),
) -> dict:
    """Return the next FIFA World Cup fixture in a stable internal format."""

    try:
        fixture = await client.get_next_world_cup_fixture()
    except FootballProviderError as exc:
        raise HTTPException(
            status_code=502,
            detail="Football data provider is temporarily unavailable",
        ) from exc

    if fixture is None:
        raise HTTPException(status_code=404, detail="No upcoming World Cup fixture found")
    return fixture
