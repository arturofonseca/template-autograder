"""Testing whether all required files are present."""

import unittest

from gradescope_utils.autograder_utils.decorators import weight
from gradescope_utils.autograder_utils.files import check_submitted_files

from processor import SubmissionProcessor

config = SubmissionProcessor.read_json("source", "config.json")


class TestFiles(unittest.TestCase):
    @weight(0)
    def test_submitted_files(self) -> None:
        """Check submitted files."""
        missing_files = check_submitted_files(config["files_needed"])
        for path in missing_files:
            print("Missing {0}".format(path))
        self.assertEqual(len(missing_files), 0, "Missing some required files!")
        print(
            f"All required files submitted!, You're on the right track with {config['lab_name']}!"
        )
