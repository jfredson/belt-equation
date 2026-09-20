#!/usr/bin/env python3
"""Draw the tree as one picture (roadmap step 13): every node, coloured by factor, with its numbers.

    python3 scripts/visual.py                      write docs/visual/<date>-tree.svg
    python3 scripts/visual.py --out path.svg       write somewhere else (the site copies it at step 22)

Standard library only. Reads data/ through the compute script's loader so a tree that fails the
schema draws nothing. Layout: three columns by horizon (leaf, mid, root), rows grouped by factor
in the equation's order, edges drawn from each dependency to the node that needs it. Choice
points have a dashed outline; resolved nodes are filled. The numbers on a node are its recorded
probabilities (conditional on its dependencies) for 2071, 2095 and no deadline; the tier box at
the top carries the computed headline from a fresh run.
"""
from __future__ import annotations
import argparse, datetime, random, sys
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compute  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FACTORS = ["W", "L", "E", "D", "B", "M", "R", "A", "C"]
NAMES = {"W": "Window", "L": "Launch", "E": "Energy", "D": "Drive", "B": "Biology",
         "M": "Motive", "R": "Regime", "A": "Access", "C": "Contact Clause"}
# Eight categorical hues in a validated order (dataviz reference palette, light surface);
# the Contact Clause sits beside the equation and takes a neutral.
COLOR = {"W": "#2a78d6", "L": "#eb6834", "E": "#1baf7a", "D": "#eda100", "B": "#e87ba4",
         "M": "#008300", "R": "#4a3aa7", "A": "#e34948", "C": "#6f6e69"}
HORIZONS = ["leaf", "mid", "root"]
HLABEL = {"leaf": "Leaves: could resolve within five years",
          "mid": "Mid: a decade or two", "root": "Roots: the far end"}

W, H = 400, 62          # node box
GAPX, GAPY = 140, 14    # between columns, between boxes
MARGIN_L, TOP = 40, 210
STRIPE = 8


