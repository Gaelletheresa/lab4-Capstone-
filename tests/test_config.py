"""Tests for loading settings, using temporary files and no network."""

from pathlib import Path

import pytest

from tvsummary.config import load_settings
from tvsummary.errors import SettingsError

GOOD_TOML = """
source_url = "https://example.invalid/shows"
timeout = 5
output_dir = "out"
seed = 7
sample_size = 3
log_level = "DEBUG"
"""


def test_valid_file_loads_into_settings(tmp_path):
    """A complete file becomes a Settings object with the right values."""
    path = tmp_path / "settings.toml"
    path.write_text(GOOD_TOML, encoding="utf-8")
    settings = load_settings(path)
    assert settings.seed == 7
    assert settings.output_dir == Path("out")
    assert settings.log_level == "DEBUG"


def test_missing_file_raises_settings_error(tmp_path):
    """A file that does not exist raises SettingsError."""
    with pytest.raises(SettingsError, match="Could not read"):
        load_settings(tmp_path / "nope.toml")


def test_incomplete_file_raises_settings_error(tmp_path):
    """A file without every setting raises SettingsError naming the gap."""
    path = tmp_path / "settings.toml"
    path.write_text("seed = 1\n", encoding="utf-8")
    with pytest.raises(SettingsError, match="missing the setting"):
        load_settings(path)


def test_invalid_toml_raises_settings_error(tmp_path):
    """A file that is not valid TOML raises SettingsError."""
    path = tmp_path / "settings.toml"
    path.write_text("this is not toml", encoding="utf-8")
    with pytest.raises(SettingsError, match="not valid TOML"):
        load_settings(path)
