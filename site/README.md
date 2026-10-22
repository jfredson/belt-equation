# The website

The public face of the tree: beltequation.com (attached at website step 25; until then the site lives at its workers.dev preview address). Plan and decisions: docs/website-plan.md. Scaffolded 2026-09-19 (website step 20) with the node pages (website step 21).

## How it fits together

    data/*.toml  ──┐
    CHANGELOG.md ──┤  scripts/export.py  ──►  site/src/data/*.json  ──►  astro build  ──►  dist/  ──►  wrangler deploy
    data/headline.json ─┘                 ──►  site/public/data/headline.json ─┘

- **Python owns the data.** `scripts/export.py` reads the tree with the same loader and validator as `scripts/compute.py`, so the site can never show a tree that fails the schema. It writes `src/data/tree.json` and `src/data/changelog.json`. Those files are generated, not committed: every `npm run build` and `npm run dev` runs the export first (`prebuild`, `predev`), so the site always reflects the tree in `data/`.
- **The headline file is served from the site.** Since 2026-10-17 the export also copies `data/headline.json` (the small file the family's Projects page reads; what is in it: data/README.md) to `public/data/headline.json`, byte for byte, so the built site serves it at https://beltequation.com/data/headline.json as well as the repository serving it from `main`. Ruled by John 2026-10-17, from the first cross-project lessons review (sentient-horizons/design/reviews/2026-10-17-lessons-review.md, section 9): every tracker serves its headline file from its own site. The copy is generated like the tree picture, not committed (`public/data/` is in .gitignore); `scripts/test_headline.py` checks that the copy is the file.
- **Astro owns the pages.** Astro 5, fully static, same generator and folder layout as the Sentient Horizons and Hearth and Void sites. `src/lib/tree.ts` is the typed view of the JSON; every page reads from it.
- **The styles are the family's skeleton with this site's own skin.** From 2026-09-19 to 2026-10-17 the stylesheet was the Deep Field look copied from Sentient Horizons (website-plan decision 7), and the whole family copied it from here. Since 2026-10-17 `src/styles/skin.css` is the "Ore" skin (a blue-black sky with the belt across it, a Belter rust, a steel blue for data; ruled by John 2026-10-17), and `src/styles/global.css` imports it, then carries `sentient-horizons/design/shell.css` copied unchanged (version noted at the marked line), then this site's own rules.

## Pages

| Path | What it shows |
|---|---|
| `/` | The number first: the headline probability under a year dial (the five longevity scenarios), then the chain of seven plain-English links, one per factor, each with the rate at which its gate nodes all hold (`numbers.chain` in the export), then who is asking and how to argue. Redesigned 2026-09-19 for readers who have never heard of the project; the letter equation stays as one line under the chain. |
| `/tree/` | The factors, and the system and access tiers with what each requires. |
| `/tree/<factor>/` | One page per factor listing its nodes, leaves first. |
| `/tree/<factor>/<node-id>/` | One page per node: description, resolution criterion, source, horizon, dependencies, what needs it, probability by scenario with rationale and date, long-shot mechanism and breaking point, revisions, notes, and a link to open an issue about it. |
| `/method/` | How the numbers are computed, in plain language and results only: play-throughs, the five deadlines, the world draw, what is reported, scoring, the Contact Clause. From 2026-09-20 to 2026-10-12 it also rendered docs/methodology.md in full; that document is now linked from the page instead, since its dated record of who settled what read oddly to a first-time visitor. |
| `/story/` | What moved the headline number and by how much: the ledger of entries, the biggest movers, and the run-by-run table, all from the committed runs. The roadmap, the day-by-day workbench and the rendered changelog were on this page from 2026-09-20 to 2026-10-12 and were taken off as process rather than results; the changelog is linked from the repository. |
| `/missions/` | The space missions John follows on the way out, whether or not they move the number (added 2026-10-21, tracker pattern rule 4.20): a coming-up list, the timeline (`src/components/MissionTimeline.astro`, years across on a computer, a list by year on a phone), a table and CSV of every milestone, and one entry per mission, all from `data/missions.toml` through `src/data/missions.json`. |
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
