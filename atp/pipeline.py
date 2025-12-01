import argparse

from loader import get_tournament_by_id


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run ETL pipeline for ATP data.",
    )
    parser.add_argument(
        "--year",
        required=True,
        help="YYYY",
    )
    parser.add_argument(
        "--tour",
        required=True,
        help="ATP of CH",
    )
    parser.add_argument("--tid", required=False, help="Tournament ID")

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    tournament = get_tournament_by_id(
        year=args.year,
        tour=args.tour,
        tournament_id=args.tid,
    )
    import json

    print(json.dumps(tournament, indent=4))


if __name__ == "__main__":
    main()
