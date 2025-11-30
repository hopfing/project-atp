import requests

from base_job import BaseJob


class Extractor(BaseJob):

    BASE_URL = "https://www.atptour.com/en/"

    def __init__(self, tournament: str, session: requests.Session = None):
        super().__init__(tournament=tournament)
        self.session = session or requests.Session()


