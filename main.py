#!/usr/bin/env python3
"""Copy the entry image to the output directory.

Reads entry.png from this repository and writes it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
Standard library only.
"""

import os
import shutil
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG"


def resolve_source():
    """Return the path of the entry image shipped with this repository."""
    return Path(__file__).resolve().parent / "entry.png"


def resolve_output_dir():
    """Return the directory main.py must write into."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def validate_png(path):
    """Check path is a regular file that starts with the PNG magic bytes."""
    if not path.exists():
        raise FileNotFoundError("entry image not found: %s" % path)
    if not path.is_file():
        raise ValueError("entry image is not a regular file: %s" % path)
    with open(path, "rb") as handle:
        header = handle.read(len(PNG_MAGIC))
    if header != PNG_MAGIC:
        raise ValueError("entry image lacks the PNG magic bytes: %s" % path)


def copy_entry(source, out_dir):
    """Validate the entry image and copy it into out_dir as entry.png."""
    validate_png(source)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    return target


def main():
    try:
        target = copy_entry(resolve_source(), resolve_output_dir())
    except (OSError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    print("wrote %s" % target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
