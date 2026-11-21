#!/usr/bin/env python3
"""Entry for make.fun bounty "Sum up 21 November's world news in one image".

Writes the bundled entry.png to the output directory as entry.png.
Deterministic: a byte-for-byte copy, identical on every run. No network.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(OUT_DIR, "entry.png"))


if __name__ == "__main__":
    main()
