#!/usr/bin/env python3
"""Generate the outside-review packets (docs/reviews/protocol.md, roadmap step 27).

    python3 scripts/review_packets.py            write docs/reviews/packets/<date>-<packet>.md
    python3 scripts/review_packets.py --date D   use a different date stamp

Each packet is the brief (docs/reviews/brief.md) followed by every node in its factors, rendered
in plain text from data/, then the scenario table and the tier requirement lists. Standard
library only. The access branch is never packaged before pipeline graduation (May 2027).
"""
from __future__ import annotations
import argparse, datetime, sys
from pathlib import Path
try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    import tomli as tomllib  # type: ignore

ROOT = Path(__file__).resolve().parent.parent
PACKETS = {
    "window-biology": ["W", "B"],
    "launch-energy-drive": ["L", "E", "D"],
    "motive-regime-contact": ["M", "R", "C"],
}
FACTOR_NAMES = {"W": "Window", "L": "Launch", "E": "Energy", "D": "Drive", "B": "Biology",
                "M": "Motive", "R": "Regime", "C": "Contact Clause"}
FILES = {"W": "W-window", "L": "L-launch", "E": "E-energy", "D": "D-drive", "B": "B-biology",
         "M": "M-motive", "R": "R-regime", "C": "C-contact"}
KEYS = ["baseline", "moderate", "strong", "radical", "open"]


def load(name: str) -> dict:
    with open(ROOT / "data" / f"{name}.toml", "rb") as f:
        return tomllib.load(f)


def clean(s: str) -> str:
    return " ".join(str(s).split())


def render_node(n: dict) -> str:
    out = [f"### {n['name']}", f"Id: `{n['id']}`. Factor {n['factor']}. Horizon: {n['horizon']}. Status: {n['status']}."]
    out.append(f"What it is: {clean(n.get('description', ''))}")
    out.append(f"Resolves when: {clean(n['resolution'])}")
    out.append(f"Source of truth: {clean(n.get('source', ''))}")
    deps = n.get("depends_on") or []
    anys = n.get("depends_on_any") or []
    if deps:
        out.append("Depends on: " + ", ".join(f"`{d}`" for d in deps))
    for g in anys:
        out.append("Depends on any one of: " + ", ".join(f"`{d}`" for d in g))
    if not deps and not anys:
        out.append("Depends on: nothing (a root of its own).")
    if n.get("long_shot"):
        out.append(f"Long shot. Mechanism: {clean(n['mechanism'])}")
        out.append(f"Breaking point: {clean(n['breaking_point'])}")
    if n["status"].startswith("resolved"):
        out.append(f"Resolved {n.get('resolved_on')}: {clean(n.get('resolved_by', ''))}")
    elif "probability" in n:
        p = n["probability"]
        out.append("Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): "
                   + " / ".join(f"{p[k]:.2f}" for k in KEYS) + f"  (estimated {n.get('estimated_on')})")
        out.append(f"Rationale: {clean(n.get('rationale', ''))}")
    if n.get("notes"):
        out.append(f"Notes: {clean(n['notes'])}")
    return "\n".join(out) + "\n"


def render_context() -> str:
    sc = load("scenarios")["scenario"]
    ti = load("tiers")
    out = ["## The five scenarios (when the window closes)"]
    for s in sc:
        yr = s.get("window_year", "no deadline")
        out.append(f"- {s['key']}: {s['name']}, {yr}")
    out.append("")
    out.append("## What each tier requires (every listed node, and any listed lower tier)")
    for t in ti["system_tier"] + ti["access_tier"]:
        out.append(f"- {t['key']} {t['name']}: {clean(t['definition'])} Requires: " + ", ".join(f"`{r}`" for r in t["requires"]))
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args(argv)
    brief = (ROOT / "docs" / "reviews" / "brief.md").read_text().split("---", 1)[1].strip()
    outdir = ROOT / "docs" / "reviews" / "packets"
    outdir.mkdir(parents=True, exist_ok=True)
    ctx = render_context()
    for packet, factors in PACKETS.items():
        parts = [f"# Review packet: {packet} ({a.date})", "", brief, "", "## The nodes", ""]
        count = 0
        for f in factors:
            nodes = load(FILES[f])["node"]
            parts.append(f"## Factor {f}: {FACTOR_NAMES[f]} ({len(nodes)} nodes)\n")
            for n in nodes:
                parts.append(render_node(n)); count += 1
        parts.append(ctx)
        text = "\n".join(parts)
        path = outdir / f"{a.date}-{packet}.md"
        path.write_text(text)
        print(f"{path.relative_to(ROOT)}: {count} nodes, {len(text.split())} words")
    return 0


if __name__ == "__main__":
    sys.exit(main())
