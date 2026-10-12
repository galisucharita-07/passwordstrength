
import unittest

from analyzer import analyze_password


class TestPasswordAnalyzer(unittest.TestCase):

    def test_empty_password(self):
        result = analyze_password("")

        self.assertEqual(result["strength"], "No Password")
        self.assertEqual(result["score"], 0)

    def test_common_password(self):
        result = analyze_password("password123")

        self.assertEqual(result["score"], 0)
        self.assertEqual(result["strength"], "Weak")
        self.assertIn(
            "High risk",
            result["checks"]["common_password"]
        )

    def test_repeated_characters(self):
        result = analyze_password("aaaaaaaa")

        self.assertEqual(result["score"], 10)
        self.assertEqual(
            result["checks"]["repeated_characters"],
            "High risk"
        )

    def test_longer_password_has_length(self):
        result = analyze_password("Example-Tree-42!")

        self.assertEqual(result["length"], 16)
        self.assertIn(result["score"], range(101))

    def test_invalid_password_type(self):
        with self.assertRaises(ValueError):
            analyze_password(None)

    def test_password_exceeds_maximum_length(self):
        with self.assertRaises(ValueError):
            analyze_password("a" * 1025)


if __name__ == "__main__":
    unittest.main()
