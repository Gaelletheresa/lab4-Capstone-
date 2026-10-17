"""Settings for the tvsummary package."""
from pathlib import Path

URL = "https://api.tvmaze.com/shows?page=0"
TIMEOUT = 10
OUTPUT_PATH = Path("data/processed/summary.json")