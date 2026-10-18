"""Build the summary from aggregation objects and write it to a JSON file."""

import json
import logging

from .config import URL

logger = logging.getLogger(__name__)


def build_summary(shows, aggregations, source_url=URL):
    """Run every aggregation on the shows and combine the results in one dict."""
    summary = {"source_url": source_url}
    for aggregation in aggregations:
        logger.debug("Running aggregation %s", aggregation.key)
        summary[aggregation.key] = aggregation.compute(shows)
    logger.info("Built summary: %s keys, %s shows", len(summary), len(shows))
    return summary


def write_summary(summary, path):
    """Write the summary to a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logger.info("Wrote summary to %s", path)