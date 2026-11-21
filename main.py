#!/usr/bin/env python3
"""Entry program for news-image-20261121.

Copies the pre-drawn front page (news.png, built by build_image.py) to
the make.fun output location. Standard library only, no network, and
fully deterministic: the same input bytes always produce the same output.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "news.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(SRC, "rb") as src, open(dest, "wb") as dst:
        shutil.copyfileobj(src, dst)
    print("wrote", dest)


if __name__ == "__main__":
    sys.exit(main())
