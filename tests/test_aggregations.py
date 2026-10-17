"""Tests for the aggregation classes, using handmade records and no network."""

from tvsummary.aggregations import RecordCount, UniqueLanguages


def test_record_count_counts_every_show(sample_shows):
    """RecordCount returns the number of shows it is given."""
    assert RecordCount().compute(sample_shows) == 4


def test_unique_languages_are_sorted_and_skip_missing(sample_shows):
    """UniqueLanguages returns each language once, sorted, ignoring None."""
    assert UniqueLanguages().compute(sample_shows) == ["English", "French"]