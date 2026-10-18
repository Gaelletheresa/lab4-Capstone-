# tvsummary

Downloads one page of TV shows from the TVmaze API and writes a JSON summary: record count, unique languages, top genres, average rating by language, and a seeded list of featured shows.

## Setup

```
conda env create -f environment.yml
conda activate tvsummary-lab4
pip install -r requirements.txt
pip install -e .
```

## Run

```
python -m tvsummary.main
python -m tvsummary.main --config config/tvsummary.toml
```

The output goes to `data/processed/summary.json` and `data/processed/run_info.json`.

## Check it

```
python -m ruff format --check .
python -m ruff check .
python -m mypy
python -m pytest
```

## Settings

All settings live in `config/tvsummary.toml`.

- `source_url`: the web address the shows are downloaded from.
- `timeout`: how many seconds to wait for the download before giving up.
- `output_dir`: the folder where `summary.json` and `run_info.json` are written.
- `seed`: the number that makes the random choice of featured shows repeatable.
- `sample_size`: how many show names go into `featured_shows`.
- `log_level`: how much detail the log shows (DEBUG, INFO, WARNING or ERROR).

## Errors and exit codes

| Error class | When it is raised | What the user sees |
| --- | --- | --- |
| `SourceError` | The download fails (no network, timeout, bad HTTP status) | `Error: Could not reach <url>: <reason>` |
| `DataShapeError` | The download works but is not a list of show records | `Error: Expected a list of show records from <url>, but the response had a different shape.` |
| `SettingsError` | The settings file is missing, not valid TOML, incomplete or has a bad value | `Error: Could not read settings file <path>: <reason>` (or "is missing the setting <name>") |

All three inherit from `TVSummaryError`, and only `main()` catches it.

- Exit code `0`: the run succeeded and both JSON files were written.
- Exit code `1`: an expected failure. One line starting with `Error:` goes to standard error, with no traceback.

## Reproducing a run

The seed is in `config/tvsummary.toml` (`seed = 42`, `sample_size = 5`). Every run writes `data/processed/run_info.json`, which records the settings used, the Python version and the versions of pytest, mypy and ruff. To get exactly the same `featured_shows` list, a classmate needs the same seed and sample size, and the same downloaded shows in the same order. The list is chosen from the downloaded data, so if TVmaze changes its data, the list and some averages can change even with the same seed.

## What the tests cover

The tests protect:

- how `Show` cleans missing genres, ratings and languages;
- each aggregation, using hand-made shows;
- that the same seed gives the same `featured_shows` list;
- writing `summary.json` and `run_info.json` into a temporary folder;
- loading the settings file, including the missing, incomplete and invalid cases;
- the error paths of the download, using a fake `requests.get`;
- `main()` exit codes and `Error:` lines.

No test uses the network. One thing I chose not to test is a real download from TVmaze, because a test that depends on the internet fails when the wifi does, and the live data keeps changing.

## Known limitations

- Only the first page of TVmaze shows (`page=0`) is downloaded.
- Averages and featured shows depend on TVmaze's live data, so they can change between days.
- Logging is configured only in `main()`, so using the package from other code produces no log output unless that code configures logging.