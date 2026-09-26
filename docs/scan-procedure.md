# Weekly scan procedure

The standalone instruction for the scheduled Radar scan (docs/scan-plan.md, step 36). A fresh Claude session with no memory of any earlier conversation follows this file from top to bottom. Written 2026-09-19. When this file and the plan disagree, this file wins for the scan and the disagreement is a flag for John.

## 0. Orient

- Get the date in John's timezone before anything else: `TZ=America/Los_Angeles date +%F`. That is the scan's `date`; every date you write is absolute (YYYY-MM-DD), never "today" or "last week".
- The repository is already cloned if you are reading this; if not: `git clone https://github.com/jfredson/belt-equation` in the cloud workspace and `cd` into it. Never work in the linked computer's copy at ~/Code/belt-equation; John's own sessions run there.
- Record `git rev-parse --short HEAD` as `commit_before`.
- Read docs/node-schema.md (the record you will edit), docs/ledger-plan.md (the "Ledger entries" table, for the entry you may write), and this file. Skim data/README.md.
- Scope: if this is the first scan of the calendar month (no file in data/scans/ dated this month), scope is `monthly` and you check every eligible node; otherwise scope is `weekly` and you check eligible leaves only.
- Eligible: `kind = "world"`, `status = "open"`, factor in W, L, E, D, B, M, R, C. Never the A branch. Never choice nodes.
- Load the tree with Python's `tomllib` to get the list; do not parse by hand.

## 1. Read each node against the world

For each eligible node, in file order:

1. Compose two to four web searches from the node's `name`, `resolution` and `source`, plus every term in its `watch` list if it has one. Ask for the past week (or the past five weeks on a monthly scope for mid and root nodes). Prefer the source the node names: a launch log, an agency announcement, a journal, a regulator's register.
2. Read the results that bear on the criterion. Read the criterion literally; the standard is "two people reading it would agree whether it has happened", so a target date, a plan, a funding round or a press claim is not the event.
3. Give one verdict:
   - `quiet`: nothing in the window bears on the criterion.
   - `noted`: something relevant happened and no number moves. `found` says what and why not. If it was widely reported (major outlets, not trade press alone), you will also write a `held-steady` ledger entry in step 3.
   - `moved`: the evidence changes the probability. Decide the new value per scenario, capped at 0.10 absolute from the current value in each scenario, in the same direction in all scenarios unless the evidence says otherwise. Sources required.
   - `resolved`: the criterion is met on the plain reading and two independent public records agree (the operator plus an independent observer; a journal plus a registry). Sources required, both listed.
   - `flagged`: anything you may not do (a move over the cap, a criterion that no longer fits the world, a node you think is missing, a resolve-no, anything in the A branch or in tiers, scenarios, definitions, methodology). `for_john` states the move you would have made and the evidence. Make no edit.

Search economy: stop at four searches per node. If a search tool fails twice, mark the node `quiet` with `found = "search unavailable"` and move on.

## 2. Edit the tree (moved and resolved only)

Edit the TOML by text, keeping the file's formatting (one field per line, the existing key order). After every file edit run `python3 -c "import tomllib,sys; tomllib.load(open(sys.argv[1],'rb'))" data/X.toml` and then `python3 scripts/compute.py validate`. If validation fails, revert that file (`git checkout -- data/X.toml`), mark the node `flagged` with the error in `for_john`, and continue.

For `moved`:
- Set `probability` to the new values, `estimated_on` to the scan date, and rewrite `rationale` in one line.
- Append to `revisions` (create the list if absent) one table per changed field, `{ date = <scan date>, field = "probability", old = "<old table as text>", new = "<new table as text>", why = "[scan YYYY-MM-DD] <one sentence with the source>" }`. Match the style of an existing `revisions` entry in data/R-regime.toml.

For `resolved`:
- Set `status = "resolved-yes"`, `resolved_on` to the date it happened in the world (from the sources), `resolved_by` to the record that settled it, and `resolved_links` to a list of one or more URLs for that record (required; the validator refuses a resolved node without one).
- Append a `revisions` entry for `status` with the same `[scan YYYY-MM-DD]` prefix.

Never edit any other field. Never edit a node you did not mark `moved` or `resolved`.

## 3. Write the ledger entries (only if `data/ledger.toml` exists)

