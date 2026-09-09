# The Belt Equation

What is the probability that I become a Belter before I die, and how does that number move year over year?

The Belt Equation is a public, long-horizon prediction project. It takes a question most people file under science fiction, whether a settled solar system like the one in The Expanse arrives within a single human lifetime, and breaks it into a handful of factors anyone can argue about, the way the Drake Equation did for the number of civilizations in the galaxy. Under each factor sits a tree of concrete breakthroughs, each with its own probability, its own resolution criterion, and its own revision history. The headline number is computed from the tree, never chosen by hand, and the whole thing is re-estimated on a fixed schedule and published so other people can disagree with specific pieces of it.

The "I" in the question is a real person with a real expected lifespan, which is what turns an abstract forecast into something you can track your own life against. Anyone can run their own version.

## The equation

    P(Belter) = W × L × E × D × B × M × R × A

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

- `docs/` holds the plans and definitions. Start with `docs/2026-09-08-kickoff.md` (the plan) and `docs/definitions.md` (what the terms mean, and the decisions behind them).
- `data/` holds the tree itself, one record per breakthrough. Empty until the first node brainstorm.
- `scripts/` holds the code that computes the headline numbers from the tree. Empty until the tree exists.
- `CHANGELOG.md` records every revision to the tree or the definitions, with absolute dates.

## Status

Created 2026-09-08. The project is at the definitions stage: no nodes, no probabilities yet. The first public version is targeted for 2026-11-16.

## Author

John Fredrickson, with Claude as a working partner. Published under the Sentient Horizons project.
