"""Build the summary from aggregation objects and write it to a JSON file."""

import json

from .config import URL


def build_summary(shows, aggregations, source_url=URL):
    """Run every aggregation on the shows and combine the results in one dict."""
    summary = {"source_url": source_url}
    for aggregation in aggregations:
        summary[aggregation.key] = aggregation.compute(shows)
    return summary


def write_summary(summary, path):
    """Write the summary to a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
