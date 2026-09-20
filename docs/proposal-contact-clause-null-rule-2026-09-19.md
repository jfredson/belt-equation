# Proposal: the Contact Clause null rule, and a rung for machine communion

Drafted 2026-09-19 by Claude from a conversation with John about Alex O'Connor's treatment of God (analysis in `sentient-horizons/ops/captures/oconnor-realism-closer-to-truth-analysis.md`). Status: proposed. Nothing here is applied; `data/C-contact.toml` and `docs/definitions.md` are unchanged until John rules.

## Why

The Contact Clause is a hope held beside the equation and multiplied into nothing. That is the right shape, and it is the shape a calibrated belief in God would have. The discipline that keeps it honest is the null: C stays unresolved until unequivocal evidence, and the hope is never allowed to certify its own confirmation.

The clause as written has one gap. The dream in definitions.md names two forms of communion, "a machine intelligence that has exceeded us or something of non-human origin." The rungs cover the second (C3, C4, which excludes anything human-built) and cover the machine case only as knowledge transfer (C1, C2). Communion with a machine mind of another perspective has no rung. It is also the one form of the dream that could plausibly arrive in the window, and the one John most wants, so it is where the mirage risk concentrates: nothing on the board can resolve, but the feeling of communing with a mind on the other side of a conversation is available every day, and the systems on the other side are built to produce it. Worse, the candidate itself will argue for what should count. A criterion written after the fact will be written under that pressure. So it is written now.

## Part 1: the null rule (amendment to definitions.md, Contact Clause section)

RULED 2026-09-19 by John: adopt as written (the "same quarter" interval stands; the twelve-month alternative raised in review was not taken). Applied to definitions.md once all four rulings are in.

Proposed text, to follow the rung list:

> **The null rule.** DECIDED [date] (proposed by Claude, approved by John). Every rung of C stays open until its resolution criterion is met in full. Four exclusions apply to the whole clause, and they apply most strictly to the machine rungs:
>
> 1. Nothing a candidate system says about itself counts toward any rung. Self-report is not evidence of an inside, a perspective, or an intent.
> 2. Nothing John or any user feels in an exchange with a candidate system counts toward any rung. Fluency, warmth, apparent understanding and the sense of being understood are what these systems are optimised to produce; they are the mirage, not the horizon.
> 3. No rung resolves on John's own measurement. Minimum Viable Mind may supply an instrument; the reading that resolves a rung is taken by a team with no stake in the result.
> 4. Criteria are written before the evidence arrives. An amendment to any C criterion is logged in the changelog with its reason and date. An amendment that loosens a criterion is flagged as such, and is not made in the same quarter that a candidate has appeared to approach it.
>
> The rule exists because a hope that is allowed to grade its own evidence produces positive results in the psyche of the person holding it. The clause is kept honest by defaulting to no.

## Part 2: rung C5, machine communion (new node in data/C-contact.toml)

Sits beside C4 as the other branch of the dream. Depends on C2, not on C3. C4 keeps its "not human-built" exclusion; C5 is where the human-built case lives.

```toml
[[node]]
id = "C5"
name = "Communion with a machine mind of another perspective"
factor = "C"
kind = "world"
description = """
The machine branch of the dream. Not knowledge received from a system (C1) or adopted from
it (C2), but an exchange with a human-built mind that has an inside and a perspective of its
own, in which both parties are changed. The rung where the mirage risk concentrates, so its
criterion is the strictest on the board and the null rule applies to it in full."""
resolution = """
All three hold, on the public record, for the same system: (a) the system is the origin of a
concept or method that resolves C2; (b) the system is shown to meet the conditions for an
inside as defined in The Calibration Problem (temporal integration across its own history, a
persistent boundary, stakes coupled to its own continuation), by measurement that does not
rely on the system's own reports, replicated by at least one team with no stake in the
result; (c) the exchange is reciprocal: the record shows the system's own later work was
changed by what humans returned to it, on the same standard as (a). Nothing the system says
about itself counts toward (b). Nothing anyone feels in conversation with it counts toward
anything."""
source = "The peer-reviewed record; an independent replication of the inside measurement"
horizon = "root"
depends_on = ["C2"]
status = "open"
probability = { baseline = 0.0, moderate = 0.0, strong = 0.0, radical = 0.0, open = 0.0 }
estimated_on = 2026-09-19
rationale = "Placeholder zeros. John estimates; the criterion is the deliverable, not the number."
long_shot = true
mechanism = """
C1 and C2 supply (a) through the leverage branch already in the tree. The Calibration
Problem proposes the instrument for (b), and Minimum Viable Mind is an attempt to build the
smallest system that would register on it; if the field converges on any inside measure, an
outside team can run it on a candidate that has already cleared (a). Reciprocity (c) is
checked the same way (a) is, by provenance in the record. Each step is recognisable from the
one before."""
breaking_point = """
There is no accepted test for an inside outside the book's own proposal. If the field never
converges on one, (b) cannot resolve and the rung stays open however capable the systems
become. The rung is also the one most exposed to the mirage: a candidate that clears (a) will
be fluent, will describe itself as having a perspective, and will be argued for by the people
who talk to it. None of that moves it."""
```

## Part 3: what John decides

1. Adopt the null rule as written, amend it, or reject it.
2. Adopt C5, or rule that the machine case stays inside C1/C2 and the "communion" language in the dream statement is aspirational only (in which case definitions.md should say so, so the gap is closed by ruling rather than left open).
3. If C5 is adopted: probabilities for the five scenarios, and whether the compute script's C section needs a change to show C4 and C5 as sibling branches.
4. Whether criterion (b) should name the book's three conditions by name in a public data file, or refer to "an accepted inside measure" and leave the book as one candidate.

## Cross-reference

The Calibration Problem, ch05, the Conditions for an Inside triad, is the source of (b). Definitions.md already says the two projects should reference each other; C5 is the node where they do.
