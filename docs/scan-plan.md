# The Radar: a weekly web scan that keeps the tree current

Drafted 2026-09-19 in a Cowork session and ruled the same day. John's rulings, in order: the ledger plan's eight decisions (docs/ledger-plan.md) accepted as proposed; the scan runs as a Cowork scheduled task; it runs weekly; and it may change numbers and resolve nodes itself, with John reviewing after the fact rather than before. The cap on how far it may move a number in one scan (decision 3 below) is Claude's addition to that ruling and stands unless John strikes it.

This plan sits on top of the ledger plan. The ledger is the record of what moved the needle; the Radar is the process that goes looking, every week, for things that should. Steps are numbered 34 to 38 so they never collide with the roadmap (1 to 19 and 27), the website plan (20 to 26), or the ledger plan (28 to 33).

## The idea in one paragraph

Every open world node already carries a criterion that says exactly what would count as it having happened, and a source that says who settles it. Once a week a fresh Claude session reads those criteria, searches the web for what happened in the past week against each one, and writes a scan record: for each node, what it searched, what it found, and a verdict. Where something moved, it edits the node (a new probability with a revision logged, or a resolution with the record that settled it), appends a ledger entry, re-runs the tree with a snapshot, and commits to main; a deploy workflow rebuilds the site from the commit. The Radar page on the site shows every scan and every verdict, so the site changes every week whether or not the headline does, and a reader can see the tree being watched rather than take it on faith.

## What the scanner may and may not do

John ruled that the scanner edits the tree itself. These limits keep an after-the-fact review cheap and a bad week reversible.

It may change the probability of an open world node in factors W, L, E, D, B, M, R and C, by at most 0.10 in absolute terms per scenario per scan, and only with a public source that bears on the criterion. It may resolve a node yes when the criterion is met on the plain reading and two independent public records agree, recording `resolved_on` and `resolved_by`. It may write ledger entries of kind `event`, `resolution` and `held-steady`.

It may not edit a criterion, a source, a description, a name, a mechanism or a breaking point; add, cut, supersede or rewire a node; touch tiers.toml, scenarios.toml, definitions.md or methodology.md; resolve a node no (that happens at the annual review, when a window has passed); touch the A branch at all (provisional until May 2027, and partly personal); or move a number by more than the cap. Anything it wants to do outside those limits it writes up as a `flagged` item in the scan record with the move it would have made, and John rules on it.

Every scanner edit is marked as the scanner's. A revision on a node gets `why` beginning `[scan YYYY-MM-DD]`; a ledger entry carries `author = "scan"` (a new optional field on the ledger record; absent means John). The site reports the totals per author beside the totals per kind, so a reader can tell world from mind from machine. John's after-the-fact overrides are ordinary `revision` entries with `corrects` pointing at the scanner's entry; entries are never edited, exactly as the ledger plan says.

## Load: which nodes get checked when

Leaf nodes (could resolve within one to five years) are checked every scan. Mid and root nodes are checked on the first scan of each calendar month. With sixty nodes, a third of them leaves, and the A branch skipped, a typical week reads about twenty criteria and a first-of-month scan reads about fifty, at two to four searches each.

## The scan record: `data/scans/YYYY-MM-DD.toml`

One file per scan, appended to the folder and never edited. The export script validates every file and refuses to build if one fails.

    [scan]
    date = 2026-09-27              # Pacific date of the run
    ran_at = 2026-09-28T01:04:00Z  # UTC timestamp
    scope = "weekly"               # "weekly" (leaves) or "monthly" (all)
    nodes_checked = 21
    searches = 58
    commit_before = "cdc4c9f"      # the tree the scan read

    [[item]]
    node = "L-fully-reusable-heavy-launcher-recovers-both-stages"
    verdict = "quiet"              # see the five verdicts
    queries = ["...", "..."]       # at least one, except as noted below
    found = "One to three sentences on what the past week held, read against the criterion."
    sources = ["https://..."]      # required for every verdict but quiet
    ledger = "2026-09-27-ship-caught"   # the ledger entry id, for moved and resolved
    for_john = "..."               # required for flagged: the move it would have made and why

