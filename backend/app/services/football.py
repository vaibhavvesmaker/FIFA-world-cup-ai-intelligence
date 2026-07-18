from datetime import datetime, timezone
from typing import Any

import httpx


class FootballProviderError(Exception):
    """Raised when API-Football cannot provide a usable response."""


class FootballClient:
    """Small API-Football client that returns our stable internal schema."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    async def get_next_world_cup_fixture(self) -> dict[str, Any] | None:
        url = f"{self.base_url}/fixtures"
        params = {
            "league": 1,
            "season": 2026,
            "next": 1,
            "timezone": "America/New_York",
        }
        headers = {"x-apisports-key": self.api_key}

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise FootballProviderError("Football provider request failed") from exc

        payload = response.json()
        if payload.get("errors"):
            raise FootballProviderError("Football provider returned an API error")

        fixtures = payload.get("response", [])
        if not fixtures:
            return None

        return normalize_fixture(fixtures[0])


def normalize_fixture(item: dict[str, Any]) -> dict[str, Any]:
    fixture = item["fixture"]
    league = item["league"]
    teams = item["teams"]
    goals = item.get("goals", {})
    venue = fixture.get("venue") or {}

    return {
        "fixture_id": fixture["id"],
        "competition": league["name"],
        "season": league["season"],
        "round": league.get("round"),
        "kickoff": fixture["date"],
        "timezone": fixture["timezone"],
        "status": {
            "long": fixture["status"]["long"],
            "short": fixture["status"]["short"],
            "elapsed": fixture["status"].get("elapsed"),
        },
        "venue": {
            "name": venue.get("name"),
            "city": venue.get("city"),
        },
        "home": {
            "id": teams["home"]["id"],
            "name": teams["home"]["name"],
            "logo": teams["home"].get("logo"),
            "goals": goals.get("home"),
        },
        "away": {
            "id": teams["away"]["id"],
            "name": teams["away"]["name"],
            "logo": teams["away"].get("logo"),
            "goals": goals.get("away"),
        },
        "source": {
            "provider": "API-Football",
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
        },
    }
