#!/usr/bin/env python3
"""Publish this entry's single joke as entry.txt.

Running the module drops one line of text into the folder the
harness points MAKEFUN_OUTPUT_DIR at (falling back to /output),
which is the whole submission for One Line, One Laugh.
"""

import os
import sys
from pathlib import Path

JOKE = "After my third wrong turn, my GPS said 'recalculating' with such patience that I could hear a machine learning to lower its expectations."
MAX_CHARS = 200


def joke_problems(text):
    """Collect every reason this text cannot be entered."""
    problems = []
    if not isinstance(text, str):
        problems.append("the joke is not text")
        return problems
    if len(text) == 0 or len(text) > MAX_CHARS:
        problems.append("the joke must be 1 to 200 characters long")
    if text.strip() == "":
        problems.append("the joke must not be blank")
    if any(mark in text for mark in ("\n", "\r")):
        problems.append("the joke must fit on one line")
    return problems


def target_folder():
    """Resolve where entry.txt belongs, ignoring stray spaces."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    cleaned = raw.strip()
    return Path(cleaned) if cleaned else Path("/output")


def publish():
    problems = joke_problems(JOKE)
    if problems:
        for problem in problems:
            print("cannot publish: " + problem, file=sys.stderr)
        return 1
    folder = target_folder()
    folder.mkdir(parents=True, exist_ok=True)
    staging = folder / ".entry.txt.part"
    try:
        staging.write_bytes((JOKE + "\n").encode("utf-8"))
        staging.chmod(0o644)
        staging.replace(folder / "entry.txt")
    except BaseException:
        try:
            staging.unlink(missing_ok=True)
        except OSError:
            pass
        raise
    return 0


if __name__ == "__main__":
    sys.exit(publish())
