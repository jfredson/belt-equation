# The Belt Equation

What is the probability that, before I die, I live and work in a solar system where human industry reaches beyond Earth and Mars? And how does that number move year over year?

The name comes from the Belters of The Expanse, the people who live and work in its asteroid belt.

The Belt Equation is a public, long-horizon prediction project. It takes a question most people file under science fiction, whether a settled solar system like the one in The Expanse arrives within a single human lifetime, and breaks it into a handful of factors anyone can argue about, the way the Drake Equation did for the number of civilizations in the galaxy. Under each factor sits a tree of concrete breakthroughs, each with its own probability, its own resolution criterion, and its own revision history. The headline number is computed from the tree, never chosen by hand, and the whole thing is re-estimated on a fixed schedule and published so other people can disagree with specific pieces of it.

The "I" in the question is a real person with a real expected lifespan, which is what turns an abstract forecast into something you can track your own life against. Anyone can run their own version.

## The equation

    P = W × L × E × D × B × M × R × A

Each factor is a probability between 0 and 1 that a necessary condition is met before the deadline:

- **W, window.** That I am alive on the date in question. This is a curve over time, not a single number, and the longevity research nodes feed it.
- **L, launch.** That the cost of putting mass into orbit falls below the threshold that makes everything else affordable.
- **E, energy.** That cheap, abundant power exists off Earth, from fusion or an equivalent.
- **D, drive.** That propulsion puts the solar system within reach on human timescales. This is the factor that separates a slow, sparse solar system from the one in the show.
- **B, biology.** That humans can live, and eventually reproduce, in partial gravity and deep-space radiation.
- **M, motive.** That there is an economic reason for large numbers of people to be out there.
- **R, regime.** That the political and legal conditions let a multi-decade build survive elections, downturns, and wars.
- **A, access.** That I personally have a pathway in, given my training, health, and career.

The factors are a way of talking about the tree, not a literal multiplication of independent numbers. The actual computation runs the tree many thousands of times with random outcomes, honoring the dependencies between breakthroughs, and reports how often each end state is reached. See docs/definitions.md for the tiers, the deadline, and what each factor means in detail.

## Layout

- `docs/` holds the plans and definitions. Start with `docs/definitions.md` (what the terms mean, and the decisions behind them) and `docs/roadmap.md` (the work plan). `docs/2026-09-08-kickoff.md` is the original outline, kept as the record of where the project started.
- `data/` holds the tree itself, one record per event, in one TOML file per factor; beside it the ledger of what moved the headline (`ledger.toml`), the weekly scan records (`scans/`), the saved runs (`snapshots/`) and `headline.json`, the one small file other sites read for the headline. See `data/README.md`.
- `scripts/` holds the code that computes the headline numbers from the tree (`compute.py`), exports it for the website (`export.py`), publishes in one command (`publish.py`) and tests itself (`test_*.py`). See `scripts/README.md`.
- `site/` holds the website, beltequation.com (live since 2026-09-19): an Astro static site that reads the exported tree at build time and serves the headline file at `/data/headline.json`. See `site/README.md` and `docs/website-plan.md`.
- `CHANGELOG.md` records every revision to the tree or the definitions, with absolute dates.

## Status

As of 2026-10-17. The headline is 0.465 percent: the chance, by 2071, that I live and work in a solar system where human industry reaches beyond Earth and Mars, from the run of 2026-10-11 (snapshot `2026-10-11-scan`, 20,000 play-throughs). The nearer thing beside it, a rotation at a station or a lunar base whether or not industry goes further, is 9.3 percent. The headline has stayed near half a percent by 2071 since the outside-model review landed on 2026-09-20; every move since has been within the dice.

- **The tree** has 81 events, 76 with a probability under each of the five longevity scenarios and 3 already resolved. Every number is computed from it; none is typed by hand.
- **The site** at beltequation.com has been live since 2026-09-19 and has worn its own skin, "Ore", since 2026-10-17, on the Sentient Horizons design standard. The project stays under-promoted: the family-and-friends note (drafted 2026-09-20) has not been sent, and the introductory essay for Sentient Horizons is drafted and waits on my read.
- **The weekly scan** reads the events that could resolve within five years against the week's news every Sunday at 18:00 Pacific, as a cloud routine that pushes to `main`, and the whole tree on the first scan of each month; a digest on Monday mornings reports what it found. Six scans so far, the last on 2026-10-11: nothing has moved, nothing has resolved, and three items were flagged for me and ruled on. Each leaves a record in `data/scans/` and a line in the site's Radar page.
- **Reviews.** The outside-model review of every number (105 rulings) was ruled on 2026-09-19. The first cross-project lessons review across the Sentient Horizons family was held on 2026-10-17; this repository's first adoptions from it are the last-checked strip in the tracker pattern's words, the headline file served from the site, and this paragraph. The quarterly scan first runs on 2027-04-04 and the annual review, every number re-estimated, each January, first on 2027-01-03.

Created 2026-09-08. Until 2026-10-17 this section still read "no nodes, no probabilities yet" with a first public version targeted for 2026-11-16; the tree was built between 2026-09-08 and 2026-09-25 and the site went live early. The dated record of every change is `CHANGELOG.md`.

## Licence

The tree and every other data file are under Creative Commons Attribution 4.0 (`LICENSE-DATA`): reuse them freely, with credit. The scripts and the site are under the MIT licence (`LICENSE`). Added 2026-10-08 under the Sentient Horizons design standard.

When you reuse the data or the text, please credit it as: *The Belt Equation*, by John Andrew Fredrickson, a Sentient Horizons project, https://beltequation.com/

## Author

John Fredrickson, with Claude as a working partner. Published under the Sentient Horizons project.
