from datetime import datetime, timezone
from math import exp, log1p
from typing import Any


MODEL_VERSION = "elo-baseline-v1"
INITIAL_RATING = 1500.0
K_FACTOR = 32.0


class PredictionError(Exception):
    """Raised when a prediction cannot be generated."""


def _parse_kickoff(value: str | None) -> datetime:
    if not value:
        return datetime.max

    try:
        return datetime.strptime(value, "%m/%d/%Y %H:%M")
    except ValueError:
        return datetime.max


def _expected_score(home_rating: float, away_rating: float) -> float:
    return 1 / (1 + 10 ** ((away_rating - home_rating) / 400))


def _actual_score(home_goals: int, away_goals: int) -> float:
    if home_goals > away_goals:
        return 1.0
    if home_goals < away_goals:
        return 0.0
    return 0.5


def _update_ratings(
    home_rating: float,
    away_rating: float,
    home_goals: int,
    away_goals: int,
) -> tuple[float, float]:
    expected_home = _expected_score(home_rating, away_rating)
    actual_home = _actual_score(home_goals, away_goals)

    goal_difference = abs(home_goals - away_goals)
    margin_multiplier = 1.0 if goal_difference == 0 else 1 + log1p(goal_difference)

    adjustment = K_FACTOR * margin_multiplier * (actual_home - expected_home)

    return home_rating + adjustment, away_rating - adjustment


def predict_match(
    matches: list[dict[str, Any]],
    match_id: str,
) -> dict[str, Any]:
    target = next(
        (match for match in matches if str(match.get("match_id")) == str(match_id)),
        None,
    )

    if target is None:
        raise PredictionError(f"Match {match_id} was not found")

    target_kickoff = _parse_kickoff(target.get("kickoff"))
    ratings: dict[str, float] = {}
    training_matches = 0

    ordered_matches = sorted(
        matches,
        key=lambda match: _parse_kickoff(match.get("kickoff")),
    )

    for match in ordered_matches:
        if str(match.get("match_id")) == str(match_id):
            continue

        if _parse_kickoff(match.get("kickoff")) >= target_kickoff:
            continue

        if match.get("status") != "finished":
            continue

        home_id = str(match["home_team"]["id"])
        away_id = str(match["away_team"]["id"])
        home_goals = match["score"]["home"]
        away_goals = match["score"]["away"]

        if home_goals is None or away_goals is None:
            continue

        home_rating = ratings.get(home_id, INITIAL_RATING)
        away_rating = ratings.get(away_id, INITIAL_RATING)

        new_home_rating, new_away_rating = _update_ratings(
            home_rating,
            away_rating,
            home_goals,
            away_goals,
        )

        ratings[home_id] = new_home_rating
        ratings[away_id] = new_away_rating
        training_matches += 1

    home_id = str(target["home_team"]["id"])
    away_id = str(target["away_team"]["id"])
    home_rating = ratings.get(home_id, INITIAL_RATING)
    away_rating = ratings.get(away_id, INITIAL_RATING)

    home_strength = _expected_score(home_rating, away_rating)
    rating_gap = abs(home_rating - away_rating)

    draw_probability = max(
        0.12,
        min(0.30, 0.28 * exp(-rating_gap / 400)),
    )

    decisive_probability = 1 - draw_probability
    home_win_probability = decisive_probability * home_strength
    away_win_probability = decisive_probability * (1 - home_strength)

    return {
        "match_id": str(target["match_id"]),
        "teams": {
            "home": target["home_team"],
            "away": target["away_team"],
        },
        "probabilities": {
            "home_win": round(home_win_probability, 4),
            "draw": round(draw_probability, 4),
            "away_win": round(away_win_probability, 4),
        },
        "ratings": {
            "home": round(home_rating, 2),
            "away": round(away_rating, 2),
        },
        "model": {
            "name": "Elo team-strength baseline",
            "version": MODEL_VERSION,
            "training_matches": training_matches,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "data": {
            "provider": "community_worldcup2026",
            "verified": False,
            "leakage_guard": "Only completed matches before kickoff were used",
        },
    }