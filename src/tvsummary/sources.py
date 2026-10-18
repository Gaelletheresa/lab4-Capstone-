"""Download TV show records from the TVmaze API. Only this module uses requests."""

import logging

import requests

from .config import TIMEOUT, URL
from .errors import DataShapeError, SourceError
from .models import Show

logger = logging.getLogger(__name__)


class TVMazeSource:
    """Downloads TV shows from the TVmaze API and returns Show objects."""

    def __init__(self, url=URL, timeout=TIMEOUT):
        """Store the URL and the timeout to use for the download."""
        self.url = url
        self.timeout = timeout

    def fetch(self):
        """Download the shows and return them as a list of Show objects."""
        logger.info("Downloading shows from %s", self.url)
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            raw_records = response.json()
        except requests.RequestException as err:
            raise SourceError(f"Could not reach {self.url}: {err}") from err
        if not isinstance(raw_records, list) or not all(
            isinstance(raw, dict) for raw in raw_records
        ):
            raise DataShapeError(
                f"Expected a list of show records from {self.url}, "
                "but the response had a different shape."
            )
        logger.debug("Received %s records", len(raw_records))
        return [Show(raw) for raw in raw_records]