# The Ledger: tracking what moves the needle, and how the number moves with it

Drafted 2026-09-19 in a Cowork session, awaiting John's ruling on the decisions at the end. This is the plan for the feature John named as one of the site's most important: documenting the things that move the needle as they happen, and showing how the headline number changes as they are documented. It sits on top of the tree, the compute script, and the site as they stand on 2026-09-19 (roadmap steps 1 to 13, 20, 21, and 27 in progress), and it is written so that a Claude Code session can build against it. Steps are numbered 28 onward so they never collide with the roadmap (1 to 19 and 27) or the website plan (20 to 26).

Nothing here changes a probability, a criterion, or a definition. It adds a record of changes, the numbers derived from that record, and the pages that show them.

## The idea in one paragraph

Because the headline number is computed from the tree, every event that matters has the same shape: something happened in the world, one or more nodes changed, the tree was re-run, and the headline moved. So the unit of this feature is a ledger entry, not a blog post. Each entry says, in one plain sentence, what happened; which link of the chain it touched; what that node's number was before and after; and what the headline was before and after. The delta is the headline of the entry. A reader who skims only the deltas still follows the story. Two things make the ledger more than a changelog. First, attribution: the tree can be re-run with and without any single change, so each entry carries a computed answer to "how much did this one thing matter", and those answers rank into the year's biggest movers. Second, the forward half: for every open node the script can compute what the headline would be if that node resolved tomorrow, which gives each link of the chain a watch list of the milestones that would actually move it, with the expected delta stated before the event rather than after. When the milestone lands, the entry links back to the prediction.

## What the reader sees

Six surfaces, in the order a first-time reader meets them.

**Arrows on the home page chain.** Each of the seven links already shows the rate at which its gate nodes hold. Add a small arrow and delta beside each link, "since the last run" (up 3 points, down 1, steady), and one beside the headline number under the year dial. This is the cheapest surface and the one most people will see.

**The Ledger page.** A reverse-chronological list of entries, replacing the changelog as the main content of "The story so far" (the raw changelog stays, rendered below the ledger as the full record, and the TimeAssembler worklog planned at website step 24 sits beside it). Each entry is a card: the date, a kind tag, the chain link it touched, the one-sentence title, and the delta badge (headline before, arrow, headline after, under the scenario the dial is set to). Expanding the card shows what happened, the source, each node that changed with its before and after, the computed contribution of the entry to the headline, and a link to the run note it landed in. Filters by kind and by link.

**The headline's history.** A line chart at the top of the Ledger page: the headline (A2, the tier at which John works off Earth on rotation) over calendar time, one line per longevity scenario or the dial's scenario alone, with a marker at each entry. Clicking a marker opens the entry. The same chart, for the factor's own gate rate, sits at the top of each factor page. Both are drawn from the committed snapshots described below, so the history on the site is exactly the history in the repository.

**Movers.** A ranking on the Ledger page, per calendar year: the entries with the largest computed contribution, up or down, and the link that gained or lost the most. Below it, in the same table, the entries that changed nothing. Those "held steady" entries matter as much as the movers: when a widely reported event does not touch any node's criterion, the ledger says so and says why. This is the ledger's credibility engine and probably its most shareable content, because it cuts against the news cycle instead of riding it.

**Watch lists.** On each factor page, under the nodes, a short list titled "What would move this": the open nodes in that link ranked by worth, where worth is the computed change in the headline if the node resolved yes now, shown alongside the change if it resolved no. Each node page carries its own worth line ("If this happened tomorrow, the headline by 2071 moves from 0.9 to 1.4 percent"). This is pre-registration without the ceremony: the site says in advance what each milestone is worth, and the entry that later records the milestone quotes the prediction.

**Run notes and the feed.** Every quarterly scan and annual review already ends in a run (roadmap steps 17 and 18). Its run note, in docs/runs/, becomes a rendered page: what changed, what did not, and the calibration score to date. Off the site, a JSON Feed and RSS feed of entries, and a badge image at a fixed address that reads "Belt Equation: 0.9% by 2071, up 0.3 since 2026-09-19", so the number can live in a README, a profile, or the Sentient Horizons sidebar.

