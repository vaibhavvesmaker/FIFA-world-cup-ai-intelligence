from fastapi.testclient import TestClient

from app.main import app, get_football_client
from app.services.football import FootballProviderError


class SuccessfulFootballClient:
    async def get_next_world_cup_fixture(self) -> dict:
        return {
            "fixture_id": 2026,
            "competition": "World Cup",
            "home": {"name": "Home"},
            "away": {"name": "Away"},
            "source": {"provider": "API-Football"},
        }


class EmptyFootballClient:
    async def get_next_world_cup_fixture(self) -> None:
        return None


class FailingFootballClient:
    async def get_next_world_cup_fixture(self) -> None:
        raise FootballProviderError("provider failed")


def test_next_match_returns_normalized_fixture() -> None:
    app.dependency_overrides[get_football_client] = SuccessfulFootballClient
    client = TestClient(app)

    response = client.get("/matches/next")

    assert response.status_code == 200
    assert response.json()["source"]["provider"] == "API-Football"
    app.dependency_overrides.clear()


def test_next_match_returns_404_when_tournament_has_no_future_fixture() -> None:
    app.dependency_overrides[get_football_client] = EmptyFootballClient
    client = TestClient(app)

    response = client.get("/matches/next")

    assert response.status_code == 404
    app.dependency_overrides.clear()


def test_next_match_returns_502_when_provider_fails() -> None:
    app.dependency_overrides[get_football_client] = FailingFootballClient
    client = TestClient(app)

    response = client.get("/matches/next")

    assert response.status_code == 502
    app.dependency_overrides.clear()
