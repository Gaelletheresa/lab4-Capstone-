"""Tests for downloading shows, with the network replaced by fakes."""
import logging

import pytest
import requests

from tvsummary import sources
from tvsummary.errors import DataShapeError, SourceError
from tvsummary.sources import TVMazeSource


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
    with pytest.raises(SourceError, match="reach"):
        TVMazeSource("https://example.invalid", timeout=1).fetch()


def test_a_good_download_returns_show_objects(monkeypatch):
    """A successful download is turned into Show objects."""
    raw_records = [{"name": "One"}, {"name": "Two", "language": "English"}]
    monkeypatch.setattr(
        sources.requests, "get", lambda *args, **kwargs: FakeResponse(raw_records)
    )
    shows = TVMazeSource("https://example.invalid", timeout=1).fetch()
    assert [show.name for show in shows] == ["One", "Two"]


@pytest.mark.parametrize(
    "bad_data",
    [
        pytest.param({"error": "not a list"}, id="dict instead of list"),
        pytest.param(["just a string"], id="list of non-dictionaries"),
    ],
)
def test_unexpected_response_shape_raises_data_shape_error(monkeypatch, bad_data):
    """A response that is not a list of dictionaries raises DataShapeError."""
    monkeypatch.setattr(
        sources.requests, "get", lambda *args, **kwargs: FakeResponse(bad_data)
    )
    with pytest.raises(DataShapeError, match="list of show"):
        TVMazeSource("https://example.invalid", timeout=1).fetch()  


def test_a_good_download_logs_how_many_records_arrived(monkeypatch, caplog):
    """A successful download logs the record count at DEBUG level."""
    raw_records = [{"name": "One"}, {"name": "Two"}]
    monkeypatch.setattr(
        sources.requests, "get", lambda *args, **kwargs: FakeResponse(raw_records)
    )
    with caplog.at_level(logging.DEBUG, logger="tvsummary.sources"):
        TVMazeSource("https://example.invalid", timeout=1).fetch()
    assert "Received 2 records" in caplog.text