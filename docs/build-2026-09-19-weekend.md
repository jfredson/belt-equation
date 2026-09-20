# Weekend build, 2026-09-19 to 2026-09-21: the ledger and the Radar

Plan for the block. Goal: by Monday morning 2026-09-21 the site records what moves the needle (ledger plan, steps 28 to 33) and is scanned every week by the scheduled task (scan plan, steps 34 to 38), with the first scan on 2026-09-27 landing on a working pipeline. Two Claude Code sessions run in parallel from ~/Code, each on its own branch and worktree, plus John's own track. Cowork wrote the plans and the procedure and created the scheduled task on 2026-09-19 (step 36 done).

## Track 1, Claude Code: the ledger (steps 28 to 32)

Branch `ledger-steps-28-32`. Sequential within the session: 28 snapshots, 29 worth and attribution, 30 the ledger file with the 2026-09-19 backfill, then 31 the Ledger page and history charts, 32 watch lists and worth lines. Step 33 (feeds, badge, scan procedure rewrite) can follow in the same session if time allows; the scan procedure half of it is already covered by docs/scan-procedure.md.

Kickoff prompt:

    Read belt-equation/docs/ledger-plan.md (ruled in full by John on 2026-09-19, all eight
    decisions as proposed) and belt-equation/docs/scan-plan.md (which adds an optional
    `author` field to the ledger record and an optional `watch` list to the node record).
    Build steps 28 through 32 in order on branch ledger-steps-28-32 in a worktree, standard
    library only in scripts/, the site's existing styles for pages. Commit per step with
    absolute dates in messages, changelog lines per step, and open one PR at the end.
    Do not touch data/scans/ or scripts/export.py's scans section; Track 2 owns those.
    When you add to export.py, add a function per section so the two branches merge cleanly.

## Track 2, Claude Code: the Radar (steps 34 and 37)

Branch `radar-steps-34-37`. Smaller; merge it first.

Kickoff prompt:

    Read belt-equation/docs/scan-plan.md and belt-equation/docs/scan-procedure.md. Build
    step 34 (data/scans/ validator and scans.json export, as a separate function in
    scripts/export.py) and step 37 (the /radar page, the home-page strip under the headline,
    and the last-three-checks line on node pages) on branch radar-steps-34-37 in a worktree.
    Write one hand-made test scan file dated 2026-09-19 with scope "weekly" and a handful of
    items covering every verdict, using real node ids, so the page has something to render;
    mark it in its [scan] table with `test = true` and have the site label it as a test.
    Add the optional `watch` field to docs/node-schema.md's table and to the validator.
    Standard library only in scripts/, the site's existing styles. Do not touch
    data/ledger.toml, data/snapshots/, or compute.py; Track 1 owns those. Commit per step,
    changelog lines, one PR.

## Track 3, John

1. Repository secrets for the deploy workflow: in the GitHub repo, Settings, Secrets and variables, Actions, add `CLOUDFLARE_API_TOKEN` (a token with Workers Scripts: Edit and Workers Routes: Edit for the beltequation.com zone) and `CLOUDFLARE_ACCOUNT_ID`. Then push anything to main, or run the workflow by hand from the Actions tab, and confirm beltequation.com redeployed.
2. Authorise `jfredson/belt-equation` for the Cowork cloud environment so the scheduled scan can push (on 2026-09-19 the cloud git proxy refused a push with "not in this session's authorized repository set"). This is set where the cloud environment's repositories are configured.
3. Merge Track 2, then Track 1, in that order; resolve the export.py merge if both touched its main function.
4. After the first two scans (2026-09-27 and 2026-10-04), the audit at step 38: read the scanner's entries, correct by revision where you disagree, rule on the 0.10 cap.

## Order of merges and what the first scan needs

The scheduled task fires Sunday 2026-09-20 at 18:00 Pacific, before any of this is merged. That run reads the tree as it is and follows the procedure's fallbacks: it writes the scan record, edits nodes if anything moved, skips the ledger entry and snapshot, and if the push is refused it delivers the record in chat and stops. That is fine; treat it as the dress rehearsal. The scan on 2026-09-27 is the first that should land end to end.
