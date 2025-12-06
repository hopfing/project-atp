import random
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

from base_job import BaseJob


class Extractor(BaseJob):

    BASE_URL = "https://www.atptour.com/en/"
    STATS_URL = "-/Hawkeye/MatchStats/Complete/"

    def __init__(self, tournament: dict, session: requests.Session = None):
        super().__init__(tournament=tournament)
        self.session = session or requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/138.0.0.0 Safari/537.36"
                ),
                "Referer": "https://www.atptour.com/",
                "Origin": "https://www.atptour.com",
                "Accept-Language": "en-US,en;q=0.9",
            }
        )

    def _fetch_content(
        self,
        url: str,
        content_type: str,
        retries=3,
    ):
        """

        :param content_type: JSON or HTML
        :param retries:
        :return:
        """
        for attempt in range(retries + 1):
            time.sleep(random.uniform(0.25, 0.75))

            resp = self.session.get(url, timeout=15)
            resp.raise_for_status()

            if content_type.lower() == "json":
                return resp.json()
            if content_type.lower() == "html":
                return BeautifulSoup(resp.text, "html.parser")

    def _get_match_json(self, match_id):

        stats_url = urljoin(
            self.BASE_URL, f"{self.STATS_URL}{self.year}/{self.tourney_id}/{match_id}"
        )
        match_json = self._fetch_content(
            url=stats_url,
            content_type="json",
        )

        return match_json

    def _get_matches(self):

        match_list = self._get_results_list()

        for match in match_list:
            file_path = self._path(
                bucket="raw",
                filename=f"match_{match}.json",
                mode="write",
            )
            match_json = self._get_match_json(match)
            self.save_json(
                data=match_json,
                path=file_path,
            )

    def _get_results_list(self):

        results_url = urljoin(self.BASE_URL, self.tournament["ScoresUrl"])
        soup = self._fetch_content(
            url=results_url,
            content_type="html",
        )

        match_ids = []
        for link in soup.find_all("a", href=True, string="Stats"):
            match_id = link["href"].split("/")[-1]
            match_ids.append(match_id)

        return match_ids

    def run(self):

        self._get_matches()
