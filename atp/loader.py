import json
from pathlib import Path
from typing import List


def load_calendar(year: int, tour: str) -> List[dict]:
    """

    :param year: season in YYYY format - ATP groups cross-year tournaments by END date
    :param tour: ATP or CH
    :return: return list of dicts representing each calendar month
    """
    path = Path(f"data/{year}/{tour.lower()}/calendar.json")
    with open(path, "r") as f:
        calendar = json.load(f)
        months = calendar.get("TournamentDates")
        return months


def _iter_tournaments(calendar: List[dict]):
    for month in calendar:
        for tournament in month.get("Tournaments", []):
            yield month, tournament


def get_tournament_by_id(year, tour, tournament_id) -> dict:

    calendar = load_calendar(year, tour)

    for month, tournament in _iter_tournaments(calendar):
        if tournament.get("Id") == tournament_id:
            return tournament