## The two rules that keep it honest

**The world moving is not the same as John changing his mind.** Every entry has a kind, and the totals are reported per kind. A reader who sees the headline climb can tell at once whether the world got closer (events, resolutions) or the forecaster got more optimistic (revisions from reviews and reconsideration), and structural changes to the tree are flagged so that numbers across them are not read as apples to apples. The six kinds:

| kind | meaning | example |
|---|---|---|
| `event` | Something happened in the world and a node's probability moved because of it. Cites a public source. | A launcher's hundredth orbital flight of the year brings the launch-price node up. |
| `resolution` | A node resolved yes or no. A special event; it feeds the calibration score. | The first participant is dosed in a partial-reprogramming trial (already on the record, 2026-06-09). |
| `revision` | A probability or rationale changed with no new event: an outside-model review, a reconsideration, a correction. | Step 27 review moves kilowatt power beaming to 0.30 by 2071. |
| `structure` | The tree changed shape: a node added, cut, superseded, or rewired; a tier requirement moved; a criterion reworded. Breaks comparability and says so. | The child-born-off-Earth requirement moved from Tier 2 to Tier 4, 2026-09-19. |
| `decision` | John took or changed a choice point, or the current plan at a fork changed. Carries the decision comparison's before-and-after. | A choice at the six-year fork, some years from now. |
| `held-steady` | Something widely reported happened and no node moved. Names the nodes it was checked against and says why none resolved or changed. | A crewed lunar landing announcement that is a target date, not a landing. |

**Entries are appended, never edited.** A mistake in an entry is fixed by a later entry that says so and points back. Numbers on an entry are computed by the export script from the snapshots and the node records, never typed by hand, so an entry cannot claim a delta the tree did not produce.

## The record

### Ledger entries: `data/ledger.toml`

One `[[entry]]` table per entry, newest last, same TOML rules as the node files. The export script validates the file and refuses to build if any rule below fails.

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | `YYYY-MM-DD-slug`, unique, never changed. |
| `date` | yes | The date the entry was written to the ledger (absolute, YYYY-MM-DD). |
| `occurred_on` | events, resolutions | The date the thing happened in the world, when that differs from `date`. |
| `kind` | yes | One of the six kinds above. |
| `title` | yes | One plain sentence, readable by someone outside the project, in the chain's vocabulary (link names, not factor letters). |
| `body` | yes | Two to five sentences: what happened, why it touches the tree the way it does. For `held-steady`, why nothing moved. |
| `source` | events, resolutions, held-steady | The public record that settles what happened: a link or citation. |
| `nodes` | all but held-steady | List of node ids the entry changed. Each id must carry a `revisions` entry (or a `resolved_on`) dated on or before `date` and after the previous snapshot; that is how the ledger and the node records are kept from drifting. |
| `checked_against` | held-steady | Node ids whose criteria the event was read against. |
| `watch_ref` | no | The node id whose watch-list worth this entry fulfils, when a listed milestone landed. The export copies the worth that was on the record at the previous snapshot into the entry, so the prediction and the outcome sit together. |
| `snapshot` | yes | The snapshot key (below) this entry landed in. Several entries share a snapshot when a scan changes several nodes and runs once. |
| `run_note` | no | Path under docs/runs/ of the run note that discusses it. |
| `corrects` | no | Id of an earlier entry this one corrects. |

Derived at export time and never stored: the factors and chain links touched (from the nodes), each node's before and after (from the two snapshots), the headline before and after per scenario, and the entry's contribution (below).

### Snapshots: `data/snapshots/YYYY-MM-DD[-label].json`

A snapshot is the complete output of one run, written by the compute script and committed: run parameters (runs, seed, world spread, git commit), every tier's rate per scenario, every node's rate per scenario, the chain's gate rates, the Contact Clause rungs, the decision comparison, and every open node's worth. Snapshots are the ledger's memory; the history chart is drawn from nothing else. A snapshot is taken at every quarterly scan, every annual review, and whenever a ruling changes the tree between scans. The key is the file name without extension.

