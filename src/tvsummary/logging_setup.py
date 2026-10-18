"""Configure logging for the whole program. Called once, from main()."""

import logging

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


def configure_logging(level: str = "INFO") -> None:
    """Send log messages to standard error at the given level."""
    logging.basicConfig(level=level.upper(), format=LOG_FORMAT)
