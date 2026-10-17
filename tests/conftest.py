"""Shared fixtures for the tvsummary tests."""

import pytest


@pytest.fixture
def complete_show_data():
    """Return a raw TVmaze-style dictionary for one complete show."""
    return {
        "name": "Test Show",
        "language": "English",
        "genres": ["Drama", "Comedy"],
        "rating": {"average": 8.5},
    }
