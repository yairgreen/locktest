"""Held out, hermetic, and runs through the public entry point.

Kept out of the default pytest path on purpose: the build loop iterates
against the unit tests, and this runs once as the execution proof.
"""

import subprocess
import sys


def run(stdin: str) -> str:
    p = subprocess.run(
        [sys.executable, "-m", "adstxt.cli"],
        input=stdin, capture_output=True, text=True, check=True,
    )
    return p.stdout


def test_cli_emits_one_line_per_valid_record():
    out = run("example.com, 1234, DIRECT\n# skip me\nother.com, 99, RESELLER\n")
    assert out.splitlines() == [
        "example.com|1234|DIRECT",
        "other.com|99|RESELLER",
    ]


def test_cli_survives_a_malformed_file():
    assert run(",,,\nnonsense\n") == ""
