"""Entry point: python -m tvsummary.main [--config PATH]."""

import argparse
import logging
import sys
from pathlib import Path

from .aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    FeaturedShows,
    RecordCount,
    TopGenres,
    UniqueLanguages,
)
from .config import DEFAULT_CONFIG_PATH, load_settings
from .errors import SettingsError, TVSummaryError
from .logging_setup import configure_logging
from .report import build_summary, write_summary
from .run_info import build_run_info, write_run_info
from .sources import TVMazeSource

logger = logging.getLogger(__name__)


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    """Read the command line options."""
    parser = argparse.ArgumentParser(description="Summarize TV shows from TVmaze.")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="path to the TOML settings file",
    )
    return parser.parse_args(argv)


def fail(err: TVSummaryError) -> int:
    """Log an expected failure, print one Error line to stderr, return 1."""
    logger.error("Run failed: %s", err)
    print(f"Error: {err}", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    """Run the whole program. Return 0 on success and 1 on an expected failure."""
    args = parse_args(argv)

    try:
        settings = load_settings(args.config)
    except SettingsError as err:
        configure_logging("INFO")
        return fail(err)

    configure_logging(settings.log_level)
    summary_path = settings.output_dir / "summary.json"
    run_info_path = settings.output_dir / "run_info.json"

    try:
        shows = TVMazeSource(settings.source_url, settings.timeout).fetch()
        aggregations: list[Aggregation] = [
            RecordCount(),
            UniqueLanguages(),
            TopGenres(),
            AverageRatingByLanguage(),
            FeaturedShows(settings.seed, settings.sample_size),
        ]
        summary = build_summary(shows, aggregations, settings.source_url)
        write_summary(summary, summary_path)
        write_run_info(build_run_info(settings), run_info_path)
    except TVSummaryError as err:
        return fail(err)

    print(f"Wrote summary of {len(shows)} records to {summary_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
