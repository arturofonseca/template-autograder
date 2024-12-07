"""Unit tests."""

import unittest

from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover("tests")
    with open("/autograder/results/results.json", "w", encoding="utf-8") as f:
        JSONTestRunner(visibility="visible", stream=f).run(suite)
