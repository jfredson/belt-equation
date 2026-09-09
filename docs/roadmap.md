# Roadmap: from seed to tracking

Written 2026-09-08. This is the working plan for the months before the SERE pipeline resumes in early 2027. It is written so that a Claude Code session started from ~/Code can pick up any step cold. Paths are relative to ~/Code. Mark steps done here and in the TimeAssembler "Belt Equation" project roadmap; log each working session there as well.

What is already settled is in belt-equation/docs/definitions.md. Read that first. Do not reopen decided items without John saying so.

## Ground rules for every session

- Plain language in everything: node names, rationales, commit messages. Someone outside the project should understand every line.
- Absolute dates everywhere (2026-09-08, never "today" or "last week").
- Nothing personal about John's health goes into this repo. The access branch stays a sketch until pipeline graduation (expected May 2027).
- No probabilities until the tree is stable (end of Phase 2). Estimating against a moving structure wastes the estimates.
- Every change to the tree or the definitions gets a dated line in belt-equation/CHANGELOG.md.
- Commit at the end of every session. From a Claude Code session on the Mac this is ordinary git; from a Cowork session the lock files git leaves behind have to be moved out of the way (see the note at the bottom).

## Phase 1. Definitions complete (target 2026-09-21)

1. Read belt-equation/docs/definitions.md end to end and fix anything inconsistent with the kickoff outline. Done when both documents agree.
2. Write belt-equation/docs/node-schema.md: the record layout for one node, with a worked example. Fields: id, name, factor (W, L, E, D, B, M, R, A, or C for the Contact Clause), kind (world event or choice point), description, resolution criterion and source of truth, dependencies, which tiers it feeds, horizon class (leaf, mid, root), probability by scenario (left blank until Phase 3), rationale, status, revision log. Choose the file format for data/ here (a plain text format that reads well in a diff; one file per factor is the current preference).
3. Refine the window placeholder from the health record. This step runs in a Cowork session with the Health folder connected, and only the resulting date (with a plus-or-minus) comes back into definitions.md. Nothing else.

## Phase 2. Tree version zero (target 2026-10-12)

4. Brainstorm the node list, one factor per session, aiming for 40 to 60 nodes total with at least a third of them leaves that could resolve within five years. Seeds for each factor are in the kickoff outline under "Branch seeds" and in definitions.md under the Contact Clause and the access branch. For each node, write the resolution criterion before anything else; a node without one is not a node.
5. Add the habitat branch explicitly (orbital construction, materials, lunar material supply, and the rotating-habitat hedge on biology).
6. Mark choice points in the access branch and list the options at each one.
7. Draw the dependency edges and check for cycles. A leaf that depends on a root is a sign the horizon classes are wrong.
8. Review pass: read every node aloud in plain language and cut, merge, or rename anything that fails the "someone outside the project understands it" test.

## Phase 3. First probabilities and the calculation (target 2026-10-26)

9. Write belt-equation/scripts/compute.py: load the tree, run it many thousands of times with random outcomes while respecting dependencies, and report the probability of each system tier and each access tier under each of the four longevity scenarios, plus the Contact Clause rungs separately. Keep it to plain Python with no dependencies beyond the standard library if possible. Include a check that refuses to run if any node lacks a resolution criterion.
10. First-pass probabilities, one factor per session, with a one-line rationale each. John's estimates, with Claude proposing a number and a reason for him to accept or move. Record every number with its date.
11. Run the calculation. Read the results against intuition. Where the computed number disagrees badly with gut, the tree is probably missing a dependency or a node; fix the tree, not the number.
12. Write belt-equation/docs/methodology.md: how the numbers are computed, how the calibration score works (the standard measure of how well probabilities match outcomes, computed on resolved leaves each year), and how the choice-point comparison is run.

## Phase 4. First presentable version (target 2026-11-16)

13. Produce one visual of the tree with current numbers, colored by factor. A static image is fine.
14. Draft the introductory essay for Sentient Horizons: the question, the equation, the tiers, the headline numbers under each scenario, the three or four nodes that dominate the result, and an explicit invitation to name a missing node or move a probability. Voice Calibration is the final gate, per the Sentient Horizons protocols.
15. Draft the family-and-friends version: shorter, conversational, the same numbers, written to start a dinner-table argument rather than to be read by strangers.
16. Decide, with John, when and whether to post beyond family and friends.

## Phase 5. Tracking begins (from 2026-11-16 onward)

17. Set the quarterly scan as a recurring task (fifteen minutes: which leaf nodes resolved or moved, log them).
18. Schedule the first annual review for January 2027, before the pipeline resumes.
19. Fold any public or family critique into the tree before that review.

## Later, not now

- A standalone site, after the tree has changed at least once from outside critique.
- Public names for the access tiers.
- Extending the access ladder above A3, if the world moves.
- The possible missing rung between one flight (A1) and a months-long rotation (A2).
- Refining the access branch with real detail after pipeline graduation, May 2027.

## Note on committing from a Cowork session

The Cowork workspace cannot delete files, so each git commit leaves lock files (.git/index.lock, .git/HEAD.lock, .git/objects/maintenance.lock, and tmp_obj_* files) that block the next commit. Move them to ~/Code/_to_delete/belt-equation-git-leftovers/ before committing again, and delete that folder from the Mac whenever. Claude Code sessions on the Mac do not have this problem.
