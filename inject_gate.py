#!/usr/bin/env python3
"""
Injects gate-snippet.html (the passcode-gate <script>) as the very first
child of <head> in one or more target HTML files. Idempotent — skips a file
that already has the gate (matched by id="ts-gate") rather than duplicating
it, so it's safe to run on every refresh.

Must run BEFORE any other content in <head> so the page never flashes
unprotected content — that's why it's inserted right after the opening
<head> tag, not appended at the end.

Usage:
    python3 inject_gate.py index.html ceo-dashboard/index.html meta-report/index.html
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SNIPPET = (ROOT / "gate-snippet.html").read_text()


def inject(path: Path) -> None:
    html = path.read_text()
    if 'id="ts-gate"' in html:
        print(f"  {path}: already gated, skipping")
        return
    new_html, n = re.subn(r"(<head[^>]*>)", r"\1\n" + SNIPPET, html, count=1)
    if n == 0:
        print(f"  {path}: no <head> tag found, skipped")
        return
    path.write_text(new_html)
    print(f"  {path}: gated")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for arg in sys.argv[1:]:
        inject(ROOT / arg)


if __name__ == "__main__":
    main()
