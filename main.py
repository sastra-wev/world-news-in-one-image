#!/usr/bin/env python3
"""Entry point for the make.fun 'news-image-20261118' bounty.

Writes the pre-rendered front page (entry.png, committed next to this file)
to /output/entry.png. The asset is copied byte-for-byte, so every run
produces identical output. No network, no dependencies beyond the stdlib.
The page itself is drawn by render.py (kept in the repo for provenance).
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main():
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    print(f"wrote {DST} ({os.path.getsize(DST)} bytes)")


if __name__ == "__main__":
    main()
