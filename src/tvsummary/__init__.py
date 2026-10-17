"""tvsummary: summarize TV shows from the TVmaze API."""
from .aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    RecordCount,
    TopGenres,
    UniqueLanguages,
)
from .models import Show
from .report import build_summary, write_summary
from .sources import SourceError, TVMazeSource

__all__ = [
    "Aggregation",
    "AverageRatingByLanguage",
    "RecordCount",
    "Show",
    "SourceError",
    "TVMazeSource",
    "TopGenres",
    "UniqueLanguages",
    "build_summary",
    "write_summary",
]