Two backfilled snapshots exist in prose already and should be written as JSON first: `2026-09-19-first-run` (from docs/runs/2026-09-19-first-run.md, before the four structural fixes) and `2026-09-19-second-run` (the numbers now in tree.json). Both carry `review_status = "pre-review"` until step 27 lands, and the site shows that label on them.

### Node worth, computed

For each open world node, the compute script forces the node to yes and re-runs, then forces it to no and re-runs, and records the headline under each scenario for both, alongside the headline as it stands. Worth-if-yes is the first minus the baseline; worth-if-no is the second minus the baseline. Both are stored in the snapshot. Sixty nodes times two forced runs times five scenarios at 20,000 runs each is about 12 million node samples per snapshot, well under a minute in plain Python and taken once per scan. Choice nodes are already covered by the decision comparison and are not given a worth.

### Entry contribution, computed

An entry's contribution is a leave-one-out figure: take the tree as it stands at the entry's snapshot, revert only the changes the entry lists (using `old` from the node revisions, or un-resolving the node), re-run, and report the headline with the entry undone minus the headline with it in. When several entries share a snapshot, their contributions do not sum exactly to the snapshot's total change, because changes interact; the export reports the residual as its own line ("interaction: +0.1"). Structural entries that add or remove nodes are attributed by rebuilding the tree without the change where that is well defined, and otherwise carry the whole snapshot delta with a note that it cannot be separated.

## Decisions, with confidence and alternatives

Per the ground rule of 2026-09-08. Proposed by Claude, awaiting John.

