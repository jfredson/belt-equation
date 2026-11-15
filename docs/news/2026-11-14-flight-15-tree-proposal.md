# Starship Flight 15 and the tree: a proposal for John's ruling

Written 2026-11-14 by Claude, in the session that rewrote the Flight 15 post as an essay (branch
`claude/flight-15-essay-2026-11-14`). Nothing in `data/` is changed. This note proposes; John rules.

## What happened, in one paragraph

On 2026-11-13 Starship's fifteenth flight launched. The booster (Booster 22) called off its tower catch
about six and a half minutes in, after a "low fuel mass alarm" cut its turn-back burn short, and it was
lost over the Gulf of Mexico. The upper stage (Ship 42) reached orbit, flew 14 orbits and was caught by
the tower at Starbase at about 3:20 p.m. Texas time on 2026-11-14, the first recovery of a Starship
upper stage. SpaceX has not said whether Ship 42 will fly again; Gwynne Shotwell said on the
2026-10-20 earnings call that SpaceX aims to "refly the second stage by early next year". Sources are
listed in `docs/news/2026-11-13-starship-flight-15-checks.md`, last section.

## What the Radar scan has recorded

The last scan ran on 2026-11-08, before launch (`data/scans/2026-11-08.toml`). It read
`L-fully-reusable-heavy-launcher-recovers-both-stages` as quiet: "No ship catch has happened ... Flight 15
... is a plan and not the event." Nothing has been recorded since. The next scan runs on Sunday
2026-11-15 at 18:00 Pacific, as the cloud routine that pushes to `main`. Following the brief, nothing in
the tree is changed here.

## The steps the catch bears on

| Step | Baseline by 2071 now | What the catch does |
|---|---|---|
| A heavy launcher recovers both of its stages intact from one orbital flight (`L-fully-reusable-heavy-launcher-recovers-both-stages`) | 0.95 (moderate 0.96, strong 0.97, radical 0.98, open 0.98) | Not met. The resolution asks for both stages from one flight, each confirmed by the operator as able to fly again. The booster was lost, and no statement on the ship's condition has been found. The catch shows the harder half can be done. |
| A fully reusable heavy launcher flies 100 orbital missions in one calendar year (`L-heavy-launcher-100-per-year`) | 0.85 | No direct bearing. Starship has flown four times in 2026, counting this flight. |
| Mass to low Earth orbit is sold for under $200 a kilogram (`L-launch-price-below-200-dollars-per-kg`) | 0.60 | No direct bearing. Its rationale already says price is a demand-and-competition question, not a cadence one. |
| A hundred tonnes of propellant pumped between spacecraft in orbit (`L-orbital-propellant-transfer-at-scale`) | 0.90 | No bearing. Refilling is a separate test, targeted for early 2027. |

## Proposal: hold every number, and add one held-steady ledger entry

Laid out as the repository's design rule asks (`CLAUDE.md`, "Every design choice comes with confidence
and an alternative"):

1. **The choice.** Hold all four steps where they are. Record the flight as a held-steady ledger entry,
   the way Flight 14 was recorded (`2026-10-04-starship-reaches-orbit-no-recovery`).
2. **Confidence: moderate to high.** The 0.95 already assumed the ship catch would come; its rationale
   reads "the residual risk is a program cancellation, not physics". A catch of the ship half is
   evidence for that rationale, but the step's own test (both stages, one flight, fit to fly again)
   is not met, and the risk of cancellation, which is what the 0.05 stands for, is barely touched by
   one good flight. A move from 0.95 is within what one event should be allowed to do.
3. **Standard practice or judgment call.** The rule that a step moves on its resolution test, and that a
   partial event is held steady, is the practice the ledger already follows (Flight 14). How much a
   partial success should nudge a high estimate is a judgment call.
4. **The strongest alternative.** Raise the step's baseline from 0.95 to 0.97 (and the other scenarios
   to 0.97, 0.98, 0.98, 0.98), on the reasoning that the ship catch was the one unproven piece of
   physics, and that its success shifts weight from "might never work" to "a matter of schedule". It
   costs little: the headline would move by far less than the spread between runs, and the move
   could be argued as reacting to the news. I would not make it before the reflight; a caught ship
   flying again, or both stages from one flight, is the evidence that would justify it.

On reflection I would not change this proposal.

## A draft ledger entry, if John rules to hold

Either the Sunday scan writes its own, or this one is added by hand; not both. If added by hand, it
belongs in `data/ledger.toml` after the last entry, with `snapshot` set to the scan's snapshot name.

```toml
[[entry]]
id = "2026-11-15-starship-ship-caught-booster-lost"
date = 2026-11-15
occurred_on = 2026-11-14
kind = "held-steady"
title = "Starship's upper stage was caught at the tower on 2026-11-14, but the booster was lost, so the launch steps stay where they were"
body = """
Flight 15 lifted off on 2026-11-13. The booster called off its tower catch about six and a half
minutes in, after a low fuel mass alarm cut its turn-back burn short, and was lost over the Gulf of
Mexico. The upper stage reached orbit, deployed 26 Starlink V3 satellites, flew 14 orbits and was
caught by the tower on 2026-11-14, the first recovery of a Starship upper stage. The step asking for
both stages of a heavy launcher to be retrieved from one orbital flight, each confirmed able to fly
again, is not met: the booster was lost, and SpaceX has not said whether the caught stage will fly
again. SpaceX's stated target for reflying an upper stage is early 2027."""
source = "https://www.cbsnews.com/news/spacex-catch-starship-rocket/ and https://www.space.com/news/live/spacex-starship-flight-15-live-updates-nov-14-2026-starship-first-double-landing-attempt"
checked_against = ["L-fully-reusable-heavy-launcher-recovers-both-stages", "L-heavy-launcher-100-per-year"]
author = "scan"
snapshot = "2026-11-15-scan"
```

If the essay goes up before the scan has run, its section "What the catch did to the numbers" says the
next scan reads the catch on November 15th. If John rules to move the number instead, that section
needs rewriting before publishing.
