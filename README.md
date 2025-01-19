# Getting started with the autograder

**- Note: the following template is of Lab 2 (see `files/` and `tests/test_simple.py`).**

## Files

**Files to modify (mandatory):**
- `config.json`: configuration settings for this lab.
- `tests/test_simple.py`: unit tests for this lab.

**Files to add (mandatory)**:
- `files/`: Any data or supporting Python files should be added to the `files/` directory.

_Files to modify (optional)_:
- `run_autograder`: the script run by Gradescope automatically.
- `requirements.txt`: dependencies for this lab (**do not modify lines 1-3**).

### `config.json`
Required keys in this file are:
- `lab_name` (string): name for this lab.
- `files_needed` (list of strings): list of file names students need to submit.
- `max_submissions` (integer or null): a non-negative integer denoting the max number a student can submit; if no limit, set to `null`.
- `max_late_days` (integer): non-negative integer denoting how many days students have to submit before they get a 0.
- `no_penalty_days` (integer): non-negative integer denoting how many days a student can submit past the due date without a deduction.
- `penalty` (integer): non-negative integer denoting what to reduce a student's score by each day it's late.
- `extensions` (object): a dictionary of student emails to a dictionary of their unique extension circumstances.
  - Leave empty if there are no extensions (`{}`).
  - Each dictionary must have a `no_penalty_days` key. The `max_late_days` and `penalty` keys are optional.
  - Constants inside each student's dictionary will override the outer-level constants.
    (`"student@email.com": {"no_penalty_days": 7}`). Constants not specified inside a student's
    dictionary will be defaulted to the ones specified above.

Example `config.json`:

```json
{
  "lab_name": "Lab 1",
  "files_needed": [
    "parking.py",
    "alignment.py"
  ],
  "max_submissions": 20,  // 20 submissions allowed (if past, set to previous score)
  "max_late_days": 14,    // 2 weeks allowed (if past, give 0)
  "no_penalty_days": 0,   // by default, no one has an extension
  "penalty": 1,           // -1 point per day
  "extensions": {
    "firstlast2030@u.northwestern.edu": {  // a student's email
      "no_penalty_days": 3,     // 3 days to submit after due date
      "max_submissions": null // (optional) unlimited submissions
      // "penalty" (optional) not specified here, so use the one above
    }
  }
}
```

> This file is validated when `grader.py` is run, so that any errors in the format
> are caught before grading a student's submission (see `config.schema.json`).

### `tests/test_simple.py`

Add tests specific to this lab.

### `files/` directory

Add any files needed to grade the submission here (csv files, `constants.py`, `filereader.py`, etc.).

### `run_autograder`

The `python3 run_tests.py` line can be commented out if not using Gradescope's
unit tests and if you are instead using your own script to grade (like `iograder.py`). In this case,
add your own command to execute your script (`python3 iograder.py`).

> It's important to remember that all student's code and data is in the `files/` directory.

### `requirements.txt`

Add any packages necessary to run Python files.
