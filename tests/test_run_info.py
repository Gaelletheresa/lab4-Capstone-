"""Tests for run_info.json, using temporary files and no network."""

import json
from importlib import metadata
from pathlib import Path

import pytest

from tvsummary import run_info
from tvsummary.config import Settings
from tvsummary.run_info import build_run_info, tool_version, write_run_info


@pytest.fixture
def settings():
    """Return a Settings object with hand-made values."""
    return Settings(
        source_url="https://example.invalid/shows",
        timeout=5.0,
        output_dir=Path("out"),
        seed=7,
        sample_size=3,
        log_level="INFO",
    )


def test_run_info_records_settings_python_and_tools(settings):
    """The run info holds the settings, the Python version and tool versions."""
    info = build_run_info(settings)
    assert info["settings"]["seed"] == 7
    assert info["settings"]["output_dir"] == "out"
    assert info["python_version"].startswith("3.")
    assert set(info["tool_versions"]) == {"pytest", "mypy", "ruff"}


def test_write_run_info_creates_valid_json(settings, tmp_path):
    """write_run_info makes missing folders and writes readable JSON."""
    path = tmp_path / "new_folder" / "run_info.json"
    info = build_run_info(settings)
    write_run_info(info, path)
    assert json.loads(path.read_text(encoding="utf-8")) == info


def test_missing_tool_is_recorded_as_not_installed(monkeypatch):
    """A tool that is not installed does not crash the run."""

    def fake_version(name):
        raise metadata.PackageNotFoundError(name)

    monkeypatch.setattr(run_info.metadata, "version", fake_version)
    assert tool_version("ruff") == "not installed"
