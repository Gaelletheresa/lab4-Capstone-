"""Record class for one TV show."""

from typing import Any


class Show:
    """One TV show from the TVmaze API, with its values cleaned on creation."""

    def __init__(self, raw: dict[str, Any]) -> None:
        """Build a Show from one raw dictionary and clean its values here."""
        self.name: str = raw.get("name") or "(unknown)"
        self.language: str | None = raw.get("language") or None
        self.genres: list[str] = raw.get("genres") or []
        rating_info = raw.get("rating") or {}
        self.rating: float | None = rating_info.get("average")

    def __str__(self) -> str:
        """Return a short readable description of the show."""
        genres = ", ".join(self.genres) if self.genres else "no genre listed"
        rating = self.rating if self.rating is not None else "no rating"
        return (
            f"{self.name} ({self.language or 'unknown language'}) - {genres} - {rating}"
        )