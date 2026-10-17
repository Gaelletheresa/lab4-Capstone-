"""Tests for the Show record class, using handmade records and no network."""
import unittest

from tvsummary import Show


class TestShow(unittest.TestCase):
    """Check that Show keeps good values and cleans missing ones."""

    def test_complete_record_is_kept(self):
        """A complete record keeps all of its values."""
        show = Show({
            "name": "Test Show",
            "language": "English",
            "genres": ["Drama", "Comedy"],
            "rating": {"average": 8.5},
        })
        self.assertEqual(show.name, "Test Show")
        self.assertEqual(show.language, "English")
        self.assertEqual(show.genres, ["Drama", "Comedy"])
        self.assertEqual(show.rating, 8.5)

    def test_missing_values_are_cleaned(self):
        """Missing or empty values become safe defaults."""
        show = Show({
            "name": "Bare Show",
            "language": None,
            "genres": None,
            "rating": {"average": None},
        })
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


if __name__ == "__main__":
    unittest.main()