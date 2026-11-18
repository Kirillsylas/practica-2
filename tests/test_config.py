import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from main import check_package, check_version, check_output


class TestConfig(unittest.TestCase):

    def test_valid_package(self):
        self.assertEqual(check_package("express"), "express")

    def test_invalid_package(self):
        with self.assertRaises(Exception):
            check_package("Express!")

    def test_valid_version(self):
        self.assertEqual(check_version("4.18.2"), "4.18.2")

    def test_invalid_version(self):
        with self.assertRaises(Exception):
            check_version("abc")

    def test_valid_output(self):
        self.assertEqual(check_output("graph.png"), "graph.png")

    def test_invalid_output(self):
        with self.assertRaises(Exception):
            check_output("graph.txt")


if __name__ == "__main__":
    unittest.main()