If data/ledger.toml does not yet exist (ledger plan step 30 not landed), skip this step and say so in the commit message; the scan record still carries the verdicts. Otherwise append one `[[entry]]` per moved, resolved and widely-reported noted node, per the ledger plan's table, newest last, with these particulars:
- `id = "YYYY-MM-DD-<slug>"` using the scan date; `date` the scan date; `occurred_on` the world date when it differs.
- `kind` is `event` for moved, `resolution` for resolved, `held-steady` for the noted ones (with `checked_against`, no `nodes`).
- `author = "scan"`.
- `title` one plain sentence in the chain's vocabulary (link names, not factor letters); `body` two to five sentences; `source` the public record.
- `snapshot` is the key of the snapshot the publish command takes in step 6 (`YYYY-MM-DD-scan`), even though you write it before running.

## 4. Write the scan record

Write `data/scans/YYYY-MM-DD.toml` (create the folder if absent) exactly in the shape given in docs/scan-plan.md under "The scan record": a `[scan]` table with `date`, `ran_at` (UTC, from `date -u +%Y-%m-%dT%H:%M:%SZ`), `scope`, `nodes_checked`, `searches`, `commit_before`, then one `[[item]]` per node checked, in the order checked, with `node`, `verdict`, `queries`, `found` (one to three sentences, plain English, absolute dates), `sources` for every verdict but quiet, `ledger` for moved and resolved when an entry was written, `for_john` for flagged. Validate it with tomllib. If the folder already has a file with today's date, suffix `-2`.

## 5. Changelog

Add one line under a `## YYYY-MM-DD` heading at the top of CHANGELOG.md (create the heading if today's is absent): "Weekly scan (scheduled task, YYYY-MM-DD): N nodes read, M moved, K resolved, F flagged for John; record at data/scans/YYYY-MM-DD.toml." Name each moved or resolved node and its before and after in the same line.

## 6. Publish: one command

The last step is one command, `scripts/publish.py` (website step 26, 2026-09-25). It checks the tree, takes the snapshot when asked, redraws the tree picture, writes the site's data (which also checks the ledger and the scan record you just wrote), builds the site, prints what changed with the headline before and after, then commits everything as one commit and pushes main. The deploy action on GitHub builds and deploys the site from that push; the script does not deploy by any other road. Replace the capitals with the scan's own date and counts:

    python3 scripts/publish.py --push \
      --message "Weekly scan YYYY-MM-DD: N read, M moved, K resolved, F flagged" \
      --message "<one line per move, with before and after; or 'Nothing moved.'>" \
      --message "<the attribution lines this session was given>" \
      --fallback-branch claude/scan-YYYY-MM-DD

- If anything moved or resolved, add `--snapshot scan`. That writes `data/snapshots/YYYY-MM-DD-scan.json`, the key the ledger entries from step 3 name. It adds about ten minutes.
- The story snapshots in data/story/ are refreshed only where the TimeAssembler key is present. A cloud session has none, and the script leaves them alone and says so; that is expected.
- If the script stops at steps 1 to 5 of its own output, the scan's edits broke a rule: read the message, fix the edit or revert that file and mark the node `flagged` (as in step 2), and run it again.
- If it stops at step 6 of its own output (building the site) for a reason that is not the scan's data, such as Node missing or the site's packages not downloading, do not fight it: run `python3 scripts/export.py --check`, then `git add -A && git commit` with the same message and `git push origin main` (falling back to the branch below), and put the build error in the report. The deploy action builds the site on its own after the push.
- A refused push: with `--fallback-branch`, the script pushes the same commit once to `claude/scan-YYYY-MM-DD` (routines always accept `claude/` branches) and says so. Report the branch name and the refusal message so John can merge it; the site does not update until he does. If that push is refused too, do not retry: put the scan record's contents in the report and stop. (Rule amended 2026-09-19 after the dress rehearsal, which lost a 44-node scan to a refused push.)

## 7. Report

Send John one short message, a numbered list and nothing else: first what he needs to do (each flagged item with its `for_john` line, and the push refusal if there was one), then one line per moved or resolved node with before and after, then one line with the counts. No prose, no summary of quiet nodes.

## Standing rules

- Commas rather than em dashes; absolute dates; plain English with any shorthand explained on first use.
- Read, do not infer: a node moves on evidence about its criterion, not on mood about the field.
- One scan, one commit, made by the publish command in step 6. Never force-push, never rebase, never touch a branch other than main (and the one fallback branch in step 6).
- If anything in this file cannot be followed as written, do the parts that can, flag the rest for John in the report, and never improvise an edit outside the limits in docs/scan-plan.md.
