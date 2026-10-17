"""Tests for building and writing the summary, using handmade records."""

import json

from tvsummary.aggregations import RecordCount, UniqueLanguages
from tvsummary.report import build_summary, write_summary


def test_build_summary_has_source_url_and_every_aggregation_key(sample_shows):
    """The summary holds the source URL plus one key per aggregation."""
    summary = build_summary(
        sample_shows,
        [RecordCount(), UniqueLanguages()],
        source_url="https://example.invalid/shows",
    )
    assert summary == {
        "source_url": "https://example.invalid/shows",
        "records_processed": 4,
        "unique_languages": ["English", "French"],
    }


def test_write_summary_creates_folder_and_valid_json(tmp_path):
    """write_summary makes missing folders and writes readable JSON."""
    summary = {"source_url": "https://example.invalid", "records_processed": 3}
    output_file = tmp_path / "new_folder" / "summary.json"

    write_summary(summary, output_file)

    assert output_file.exists()
    assert json.loads(output_file.read_text(encoding="utf-8")) == summary