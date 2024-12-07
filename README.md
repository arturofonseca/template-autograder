# Getting started with the autograder

## Prerequisites

Download dependencies

```bash
pip install -r requirements.txt
```

## Files

**Files to modify (mandatory):**
- `config.json`: configuration settings for this lab

Files to modify (optional):
- `requirements.txt`: dependencies for this lab (**do not modify lines 1-3**)
- `tests/test_simple.py`: unit tests for this lab

> _Additionally, the `tests/`directory and `run_tests.py` can be deleted entirely if not using Gradescope utilities to autograde_

Files to add (optional):
- Any data or additional Python files should be added to the project root
**Note**: all other provided files should be left unmodified

### `config.json`
Required keys in this file are:
- `lab_name` (string): name for this lab
- `files_needed` (list of strings): list of file names students need to submit
- `max_submissions` (integer or null): a non-negative integer denoting the max number a student can submit; if no limit, set to `null`
- `max_late_days` (integer): non-negative integer denoting how many days students have to submit before they get a 0
- `no_penalty_days` (integer): non-negative integer denoting how many days a student can submit past the due date without a deduction
- `penalty` (integer): non-negative integer denoting what to reduce a student's score by each day it's late 
- `extensions` (object): a dictionary of student emails to a dictionary of their unique extension 
  circumstances
  - Leave empty if there are no extensions (`{}`)
  - Each dictionary must has `no_penalty_days` key. `max_late_days` and `penalty` are optional.
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
      "max_submissions": false, // (optional) unlimited submissions
      // "penalty" (optional) not specified here, so use the one above
    }
  }
}
```

> This file is validated when `grader.py` is run, so that any errors in the format
> are caught before grading a student's submission (see `config.schema.json`).
> 

### `tests/test_simple.py`

Add tests specific to this lab.

### `requirements.txt`

Add any packages necessary to run Python files.