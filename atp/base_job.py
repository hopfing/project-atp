import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


class BaseJob:

    def __init__(self, tournament: dict):
        self.tournament = tournament
        self.tourney_id = tournament["Id"]
        self.tourney_display = (
            tournament["Location"].split(",")[0].replace(" ", "_").lower()
        )
        self.year = tournament["FormattedDate"][-4:]
        self.tour = tournament["Type"].lower()

    def _path(
        self,
        bucket: str,
        filename: str = None,
        mode: str = "read",  # "read" or "write"
    ) -> Path:
        if bucket not in {"raw", "staged", "analysis"}:
            raise ValueError(f"Invalid bucket: {bucket}")

        base = (
            DATA_DIR
            / str(self.year)
            / self.tour
            / "tournaments"
            / f"{self.tourney_id}_{self.tourney_display}"
            / bucket
        )

        if mode == "write":
            base.mkdir(parents=True, exist_ok=True)
        elif mode == "read":
            if not base.exists():
                raise FileNotFoundError(f"Directory does not exist: {base}")
        else:
            raise ValueError(f"Invalid mode: {mode}")

        return base if filename is None else base / filename

    def save_json(self, data, path: Path):
        path = path.with_suffix(".json")

        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
