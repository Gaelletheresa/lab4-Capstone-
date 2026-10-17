"""Entry point: download the shows, build the summary and write it."""

import sys

from tvsummary import (
    AverageRatingByLanguage,
    RecordCount,
    SourceError,
    TopGenres,
    TVMazeSource,
    UniqueLanguages,
    build_summary,
    write_summary,
)
from tvsummary.config import OUTPUT_PATH


def main():
    """Download the shows, build the summary and write summary.json."""
    try:
        shows = TVMazeSource().fetch()
    except SourceError as err:
        print(f"Error fetching records: {err}")
        sys.exit(1)

    aggregations = [
        RecordCount(),
        UniqueLanguages(),
        TopGenres(),
        AverageRatingByLanguage(),
    ]
    summary = build_summary(shows, aggregations)
    write_summary(summary, OUTPUT_PATH)
    print(f"Wrote summary of {len(shows)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
