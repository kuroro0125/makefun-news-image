#!/usr/bin/env python3
"""Deliver the finished front page for the make.fun news-image bounty.

The picture itself ships inside this repository as ``entry.png``.  This
program's whole job is to place a copy of it where the runner expects
to find the answer: a file called ``entry.png`` inside the directory
named by the MAKEFUN_OUTPUT_DIR environment variable, falling back to
``/output`` when the variable is not set.

Copying bytes instead of redrawing keeps the result perfectly stable:
every run hands over exactly the same file, byte for byte.
"""

from pathlib import Path
import os
import shutil

ANSWER_NAME = "entry.png"
FALLBACK_DIR = "/output"


def destination_dir() -> Path:
    """Return the folder the answer belongs in, creating it if needed."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_DIR
    folder = Path(raw)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def deliver() -> Path:
    """Copy the bundled picture to the runner and report where it went."""
    source = Path(__file__).resolve().parent / ANSWER_NAME
    target = destination_dir() / ANSWER_NAME
    shutil.copyfile(source, target)
    return target


if __name__ == "__main__":
    deliver()
