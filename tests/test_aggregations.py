"""Tests for the aggregation classes, using handmade records and no network."""

import logging

import pytest

from tvsummary.aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    RecordCount,
    TopGenres,
    UniqueLanguages,
)


def test_record_count_counts_every_show(sample_shows):
    """RecordCount returns the number of shows it is given."""
    assert RecordCount().compute(sample_shows) == 4


def test_unique_languages_are_sorted_and_skip_missing(sample_shows):
    """UniqueLanguages returns each language once, sorted, ignoring None."""
    assert UniqueLanguages().compute(sample_shows) == ["English", "French"]


def test_top_genres_counts_each_genre_and_missing_genres(sample_shows):
    """TopGenres counts every genre and groups empty lists as no genre listed."""
    result = TopGenres().compute(sample_shows)
    assert dict(result) == {"Drama": 2, "Comedy": 2, "(no genre listed)": 1}


def test_top_genres_keeps_only_the_top_n(sample_shows):
    """TopGenres(n=1) returns a single genre with the highest count."""
    result = TopGenres(n=1).compute(sample_shows)
    assert len(result) == 1
    assert result[0][1] == 2


def test_average_rating_skips_missing_language_and_rating(sample_shows):
    """Only shows with both a language and a rating count toward the average."""
    result = AverageRatingByLanguage().compute(sample_shows)
    assert result == {"English": 7.0}


def test_base_class_compute_must_be_overridden():
    """The base Aggregation class refuses to compute anything itself."""
    with pytest.raises(NotImplementedError, match="override"):
        Aggregation("anything").compute([])


def test_average_rating_warns_about_skipped_shows(sample_shows, caplog):
    """Shows with no language or no rating are skipped and a warning is logged."""
    with caplog.at_level(logging.WARNING, logger="tvsummary.aggregations"):
        AverageRatingByLanguage().compute(sample_shows)
    assert "Skipped 2 shows" in caplog.text
    assert caplog.records[0].levelname == "WARNING"