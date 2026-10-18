"""tvsummary: summarize TV shows from the TVmaze API."""

from .aggregations import (
    Aggregation,
    AverageRatingByLanguage,
    RecordCount,
    TopGenres,
    UniqueLanguages,
)
from .errors import DataShapeError, SettingsError, SourceError, TVSummaryError
from .models import Show
from .report import build_summary, write_summary
from .sources import TVMazeSource

__all__ = [
    "Aggregation",
    "AverageRatingByLanguage",
    "DataShapeError",
    "RecordCount",
    "SettingsError",
    "Show",
    "SourceError",
    "TVMazeSource",
    "TVSummaryError",
    "TopGenres",
    "UniqueLanguages",
    "build_summary",
    "write_summary",
]
