"""Settings for the tvsummary package, read from a TOML file."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

from .errors import SettingsError

DEFAULT_CONFIG_PATH = Path("config/tvsummary.toml")

# Old constants: still used until the other modules switch to Settings.
URL = "https://api.tvmaze.com/shows?page=0"
TIMEOUT = 10
OUTPUT_PATH = Path("data/processed/summary.json")


@dataclass(frozen=True)
class Settings:
    """Every setting the program reads. Frozen, so it cannot change mid-run."""

    source_url: str
    timeout: float
    output_dir: Path
    seed: int
    sample_size: int
    log_level: str


def load_settings(path: Path = DEFAULT_CONFIG_PATH) -> Settings:
    """Read the TOML file at path and return a Settings object."""
    try:
        with path.open("rb") as file:
            data = tomllib.load(file)
    except OSError as err:
        raise SettingsError(f"Could not read settings file {path}: {err}") from err
    except tomllib.TOMLDecodeError as err:
        raise SettingsError(f"Settings file {path} is not valid TOML: {err}") from err

    try:
        return Settings(
            source_url=str(data["source_url"]),
            timeout=float(data["timeout"]),
            output_dir=Path(str(data["output_dir"])),
            seed=int(data["seed"]),
            sample_size=int(data["sample_size"]),
            log_level=str(data["log_level"]),
        )
    except KeyError as err:
        raise SettingsError(
            f"Settings file {path} is missing the setting {err.args[0]}"
        ) from err
    except (TypeError, ValueError) as err:
        raise SettingsError(f"Settings file {path} has a bad value: {err}") from err
