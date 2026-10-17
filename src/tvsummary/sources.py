"""Download TV show records from the TVmaze API. Only this module uses requests."""

import requests

from .config import TIMEOUT, URL
from .errors import SourceError
from .models import Show


class TVMazeSource:
    """Downloads TV shows from the TVmaze API and returns Show objects."""

    def __init__(self, url=URL, timeout=TIMEOUT):
        """Store the URL and the timeout to use for the download."""
        self.url = url
        self.timeout = timeout

    def fetch(self):
        """Download the shows and return them as a list of Show objects."""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            raw_records = response.json()
        except requests.RequestException as err:
            raise SourceError(f"Could not reach {self.url}: {err}") from err
        return [Show(raw) for raw in raw_records]