# Book tracking setup (2026-09-25)

Set up 2026-09-25 on John's instruction. After several years of tracking, John may write a book about this project. The book would be about the method, not the numbers: keeping a public forecast of a personal dream, simulated many thousands of times over, and letting it steer near-term decisions. Its material is therefore the changelog, the runs that compared real options, the arguments over method, and the person's state over time. This document records how that material is captured now, cheaply and with dates, so it exists when it is wanted.

## Where things live

- **docs/private/book/book-log.md** (private, ignored by git). Four dated lists, one line per entry:
  - *What I got wrong*: a probability, structure or wording that a review or an event overturned, in John's words.
  - *Decisions the number changed*: a real-life choice where a run of the tree, or one step's probability, moved what John did. Points at the choice runs below.
  - *Method fights*: rulings that changed how the instrument works (for example the Contact Clause null rule, 2026-09-19, and retiring the phrase "become a Belter" from the site's copy, 2026-09-25).
  - *Moments*: the human parts: family reactions, doubts, wonder.

  Seeded 2026-09-25 from the existing record (the run notes, the 2026-09-19 review rulings, the methodology pass, the Contact Clause proposal, the ledger and scan plans, the changelog and git history). Every seeded entry names its source file and is marked [seeded], since John did not write it in his own words.
- **docs/private/book/state-snapshots.md** (private, ignored by git). One dated block per quarter in John's own words: what he is doing, training in miles, the headline number that quarter, and what he is deciding. The first block, for the third quarter of 2026, is left blank for him to fill.
- **docs/runs/README.md** (public). The choice-run convention: every run of the tree made to compare real options is saved as `docs/runs/YYYY-MM-DD-choice-<slug>.md`, with the options, the headline per option, the decision taken and a dated note.

The private files stay private until at least May 2027. This document is public, and says nothing more personal than the paragraph about John in docs/definitions.md already does.

## Start criteria, written in advance

The book is not started until both hold: at least three annual reviews are on record (2027, 2028, 2029), and at least one of John's own access steps has resolved (the A0 or A1 rung). Until then the log is capture only.

## How capture happens without a new habit

Capture is wired into procedures that already run:

- **Weekly scan** (docs/scan-procedure.md, step 8): if the scan moved a probability or resolved a step, it writes one line for the book log under "What I got wrong" or "Moments". A cloud scan cannot see the private folder, so it puts the line in its report for John to paste.
- **Quarterly leaf scan** (docs/roadmap.md, step 17, and the book note after step 19): prompts a state snapshot.
- **Annual review** (docs/roadmap.md, step 18, and the same book note): prompts a "What I got wrong" pass over the year's CHANGELOG.md.

Nothing in data/, no number, and no public page changed in setting this up.
