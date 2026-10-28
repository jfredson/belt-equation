#!/usr/bin/env python3
"""Refuse a built site that carries a note addressed to John.

    python3 scripts/check_site.py            # reads site/dist
    python3 scripts/check_site.py path/to/dist

Added 2026-10-27, ruled by John: the Missions page had shown "draft for John to rewrite"
beside sixteen missions since 2026-10-21. A note for John belongs in the data files and
the docs, never on a public page. This runs after the build, before the deploy.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PHRASES = [
    r"for john",            # "draft for John to rewrite", "a note for John"
    r"john to (rewrite|review|approve|check|read)",
    r"\[draft\b",
    r"\bTODO\b",
    r"\bFIXME\b",
]
PATTERN = re.compile("|".join(PHRASES), re.IGNORECASE)


def check(dist: Path) -> list[str]:
    problems: list[str] = []
    for page in sorted(dist.rglob("*.html")):
        text = page.read_text(encoding="utf-8", errors="replace")
        for m in PATTERN.finditer(text):
            start = max(0, m.start() - 60)
            snippet = re.sub(r"\s+", " ", text[start:m.end() + 60])
            problems.append(f"{page.relative_to(dist)}: …{snippet}…")
    return problems


def main() -> int:
    dist = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "site" / "dist"
    if not dist.is_dir():
        print(f"no built site at {dist}; build it first", file=sys.stderr)
        return 2
    problems = check(dist)
    if problems:
        print("The built site carries text that must not be public:")
        for p in problems:
            print("  " + p)
        return 1
    print(f"check_site: no note addressed to John in {dist}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
