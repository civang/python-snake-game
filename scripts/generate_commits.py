#!/usr/bin/env python3
"""Script moved into scripts/ to keep repo root clean.

Usage: python scripts/generate_commits.py [options]
"""
from pathlib import Path
from generate_commits import main as _main


if __name__ == '__main__':
    # re-export the original script from scripts/
    _main()