def wrap(text: str, width: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    if len(lines) > 2:
        lines = [lines[0], (" ".join(lines[1:]))[:width - 1] + "…"]
    return lines


def render(tree: dict, results: dict, runs: int, today: str) -> str:
    """The whole tree as one SVG, as a string.

    `results` maps each scenario key to a dict with a "tiers" table (tier key to rate), which is
    what compute.simulate() returns and also what the export script already holds after its own
    run; passing it in means the picture and the site's numbers come from the same play-throughs.
    Split out of main() on 2026-09-20 (website step 22) so scripts/export.py can write the same
    picture to site/public/tree.svg on every build."""
    nodes = tree["nodes"]
    keys = [s["key"] for s in tree["scenarios"]]

    # positions: column by horizon, rows grouped by factor order
    cols = {h: [] for h in HORIZONS}
    for f in FACTORS:
        for n in nodes:
            if n["factor"] == f:
                cols[n["horizon"]].append(n)
    pos = {}
    col_x = {h: MARGIN_L + i * (W + GAPX) for i, h in enumerate(HORIZONS)}
    max_rows = 0
    for h in HORIZONS:
        y = TOP
        last_f = None
        for n in cols[h]:
            if last_f is not None and n["factor"] != last_f:
                y += GAPY  # a little extra between factor groups
            pos[n["id"]] = (col_x[h], y)
            y += H + GAPY
            last_f = n["factor"]
        max_rows = max(max_rows, y)
    width = MARGIN_L * 2 + 3 * W + 2 * GAPX + 60  # room for the loop-back edges on the right
    height = max_rows + 120

    res = results
    head = tree["tiers"]
    a2 = next(t for t in head if t["key"] == compute.HEADLINE_TIER)
    t3 = next(t for t in head if t["key"] == "T3")

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="Helvetica, Arial, sans-serif">')
    s.append('<style>.t{fill:#0b0b0b}.d{fill:#52514e}.m{fill:#8a8983}.small{font-size:11px}.num{font-size:12px;font-variant-numeric:tabular-nums}</style>')
    s.append(f'<rect width="{width}" height="{height}" fill="#fcfcfb"/>')
    # title block
    s.append(f'<text x="{MARGIN_L}" y="44" class="t" font-size="26" font-weight="700">The Belt Equation: the tree, {today}</text>')
    s.append(f'<text x="{MARGIN_L}" y="68" class="d" font-size="14">{len(nodes)} breakthroughs under eight factors, plus the Contact Clause beside the equation. Each box shows the chance the node resolves before 2071 / 2095 / ever, given what it depends on. Arrows run from a dependency to the node that needs it.</text>')
    s.append(f'<text x="{MARGIN_L}" y="86" class="d" font-size="14">Numbers reviewed by outside models (roadmap step 27, ruled 2026-09-19, landed 2026-09-20); they move at the weekly scan, the quarterly scan and the annual review.</text>')
    # headline box
    def pct(v): return f"{100*v:.1f}%" if v < 0.1 else f"{100*v:.0f}%"
    line1 = "  ·  ".join(f"{k} {pct(res[k]['tiers'][a2['key']])}" for k in keys)
    line2 = "  ·  ".join(f"{k} {pct(res[k]['tiers'][t3['key']])}" for k in keys)
    s.append(f'<rect x="{MARGIN_L}" y="102" width="{width - 2*MARGIN_L}" height="76" rx="6" fill="#f0efec"/>')
    s.append(f'<text x="{MARGIN_L+14}" y="126" class="t" font-size="14" font-weight="700">Headline, {a2["key"]} ({a2["name"].lower()}):  <tspan class="num" font-weight="400">{line1}</tspan></text>')
    s.append(f'<text x="{MARGIN_L+14}" y="148" class="t" font-size="14" font-weight="700">{t3["key"]} ({t3["name"]}, the bar for the Belt existing):  <tspan class="num" font-weight="400">{line2}</tspan></text>')
    s.append(f'<text x="{MARGIN_L+14}" y="168" class="m small">Scenarios are the year the window closes: baseline 2071, moderate 2080, strong 2095, radical 2136, open = no deadline. Computed from {runs:,} play-throughs per scenario with the world draw at its default spread.</text>')
    # column headers
    for h in HORIZONS:
        s.append(f'<text x="{col_x[h]}" y="{TOP-12}" class="d" font-size="13" font-weight="700">{HLABEL[h]}</text>')
    # legend
    lx = MARGIN_L
    for f in FACTORS:
        s.append(f'<rect x="{lx}" y="{height-40}" width="14" height="14" rx="2" fill="{COLOR[f]}"/>')
        s.append(f'<text x="{lx+20}" y="{height-28}" class="d" font-size="12">{f}: {NAMES[f]}</text>')
        lx += 30 + 8 * len(NAMES[f]) + 24
    s.append(f'<text x="{lx+10}" y="{height-28}" class="m" font-size="12">Dashed outline: a choice John makes, never rolled.  Filled: already resolved.</text>')
    # edges first, under the boxes
    s.append('<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#b5b4ae"/></marker></defs>')
    for n in nodes:
        deps = list(n.get("depends_on") or []) + [d for g in (n.get("depends_on_any") or []) for d in g]
        for d in deps:
            if d not in pos: continue
            x1, y1 = pos[d]; x2, y2 = pos[n["id"]]
            sx, sy = x1 + W, y1 + H/2
            ex, ey = x2, y2 + H/2
            if x2 <= x1:  # same column or backwards: route around the right side
                sx = x1 + W; ex = x2 + W
                cx = max(sx, ex) + 40
                s.append(f'<path d="M{sx},{sy} C{cx},{sy} {cx},{ey} {ex},{ey}" fill="none" stroke="#c9c8c2" stroke-width="1.2" marker-end="url(#ar)"/>')
            else:
                mx = (sx + ex) / 2
                s.append(f'<path d="M{sx},{sy} C{mx},{sy} {mx},{ey} {ex},{ey}" fill="none" stroke="#c9c8c2" stroke-width="1.2" marker-end="url(#ar)"/>')
    # boxes
    for n in nodes:
        x, y = pos[n["id"]]
        c = COLOR[n["factor"]]
        resolved = n["status"].startswith("resolved")
        choice = n["kind"] == "choice"
        fill = c if resolved else "#ffffff"
        dash = ' stroke-dasharray="5,3"' if choice else ""
        s.append(f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="5" fill="{fill}" fill-opacity="{0.18 if resolved else 1}" stroke="{c}" stroke-width="1.5"{dash}/>')
        s.append(f'<rect x="{x}" y="{y}" width="{STRIPE}" height="{H}" rx="3" fill="{c}"/>')
        s.append(f'<text x="{x+STRIPE+8}" y="{y+16}" class="m small" font-weight="700">{n["factor"]}</text>')
        lines = wrap(n["name"], 58)
        for i, ln in enumerate(lines):
            s.append(f'<text x="{x+STRIPE+26}" y="{y+16+i*15}" class="t" font-size="12.5">{escape(ln)}</text>')
        if resolved:
            tail = f"resolved {n.get('resolved_on', '')}"
        elif choice:
            tail = "choice point" + (", current plan" if n.get("current_plan") else "")
        elif "probability" in n:
            p = n["probability"]
            tail = f"2071 {p['baseline']:.2f}   ·   2095 {p['strong']:.2f}   ·   ever {p['open']:.2f}"
            if n.get("long_shot"): tail += "   ·   long shot"
        else:
            tail = "no number yet"
        s.append(f'<text x="{x+STRIPE+26}" y="{y+H-10}" class="d num">{escape(tail)}</text>')
    s.append('</svg>')
    return "\n".join(s)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--runs", type=int, default=20000)
    a = ap.parse_args(argv)
    today = datetime.date.today().isoformat()
    out = a.out or ROOT / "docs" / "visual" / f"{today}-tree.svg"
    tree = compute.load_tree(ROOT / "data")
    problems = compute.validate(tree)
    if problems:
        print("tree fails the schema; nothing drawn:\n  " + "\n  ".join(problems)); return 1
    keys = [s["key"] for s in tree["scenarios"]]
    rng = random.Random(2026)
    results = {k: compute.simulate(tree, k, a.runs, rng) for k in keys}
    svg = render(tree, results, a.runs, today)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg)
    shown = out.relative_to(ROOT) if out.is_relative_to(ROOT) else out
    print(f"wrote {shown}: {len(tree['nodes'])} nodes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