1. **A separate ledger file with hand-written entries, and every number on an entry derived by the export script.** High confidence. Judgment call on the shape; standard practice on the principle that narrative is typed and figures are computed. Alternative: derive entries entirely from the node `revisions` fields and git history, with no new file. It needs no upkeep, but it cannot hold a held-steady entry, a source, or a sentence of narrative, and reading history out of git inside the export is fragile. The cross-check rule (every entry's nodes must carry a matching revision) keeps the two records from drifting, which was the real risk of a second file.

2. **Committed JSON snapshots per run as the source of all history.** High confidence; standard practice (freezing model outputs per release). Alternative: recompute the history at export time by checking out each past commit and running the tree. Slow, breaks whenever the schema or the script changes, and depends on git in the build. Cost of snapshots: a 100 to 200 KB file per scan, a few dozen a decade.

3. **Leave-one-out contribution with the interaction residual reported.** Moderate confidence; a judgment call. Alternative: order-dependent sequential attribution (apply changes one at a time in ledger order), which sums exactly but makes the same change worth different amounts depending on where it sits in the scan. Shapley values would be the principled answer and are exponential in the number of changes; not worth it for a page a family reads. Leave-one-out plus a stated residual is the honest cheap version.

4. **Node worth computed by forcing, shown on node pages and as the factor watch lists.** High confidence; standard practice (one-at-a-time sensitivity analysis). Alternative: hand-written watch lists with guessed deltas, which is what most forecasting write-ups do and which drift from the tree the moment a number changes. Cost: the extra compute at each snapshot, and a `worth` command in compute.py.

5. **Six kinds of entry, with totals reported per kind.** Moderate confidence. Alternative: two kinds, world versus mind, which is the distinction that matters most. Six was chosen because resolutions feed the calibration score, structural changes break comparability, decisions are the project's stated purpose, and held-steady entries have no home in a two-kind scheme. Collapse to fewer kinds if the ledger reads as over-labelled after a year.

6. **The ledger replaces the changelog as the main content of "The story so far".** Moderate confidence. Alternative: a new page beside the story page. One page fewer to explain, and the story page's promise ("one place to see what has changed and why") is exactly the ledger's. The changelog stays rendered below as the raw record, and remains the place where every commit-level change is written; the ledger is the subset that moved or notably failed to move the numbers.

7. **Charts as inline SVG generated at build time from the snapshots, no chart library.** Moderate confidence. Alternative: a client-side chart library, which gives hover and zoom for free at the cost of a dependency and a look the sister sites do not share. Version one has at most a handful of points per line; build-time SVG in the site's own styles is enough, and the markers link to entries by plain anchors. Revisit alongside the interactive tree (deferred, website plan).

8. **JSON Feed, RSS, and a badge SVG, written by the export script.** High confidence on feeds (standard, cheap, no service). Moderate on the badge. Alternative: nothing off the site until the posture changes at roadmap step 16. The feeds are static files and do not count as promotion; the badge exists so that the number can appear in the repo README and on Sentient Horizons. A newsletter stays deferred.

## Steps

Each names what it waits on. Targets assume the ledger goes live with the family-and-friends announcement (website step 25's remaining half, target 2026-11-16) and no earlier, so the first public history starts with reviewed numbers.

28. **Snapshots** (waits on nothing; can start now). `compute.py run --snapshot [label]` writes `data/snapshots/YYYY-MM-DD[-label].json` with everything listed under "Snapshots". Backfill `2026-09-19-first-run` and `2026-09-19-second-run`, marked pre-review. The export script reads the snapshot folder and puts the series into the site's JSON. Done when the two backfilled snapshots exist and `export.py --check` counts them.

29. **Node worth and entry contribution** (waits on 28). `compute.py worth` (every open world node forced yes and no, per scenario) and `compute.py attribute <entry-id>` (leave-one-out against the entry's snapshot). Both feed the snapshot. Done when the worth table for the current tree is in a snapshot and the two regime-gate rulings of 2026-09-19 have attributed contributions.

30. **The ledger file** (waits on 28; entries for step 27 land as its rulings land). `data/ledger.toml` per the record above, validated by the export script with the cross-check against node revisions. Backfill the 2026-09-19 entries: the two regime-gate rewordings (`structure`), the child-born tier move (`structure`), the world draw (`structure`), the three nodes already resolved (`resolution`, with `occurred_on`), and one `revision` entry per ruled step-27 disagreement as John rules them. Done when every 2026-09-19 changelog line that changed a number or the tree has an entry, and the export validates.

31. **The Ledger page and the history charts** (waits on 29, 30; target 2026-11-09, alongside website step 24). The story page rebuilt around the ledger: chart at the top, entry cards with filters, movers table, changelog below. Factor pages get their gate-rate history. Home page chain gets the since-last-run arrows. Done when clicking a chart marker opens its entry and the arrows match the difference between the last two snapshots.

32. **Watch lists and worth lines** (waits on 29; target 2026-11-09). "What would move this" on each factor page; the worth sentence on each node page; `watch_ref` fulfilment shown on entries. Done when every open world node page states its worth under the dial's scenario.

33. **Feeds, badge, and the scan procedure** (waits on 31; target 2026-11-16, then ongoing). `feed.json`, `rss.xml`, and `badge.svg` written by the export. Roadmap step 17's quarterly scan rewritten as a procedure: read each leaf against its criterion, write entries (including held-steady ones for anything widely reported that did not move), run with a snapshot, write the run note, publish with the one-command script from website step 26. Done when one quarterly scan has gone from leaf check to live site through this procedure.

## Deferred, and why

- **Reader-submitted "did this move anything?" questions.** Critique already goes through GitHub issues (website plan, decision 8); a question about whether an event moved a node can be an issue with a label, and its answer a held-steady or event entry that cites the issue. No new machinery until the posture changes at roadmap step 16.
- **Per-scenario history for every node** on the site. The snapshots hold it; the pages show the headline and the gate rates in version one. Node-level history charts follow when node pages become the place people argue.
- **Attribution across structural changes** beyond the simple cases. Version one reports the whole delta with a note; a rebuild-based method waits until a structural change actually needs separating.
- **Anything from the health record.** Window changes appear in the ledger only as a scenario year moving in `scenarios.toml`, exactly as the ground rule allows, with the entry's body saying no more than definitions.md already does.
