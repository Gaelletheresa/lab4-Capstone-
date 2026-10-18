"""Errors that the tvsummary package raises on purpose."""


class TVSummaryError(Exception):
    """Base class for every error this package raises on purpose."""


class SourceError(TVSummaryError):
    """Raised when the shows cannot be downloaded."""


class DataShapeError(TVSummaryError):
    """Raised when the downloaded response does not have the expected shape."""


class SettingsError(TVSummaryError):
    """Raised when the settings file is missing, unreadable or incomplete."""
