"""Tests for the Show record class, using handmade records and no network."""

import unittest

import pytest

from tvsummary import Show


class TestShow(unittest.TestCase):
    """Check that Show keeps good values and cleans missing ones."""

    def test_complete_record_is_kept(self):
        """A complete record keeps all of its values."""
        show = Show(
            {
                "name": "Test Show",
                "language": "English",
                "genres": ["Drama", "Comedy"],
                "rating": {"average": 8.5},
            }
        )
        self.assertEqual(show.name, "Test Show")
        self.assertEqual(show.language, "English")
        self.assertEqual(show.genres, ["Drama", "Comedy"])
        self.assertEqual(show.rating, 8.5)

    def test_missing_values_are_cleaned(self):
        """Missing or empty values become safe defaults."""
        show = Show(
            {
                "name": "Bare Show",
                "language": None,
                "genres": None,
                "rating": {"average": None},
            }
        )
        self.assertIsNone(show.language)
        self.assertEqual(show.genres, [])
        self.assertIsNone(show.rating)

    def test_empty_record_does_not_crash(self):
        """A record with no keys at all still produces a Show."""
        show = Show({})
        self.assertEqual(show.name, "(unknown)")
        self.assertEqual(show.genres, [])
        self.assertIsNone(show.rating)

    def test_str_contains_the_name(self):
        """The text version of a Show includes its name."""
        show = Show({"name": "Test Show", "language": "English", "genres": ["Drama"]})
        self.assertIn("Test Show", str(show))


def test_missing_genre_list_becomes_empty_list(complete_show_data):
    """A record with no genres key gets an empty genre list."""
    del complete_show_data["genres"]
    show = Show(complete_show_data)
    assert show.genres == []


@pytest.mark.parametrize(
    "rating_value",
    [
        pytest.param({}, id="empty rating dict"),
        pytest.param({"average": None}, id="average is None"),
        pytest.param(None, id="rating is None"),
        pytest.param("missing", id="no rating key at all"),
    ],
)
def test_missing_rating_becomes_none(complete_show_data, rating_value):
    """Every way of leaving out a rating ends up as None."""
    if rating_value == "missing":
        del complete_show_data["rating"]
    else:
        complete_show_data["rating"] = rating_value
    show = Show(complete_show_data)
    assert show.rating is None


if __name__ == "__main__":
    unittest.main()
