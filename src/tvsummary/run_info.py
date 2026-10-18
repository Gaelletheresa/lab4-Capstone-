"""Record how a run was made, so someone else can repeat it."""

import json
import logging
import platform
from dataclasses import asdict
from importlib import metadata
from pathlib import Path
from typing import Any

from .config import Settings

logger = logging.getLogger(__name__)

TOOLS = ("pytest", "mypy", "ruff")


def tool_version(name: str) -> str:
    """Return the installed version of a tool, or 'not installed'."""
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        logger.warning("Tool %s is not installed; version not recorded", name)
        return "not installed"


def build_run_info(settings: Settings) -> dict[str, Any]:
    """Collect the settings, Python version and tool versions for this run."""
    settings_data = {
        key: str(value) if isinstance(value, Path) else value
        for key, value in asdict(settings).items()
    }
    return {
        "settings": settings_data,
        "python_version": platform.python_version(),
        "tool_versions": {name: tool_version(name) for name in TOOLS},
    }


def write_run_info(run_info: dict[str, Any], path: Path) -> None:
    """Write the run information to a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(run_info, indent=2), encoding="utf-8")
    logger.info("Wrote run info to %s", path)