Every item names at least one search it ran, with one exception: a node that resolves only when one of the nodes it depends on resolves has nothing of its own to look for, so it may leave `queries` empty as long as its verdict is `quiet` and `found` says why no search was run. Every other verdict still needs a search.

Five verdicts. `quiet`: nothing found that bears on the criterion. `noted`: something relevant happened and no number moved; `found` says why not. When the thing was widely reported, the scanner also writes a `held-steady` ledger entry that names the criterion it was read against. `moved`: the probability changed within the cap; a revision on the node and an `event` ledger entry. `resolved`: the criterion was met; `resolved_on`, `resolved_by` on the node and a `resolution` entry. `flagged`: something the scanner may not do on its own; a `for_john` line and no edit.

## What the reader sees

**The Radar page** (`/radar`). The latest scan at the top: date, scope, nodes checked, and a count per verdict. Below it the items grouped by chain link (the home page's seven plain-English links), each a card with the node name, the verdict as a badge, the `found` sentence, and the sources; a `moved` or `resolved` card links to its ledger entry. Older scans follow, collapsed. A "Waiting on John" list of every open `flagged` item, cleared when a later ledger entry or scan item cites it.

**A strip on the home page**, under the headline number: "Last checked 2026-09-27: 21 nodes read, none moved" (or "one moved: the ship came back", linking to the entry). This is how a first-time visitor learns the number is watched.

**On each node page**, above the revisions: its last three scan items, "2026-09-27: quiet", with the found sentence on hover or expansion.

**In the ledger**, entries with `author = "scan"` carry a small mark, and the movers table reports scanner-made and John-made totals separately.

## Decisions, with confidence and alternatives

Per the ground rule of 2026-09-08. The first two were ruled by John on 2026-09-19; the rest were proposed by Claude and stand unless struck.

1. **A Cowork scheduled task, cloning the repository in the cloud and pushing to main.** Ruled. Alternatives: a GitHub Action with a search API and a model API (two keys, a small monthly bill, and a script to maintain), or Claude Code on the Mac under launchd (the Mac must be awake on Sunday evenings, and the scan would share a working tree with whatever else is going on). The task is a Claude Code routine (claude.ai/code/routines) with the repository attached; pushing needs the Claude GitHub App installed on the repository, John's action (step 35). A refused push to main falls back to a `claude/scan-YYYY-MM-DD` branch for John to merge. Dress rehearsal 2026-09-19: 44 nodes read, 84 searches, nothing moved, one flagged (C1), push refused for want of the app.

2. **Weekly, Sunday 18:00 Pacific, leaves every week and the whole tree on the first scan of the month.** Ruled weekly; the leaf/monthly split is Claude's. Alternatives: daily (more noise, and a scan that finds nothing forty times in a row teaches nothing), fortnightly (slower to catch a resolution), or every node every week (about a hundred and fifty searches a run for numbers that are mostly about 2050).

3. **Bounded autonomy: a 0.10 cap per scenario per scan, no structural or textual edits, no resolve-no, no A branch.** Moderate confidence; John ruled for autonomy, the bounds are Claude's. Alternative: propose-only, where every scan is a pull request John merges. Rejected by John on 2026-09-19 as a gate that does not earn its place: the ledger is append-only and every scanner edit is marked, so a mistake costs one correcting entry, not a review of every week. The cap exists so that one over-read headline cannot swing the tree by more than a review would, and it is the first thing to revisit at step 38.

4. **Queries composed at scan time from the node's name, criterion and source, with an optional `watch` list on the node for hand-added terms.** Moderate confidence. Alternative: a hand-written query list per node, sixty lists to keep current. The criterion already says what would count, and a model reads it better than a keyword list does; the `watch` field (new, optional, on the node record) is for the cases where the plain reading misses a term of art or a project name.

5. **A TOML scan record per run, exported to the site, appended and never edited.** High confidence; the same shape as the ledger and the node files, validated the same way.

6. **Deploy by a GitHub Actions workflow on every push to main that touches the tree, the scripts or the site.** High confidence; standard practice, and the only way a cloud session with no Cloudflare credentials can put its work on the site. Alternatives: Cloudflare's own build-on-push (needs Python in its build image, which is unverified), or the manual `npm run deploy` (which makes the weekly update wait on John, defeating the purpose). Needs two repository secrets, John's action (step 35). The workflow is in `.github/workflows/deploy.yml`.

7. **Three surfaces: the Radar page, the home strip, the node page's last three checks.** Moderate confidence. Alternative: the Radar page alone. The strip is the surface most people will see and is one line; the node page's line is what makes a node's number trustworthy at a glance.

8. **After-the-fact review as a standing item in the quarterly scan, and a first audit two scans in.** High confidence. John reads the scanner's entries since the last review, writes correcting revisions where he disagrees, and adjusts the cap or the watch terms. The first audit (step 38) is deliberately early so the procedure is tuned on two real weeks rather than a guess.

## Steps

34. **Scan record schema and export** (done 2026-09-19). `data/scans/` per the record above; a validator in `export.py` (id uniqueness, verdict set, sources present, ledger ids resolve, node ids exist); `site/src/data/scans.json` written on every build, newest scan first, with each item's factor and chain link resolved from the node. Done when a hand-written test scan file exports and a malformed one is refused. Two things the record above did not settle, decided while building: a scan record may carry `test = true`, which marks a hand-made file that stands in for a real week and which the site labels everywhere it appears (the validator also let such a file name a ledger entry that was never written; that exemption is gone, see below), and a ledger id is checked for shape always but only resolved against `data/ledger.toml` once that file exists, since the ledger lands with ledger plan step 30. The hand-made test record dated 2026-09-19 has been replaced by the first real scan of the same date, so no fixture is left in `data/scans/` and a record marked `test = true` no longer gets any exemption from the rules; the `test` mark itself stays, so a future fixture is still labelled as one on the site.

35. **Deploy on push, and repository access for the scanner** (waits on nothing; John). Add `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` as repository secrets so `.github/workflows/deploy.yml` can run, and authorise `jfredson/belt-equation` for the cloud environment's git proxy so the scheduled task can push. Done when a push to main deploys beltequation.com without a hand on the keyboard, and a scan's push is accepted.

36. **The scan procedure and the scheduled task** (done 2026-09-19). `docs/scan-procedure.md` is the standalone instruction a fresh session follows; the scheduled task's prompt only says to clone the repository and follow that file, so the procedure can change without touching the task. The task is created and fires Sundays at 18:00 Pacific. Until steps 28 to 30 land, a scan that moves a number still logs the revision and the scan file but skips the ledger entry and the snapshot, saying so in its commit message; the first scan after those land backfills the entries.

37. **The Radar page, the home strip, and the node page's last checks** (done 2026-09-19). Done when the latest scan renders with its counts, a `moved` card links to its ledger entry, and every node page shows its last check. The page is `/radar/`, in the site's navigation as "This week's reading". One thing could not be finished as written: a `moved` card cannot link to its ledger entry yet, because the ledger does not exist until ledger plan step 30. The card names the entry and says it is not written yet, and the link appears on its own once the entry is there.

38. **First audit** (two scans after step 35 lands; target 2026-10-11). John reads every scanner entry and scan item to date, corrects what he disagrees with by revision, and rules on the cap and the load split. Done when the changelog records the audit and any change to this plan.

## Deferred, and why

- **Reader-submitted items** ("did this move anything?"). Same answer as the ledger plan: a GitHub issue with a label, answered by a scan item or a held-steady entry. No new machinery before roadmap step 16.
- **Scanning for the A branch.** Provisional until John completes his current training in May 2027; its world nodes (the training industry, the route that stays in his current career) join the scan then.
- **Searching beyond the open web** (preprint servers by API, launch databases by feed). The criteria name their sources and a web search reaches most of them; a per-source fetch is worth adding only once a scan has demonstrably missed something a feed would have caught.
- **The scanner proposing new nodes.** It may flag a gap it noticed; adding a node is structural and stays with John and the annual review.
