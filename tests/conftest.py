"""Shared fixtures for the tvsummary tests."""

import pytest

from tvsummary import Show


@pytest.fixture
def complete_show_data():
    """Return a raw TVmaze-style dictionary for one complete show."""
    return {
        "name": "Test Show",
        "language": "English",
        "genres": ["Drama", "Comedy"],
        "rating": {"average": 8.5},
    }


@pytest.fixture
def sample_shows():
    """Return four hand-made shows that cover the awkward cases."""
    return [
        Show(
            {
                "name": "Alpha",
                "language": "English",
                "genres": ["Drama", "Comedy"],
                "rating": {"average": 8.0},
            }
        ),
        Show(
            {
                "name": "Beta",
                "language": "English",
                "genres": ["Drama"],
                "rating": {"average": 6.0},
            }
        ),
        Show(
            {
                "name": "Gamma",
                "language": "French",
                "genres": [],
                "rating": {"average": None},
            }
        ),
        Show(
            {
                "name": "Delta",
                "language": None,
                "genres": ["Comedy"],
                "rating": {"average": 7.0},
            }
        ),
    ]