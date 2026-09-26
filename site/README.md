# The website

The public face of the tree: beltequation.com (attached at website step 25; until then the site lives at its workers.dev preview address). Plan and decisions: docs/website-plan.md. Scaffolded 2026-09-19 (website step 20) with the node pages (website step 21).

## How it fits together

    data/*.toml  ──┐
    CHANGELOG.md ──┤  scripts/export.py  ──►  site/src/data/*.json  ──►  astro build  ──►  dist/  ──►  wrangler deploy

- **Python owns the data.** `scripts/export.py` reads the tree with the same loader and validator as `scripts/compute.py`, so the site can never show a tree that fails the schema. It writes `src/data/tree.json` and `src/data/changelog.json`. Those files are generated, not committed: every `npm run build` and `npm run dev` runs the export first (`prebuild`, `predev`), so the site always reflects the tree in `data/`.
- **Astro owns the pages.** Astro 5, fully static, same generator and folder layout as the Sentient Horizons and Hearth and Void sites. `src/lib/tree.ts` is the typed view of the JSON; every page reads from it.
- **The styles are copied** from Sentient Horizons' design system (website-plan decision 7): same colour tokens, typography, nav, and light/dark toggle, so the three sites read as one family.

## Pages

| Path | What it shows |
|---|---|
| `/` | The number first: the headline probability under a year dial (the five longevity scenarios), then the chain of seven plain-English links, one per factor, each with the rate at which its gate nodes all hold (`numbers.chain` in the export), then who is asking and how to argue. Redesigned 2026-09-19 for readers who have never heard of the project; the letter equation stays as one line under the chain. |
| `/tree/` | The factors, and the system and access tiers with what each requires. |
| `/tree/<factor>/` | One page per factor listing its nodes, leaves first. |
| `/tree/<factor>/<node-id>/` | One page per node: description, resolution criterion, source, horizon, dependencies, what needs it, probability by scenario with rationale and date, long-shot mechanism and breaking point, revisions, notes, and a link to open an issue about it. |
| `/method/` | How the numbers are computed, the scenario table, the Contact Clause. The full methodology document joins at website step 23. |
| `/story/` | The changelog, rendered. TimeAssembler's progress feed joins at website step 24. |
| `/disagree/` | How to name a missing node, challenge a criterion, or move a number, and what happens to critique. |

Node ids are the URL keys because the schema promises they are never renamed once a probability has been recorded.

## Commands

Run from `site/`. Needs Node (the Mac has 26) and Python 3.11 or later for the export.

    npm install          once
    npm run export       write the JSON from ../data without building
    npm run dev          local preview with live reload (runs the export first)
    npm run build        static build to dist/ (runs the export first)
    npm run preview      serve dist/ locally
    npm run deploy       build, then `wrangler deploy` to Cloudflare Workers static assets

The ordinary way to publish is not `npm run deploy` but `python3 scripts/publish.py --push` from the repository root (website step 26, 2026-09-25): it regenerates and builds everything, shows what changed, and pushes main, and the GitHub Action (.github/workflows/deploy.yml, since 2026-09-19) builds and deploys from that push. `npm run deploy` stays for a deploy from this Mac by hand. Deploying by hand needs a Cloudflare login on this Mac (`npx wrangler login`, which expires now and then and has to be repeated). The Worker is named `beltequation` and the preview address is https://beltequation.jfredson.workers.dev (first deployed 2026-09-19). The custom domain is attached at website step 25, not before.
