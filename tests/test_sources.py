"""Tests for downloading shows, with the network replaced by fakes."""

import pytest
import requests

from tvsummary import sources
from tvsummary.sources import SourceError, TVMazeSource


class FakeResponse:
    """A stand-in for a requests response that returns fixed data."""

    def __init__(self, data):
        """Store the data that json() will return."""
        self.data = data

    def raise_for_status(self):
        """Pretend the download succeeded."""

    def json(self):
        """Return the stored data."""
        return self.data


def test_a_failed_download_raises_a_source_error(monkeypatch):
    """If requests.get fails, fetch raises SourceError with the original text."""

    def fake_get(*args, **kwargs):
        raise requests.ConnectionError("no network")

    monkeypatch.setattr(sources.requests, "get", fake_get)
    with pytest.raises(SourceError, match="no network"):
        TVMazeSource("https://example.invalid", timeout=1).fetch()


def test_a_good_download_returns_show_objects(monkeypatch):
    """A successful download is turned into Show objects."""
    raw_records = [{"name": "One"}, {"name": "Two", "language": "English"}]
    monkeypatch.setattr(
        sources.requests, "get", lambda *args, **kwargs: FakeResponse(raw_records)
    )
    shows = TVMazeSource("https://example.invalid", timeout=1).fetch()
    assert [show.name for show in shows] == ["One", "Two"]