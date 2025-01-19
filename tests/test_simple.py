"""Sample test_simple.py file"""

import unittest

from gradescope_utils.autograder_utils.decorators import number, weight


class TestLabX(unittest.TestCase):
    """Class to test the student's submission."""

    def setUp(self) -> None:
        """Set up the tests.

        Runs before every test.
        """
        ...

    @weight(10)
    @number("0")
    def test_func(self) -> None:
        """Test whether loading breeds works."""
        assert True
