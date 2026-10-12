# Belt Equation — instructions for Claude

These two rules were memory notes that loaded for every project; they moved here
2026-10-12 so they load only in this repo. The workspace `CLAUDE.md` in `~/Code` still
applies on top.

## Commit on main and push

In an interactive session, commit on `main` and push at the end of each working
session, without asking. Ruled by John 2026-09-08, after a background-job session left
a review commit on a side branch and asked him to merge it. The repo is a public
documentation-and-data project with one author, so a branch-and-merge step is a chore
with no review benefit; `docs/roadmap.md` already says "commit at the end of every
session".

Background-job sessions cannot push to `main`. If a task here runs as a background job,
say up front that the result will land on a branch, and open a pull request so the merge
is one click.

## Every design choice comes with confidence and an alternative

Ruled by John 2026-09-08. Before asking John to accept any design choice (a schema
field, a method, a file layout), give him, as a short table or list:

1. The choice.
2. How confident you are (high, moderate or low), with a sentence on why.
3. Whether it is standard practice or a judgment call.
4. The strongest alternative and what it would cost.

Flag any proposal you would change yourself on reflection. This came from six
node-schema proposals where the exercise changed two of them. The same ground rule is in
`docs/roadmap.md`.
