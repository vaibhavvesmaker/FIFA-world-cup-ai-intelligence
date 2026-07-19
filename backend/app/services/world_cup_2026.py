from typing import Any

import httpx

from app.config import get_settings


class WorldCup2026ProviderError(Exception):
    """Raised when the community World Cup 2026 API cannot be used."""


def _to_int(value: Any) -> int | None:
    if value in (None, "", "null"):
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _is_finished(game: dict[str, Any]) -> bool:
    finished = str(game.get("finished", "")).strip().lower()
    elapsed = str(game.get("time_elapsed", "")).strip().lower()

    return finished == "true" or elapsed == "finished"


def _normalize_game(game: dict[str, Any]) -> dict[str, Any]:
    return {
        "match_id": str(game.get("id") or game.get("_id")),
        "kickoff": game.get("local_date"),
        "status": "finished" if _is_finished(game) else "scheduled",
        "stage": game.get("type"),
        "group": game.get("group"),
        "matchday": game.get("matchday"),
        "stadium_id": game.get("stadium_id"),
        "home_team": {
            "id": game.get("home_team_id"),
            "name": game.get("home_team_name_en"),
        },
        "away_team": {
            "id": game.get("away_team_id"),
            "name": game.get("away_team_name_en"),
        },
        "score": {
            "home": _to_int(game.get("home_score")),
            "away": _to_int(game.get("away_score")),
        },
        "source": {
            "provider": "community_worldcup2026",
            "verified": False,
            "url": "https://worldcup26.ir",
        },
    }


async def get_world_cup_2026_matches() -> list[dict[str, Any]]:
    settings = get_settings()
    url = f"{settings.world_cup_2026_api_base_url.rstrip('/')}/get/games"

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(url)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise WorldCup2026ProviderError(
            "World Cup 2026 community provider is unavailable"
        ) from exc

    payload = response.json()
    games = payload.get("games")

    if not isinstance(games, list):
        raise WorldCup2026ProviderError(
            "World Cup 2026 provider returned an unexpected response"
        )

    return [_normalize_game(game) for game in games]