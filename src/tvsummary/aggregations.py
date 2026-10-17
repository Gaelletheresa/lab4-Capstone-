"""Aggregations over Show records: one base class and four subclasses."""


class Aggregation:
    """Base class: each aggregation has a summary key and a compute method."""

    def __init__(self, key):
        """Store the key under which the result appears in the summary."""
        self.key = key

    def compute(self, shows):
        """Return the result for this aggregation. Subclasses must override."""
        raise NotImplementedError("Subclasses must override compute().")


class RecordCount(Aggregation):
    """Counts how many shows were processed."""

    def __init__(self):
        """Use the key records_processed."""
        super().__init__("records_processed")

    def compute(self, shows):
        """Return the number of shows."""
        return len(shows)


class UniqueLanguages(Aggregation):
    """Lists the unique languages found in the shows."""

    def __init__(self):
        """Use the key unique_languages."""
        super().__init__("unique_languages")

    def compute(self, shows):
        """Return the sorted list of unique languages."""
        return sorted({show.language for show in shows if show.language})


class TopGenres(Aggregation):
    """Finds the genres with the most shows."""

    def __init__(self, n=6):
        """Use the key top_genres and keep the top n genres."""
        super().__init__("top_genres")
        self.n = n

    def compute(self, shows):
        """Return the top n genres as (genre, count) tuples."""
        counts = {}
        for show in shows:
            if not show.genres:
                counts["(no genre listed)"] = counts.get("(no genre listed)", 0) + 1
            for genre in show.genres:
                counts[genre] = counts.get(genre, 0) + 1
        pairs = list(counts.items())
        pairs.sort(key=self._get_count, reverse=True)
        return pairs[: self.n]

    @staticmethod
    def _get_count(item):
        """Return the count from a genre and count pair."""
        return item[1]


class AverageRatingByLanguage(Aggregation):
    """Averages the show ratings for each language."""

    def __init__(self):
        """Use the key average_rating_by_language."""
        super().__init__("average_rating_by_language")

    def compute(self, shows):
        """Return a dictionary of average rating per language."""
        ratings = {}
        for show in shows:
            if show.language and show.rating is not None:
                if show.language not in ratings:
                    ratings[show.language] = []
                ratings[show.language].append(show.rating)

        averages = {}
        for language, rating_list in ratings.items():
            averages[language] = sum(rating_list) / len(rating_list)
        return averages
