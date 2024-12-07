"""
This file modifies a student's autograder score.

This is done by updating results.json, deducting any late points,
and capping their submission count.

Author: Arturo Fonseca
Date: December 10, 2024
"""

import json
import os
from datetime import datetime, timedelta
from math import ceil
from typing import Any

from jsonschema import ValidationError, validate  # type: ignore
from pytz import timezone  # type: ignore


class Grader:
    """A class to handle the grading of student submissions.

    This class reads configuration and submission data, applies grading rules,
    and calculates the final score for a submission based on various criteria
    such as submission limits and late penalties.

    Attributes:
        root (str): The root directory for the grader.
        _config (dict): The config.json data.
        _schema (dict): The schema for config.json.
        _results (dict): The results.json data.
        _metadata (dict): The metadata for the submission.
        _max_submissions (int | None): The maximum number of submissions allowed.
        _max_late_days (int): The maximum number of late days allowed.
        _no_penalty_days (int): The number of days allowed without penalty.
        _penalty (int): The penalty per late day.
        _min_marks (float): The minimum marks for a submission.
        _max_marks (float): The maximum marks for a submission.
        _total_marks (float): The total marks for the current submission.
        _submit_date (datetime): The submission date.
        _due_date (datetime): The due date.
        _exceeded_limit (bool): Whether one has exceeded the submission limit.
    """

    root = "/autograder"

    def __init__(self) -> None:
        """Initialize the Grader instance."""
        # Setup
        self._config = self.read_json("source", "config.json")
        self._schema = self.read_json("source", "config.schema.json")
        self._results = self.read_json("results", "results.json")
        self._metadata = self.read_json("submission_metadata.json")

        # Make sure config.json has valid values
        self._validate_config()

        # Get constants
        constants = self._get_constants()
        self._max_submissions: int | None = constants["max_submissions"]
        self._max_late_days: int = constants["max_late_days"]
        self._no_penalty_days: int = constants["no_penalty_days"]
        self._penalty: int = constants["penalty"]

        # Get submission details
        self._min_marks = 0.0
        self._max_marks = float(self._metadata["assignment"]["total_points"])
        self._total_marks = self._calc_score()
        self._submit_date = datetime.fromisoformat(self._metadata["created_at"])
        self._due_date = datetime.fromisoformat(
            self._metadata["assignment"]["due_date"]
        )
        self._exceeded_limit = False

    def grade(self) -> None:
        """Grade the student's submission."""
        self._limit_submission_count()
        self._apply_late_penalty()

    def _limit_submission_count(self) -> None:
        """Update the score if the submission limit exceeded."""
        # Do nothing if no maximum specified
        if not self._max_submissions:
            return

        # Get their submission count
        previous_submissions = self._metadata.get("previous_submissions", [])
        submission_count = len(previous_submissions) + 1  # This submission

        # If within the limit, just print output
        if submission_count <= self._max_submissions:
            output = (
                f"\n\n*****************************\n"
                f"This is submission {submission_count} of {self._max_submissions}.\n"
                f"After {self._max_submissions} submissions, only submission "
                f"{self._max_submissions}'s score will count.\n"
            )

        # Otherwise, update their score to their last submission's score and print the output
        else:
            self._total_marks = float(previous_submissions[-1]["score"])
            output = (
                f"\n\n*****************************\n"
                f"{self._max_submissions} submissions exceeded ({submission_count} submitted).\n"
                f"Only submission {self._max_submissions}'s score ({self._total_marks}) will count.\n"
            )
            self._exceeded_limit = True

        # Update results.json
        self._results["output"] = self._results.get("output", "") + output
        self._results["score"] = self._total_marks
        self.write_json(self._results, "results", "results.json")

    def _apply_late_penalty(self) -> None:
        """Apply late penalties to the student's submission."""
        # Do nothing if this submission's score won't count anyway
        if self._exceeded_limit:
            return

        # Do nothing if submitted before the due date
        days_past_due = self._calc_days_between(self._due_date, self._submit_date)
        if days_past_due <= 0:
            return

        # Print submission details
        output = (
            f"\n\n*****************************\n"
            f"Submission date is: {self._format_date(self._submit_date)}.\n"
        )
        # If they have an extension, push back the due date
        if self._no_penalty_days > 0:
            self._due_date += timedelta(days=self._no_penalty_days)
            output += (
                f"* {self._no_penalty_days}-DAY EXTENSION *: New date due is "
                f"{self._format_date(self._due_date)}.\n"
            )
            days_past_due = self._calc_days_between(self._due_date, self._submit_date)
        # Otherwise, just print the original due date
        else:
            output += f"Due date is: {self._format_date(self._due_date)}.\n"

        # If late, print how late
        if days_past_due > 0:
            output += (
                f"*** This submission is {ceil(days_past_due)} "
                f"day{self._pluralize(ceil(days_past_due))} late. ***\n"
            )

        # If past the late dateline, their score is min_mark
        if days_past_due > self._max_late_days:
            self._total_marks = self._min_marks
            output += (
                f"Submission past the late deadline: {self._max_late_days} "
                f"day{self._pluralize(self._max_late_days)} after due date "
                f"({self._format_date(self._due_date + timedelta(days=self._max_late_days))}).\n"
                f"Your score is {self._total_marks}.\n"
            )

        # Otherwise, reduce appropriate marks
        else:
            total_penalty = self._penalty * ceil(days_past_due)
            output += (
                f"Reducing {total_penalty} "
                f"mark{self._pluralize(total_penalty)} "
                f"from your score ({self._total_marks}) as per the late submission policy.\n"
            )
            self._total_marks = max(self._min_marks, self._total_marks - total_penalty)

        # Update results.json
        self._results["output"] = self._results.get("output", "") + output
        self._results["score"] = self._total_marks
        self.write_json(self._results, "results", "results.json")

    def _validate_config(self) -> None:
        """Validate the configuration against the schema.

        Raises:
            ValidationError: If the configuration does not match the schema.
        """
        try:
            validate(instance=self._config, schema=self._schema)
        except ValidationError as e:
            raise e

    # HELPERS

    def _get_constants(self) -> dict[str, Any]:
        """Retrieve grading constants from the configuration.

        Returns:
            dict[str, Any]: A dictionary containing the grading constants.
        """
        constants: dict[str, Any] = {}
        ext_constants = self._get_extension_constants()
        keys = {"max_submissions", "max_late_days", "no_penalty_days", "penalty"}

        for key in keys:
            # If a student has an extension, look for any keys present in their dictionary
            # Otherwise, assume top-level constants are the default
            if key in ext_constants:
                value = ext_constants[key]
            else:
                value = self._config[key]

            constants[key] = value

        return constants

    def _get_extension_constants(self) -> dict[str, Any]:
        """Retrieve the extension constants for a student.

        Returns:
            dict[str, Any]: A dictionary containing the extension constants
            if an extension is found, otherwise an empty dictionary.
        """
        submission_emails = [user["email"] for user in self._metadata["users"]]

        for email in submission_emails:
            if email in self._config["extensions"]:
                return self._config["extensions"][email]  # type: ignore

        return {}

    def _calc_score(self) -> float:
        """Calculate a student's score by looking at their results.json.

        Returns:
            float: Their score.
        """
        if "score" in self._results:
            return float(self._results["score"])

        return float(sum(test.get("score", 0) for test in self._results["tests"]))

    @staticmethod
    def _calc_days_between(start_date: datetime, end_date: datetime) -> float:
        """Calculate the number of days between two dates.

        Args:
            start_date (datetime): The starting date.
            end_date (datetime): The ending date.

        Returns:
            float: The number of days (0 if `start_date` <= `end_date`).
        """
        days_late = (end_date - start_date).total_seconds() / (60 * 60 * 24)
        return max(0.0, days_late)

    @staticmethod
    def _format_date(date: datetime) -> str:
        """Return readable date and time format: January 01 at 11:59 PM (UTC-0500).

        Args:
            date (datetime): The date to format.

        Returns:
            str: The formatted date string.
        """
        date = date.astimezone(timezone("America/Chicago"))
        return date.strftime("%B %d at %-I:%M %p (UTC%z)")

    @staticmethod
    def _pluralize(number: int | float) -> str:
        """Determine the plural suffix for a given number.

        Args:
            number (int | float): The number to determine if the word should be pluralized.

        Returns:
            str: An empty string if the number is 1, otherwise 's'.
        """
        return "" if number == 1 else "s"

    @staticmethod
    def read_json(*path_args: str) -> dict[str, Any]:
        """Read and parse a JSON file from the specified path.

        Args:
            *path_args (str): Components of the file path.

        Returns:
            dict[str, Any]: The parsed JSON content as a dictionary.
        """
        with open(os.path.join(Grader.root, *path_args), encoding="utf-8") as f:
            return json.load(f)  # type: ignore

    @staticmethod
    def write_json(json_dict: dict[str, Any], *path_args: str) -> None:
        """Write a dictionary to a JSON file at the specified path.

        Args:
            json_dict (dict[str, Any]): The dictionary to be written to the JSON file.
            *path_args (str): Components of the file path.
        """
        with open(os.path.join(Grader.root, *path_args), "w", encoding="utf-8") as f:
            json.dump(json_dict, f, indent=2)


def main() -> None:
    """Run the program."""
    grader = Grader()
    grader.grade()


if __name__ == "__main__":
    main()
