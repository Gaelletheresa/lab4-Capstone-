"""Tests for main(): exit codes and the printed messages, with no network."""

import json

import pytest

from tvsummary import main as main_module
from tvsummary.errors import SourceError


@pytest.fixture
def config_file(tmp_path):
    """Write a settings file that sends its output into a temporary folder."""
    path = tmp_path / "settings.toml"
    path.write_text(
        f"""
source_url = "https://example.invalid/shows"
timeout = 5
output_dir = "{tmp_path / "out"}"
seed = 42
sample_size = 2
log_level = "INFO"
""",
        encoding="utf-8",
    )
    return path


def test_successful_run_returns_zero_and_writes_both_files(
    monkeypatch, sample_shows, config_file, tmp_path, capsys
):
    """A good run returns 0, prints the result and writes both JSON files."""
    monkeypatch.setattr(main_module.TVMazeSource, "fetch", lambda self: sample_shows)
    assert main_module.main(["--config", str(config_file)]) == 0
    assert "Wrote summary of 4 records" in capsys.readouterr().out
    summary = json.loads((tmp_path / "out" / "summary.json").read_text("utf-8"))
    assert len(summary["featured_shows"]) == 2
    assert (tmp_path / "out" / "run_info.json").exists()


def test_missing_settings_file_returns_one_with_an_error_line(tmp_path, capsys):
    """A missing settings file gives exit code 1 and one Error: line."""
    code = main_module.main(["--config", str(tmp_path / "nope.toml")])
    err = capsys.readouterr().err
    assert code == 1
    assert err.strip().splitlines()[-1].startswith("Error: Could not read")
    assert "Traceback" not in err


def test_failed_download_returns_one_with_an_error_line(
    monkeypatch, config_file, capsys
):
    """A failed download gives exit code 1 and one Error: line, no traceback."""

    def fake_fetch(self):
        raise SourceError("Could not reach the test server")

    monkeypatch.setattr(main_module.TVMazeSource, "fetch", fake_fetch)
    code = main_module.main(["--config", str(config_file)])
    err = capsys.readouterr().err
    assert code == 1
    assert "Error: Could not reach the test server" in err
    assert "Traceback" not in err
