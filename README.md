# tvsummary

A Python package that downloads TV shows from the TVmaze API and writes a JSON summary: record count, unique languages, top genres and average rating per language.

## Data source

- URL: https://api.tvmaze.com/shows?page=0
- One record represents one TV show.
- The page returns about 240 shows.

## Setup

```bash
conda env create -f environment.yml
conda activate tvsummary
pip install -r requirements.txt
pip install -e .
```

## Run

```bash
python main.py
```

The summary is written to `data/processed/summary.json`. If the download fails, the program prints a clear message and stops without a traceback.

## Test

```bash
python -m unittest discover -s tests
```

## Layout

- `main.py`: thin entry point. It wires the pieces together and prints messages.
- `src/tvsummary/config.py`: the URL, timeout and output path, so settings live in one place.
- `src/tvsummary/models.py`: the `Show` class. It represents one record and cleans its own values.
- `src/tvsummary/sources.py`: the `TVMazeSource` class. It downloads the data and is the only module that imports `requests`.
- `src/tvsummary/aggregations.py`: the `Aggregation` base class and its four subclasses.
- `src/tvsummary/report.py`: builds the summary and writes it to JSON.
- `tests/test_models.py`: unit tests for `Show`, using handmade records and no network.

## What moved where

| Lab 02 function | Where it lives now |
|---|---|
| `fetch_records` | `TVMazeSource.fetch` in `sources.py` |
| `shows_per_genre` | inside `TopGenres.compute` in `aggregations.py` |
| `unique_languages` | `UniqueLanguages.compute` in `aggregations.py` |
| `get_count` | `TopGenres._get_count` in `aggregations.py` |
| `top_genres` | `TopGenres.compute` in `aggregations.py` |
| `average_rating_by_language` | `AverageRatingByLanguage.compute` in `aggregations.py` |
| `build_summary` | `build_summary` in `report.py` (loops over aggregation objects) |
| `write_summary` | `write_summary` in `report.py` |
| `main` | `main` in `main.py` |
| `URL`, `Output` | `URL`, `OUTPUT_PATH` in `config.py` |
| missing-value checks (`or []`, `.get`) | `Show.__init__` in `models.py` |

## Design choices

- **`Show`** represents one record. It cleans missing or malformed values when it is created, so the rest of the code can trust every `Show`.
- **`TVMazeSource`** is responsible only for getting the data. It returns `Show` objects instead of raw dictionaries, and it raises `SourceError` when the download fails.
- **`Aggregation`** is a base class. It stores the key used in the summary and defines a `compute` method. `RecordCount`, `UniqueLanguages`, `TopGenres` and `AverageRatingByLanguage` are subclasses that override `compute`. `build_summary` calls `compute` on each object without checking its type.
- Adding one more aggregation means writing one new subclass with its own `compute` method and adding an instance of it to the list in `main.py`. Nothing else changes.

## Known limitations

- TVmaze ratings change over time, so `average_rating_by_language` can differ slightly between days. Running the Lab 02 program and this package on the same day gave identical summaries.
- Only the first page of shows is downloaded.
- The program needs an internet connection to run.
- The tests cover the `Show` class only. A fuller test suite is planned for Lab 04.