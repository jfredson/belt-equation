# External forecaster baseline: GPT-6 Astra, 2026-09-19

Status: external row for comparison, not adopted priors. Elicited via the ChatGPT desktop app, single message, no documents shown, no lookup allowed, conditional on no civilization-ending catastrophe. Astra flagged the seven items as strongly correlated, so these marginals must not be multiplied.

## Prompt

> Without looking anything up, give your probability that each of the following holds by 2070, by 2080, and by 2095, with a one-paragraph plausibility chain for each. Assume no civilization-ending catastrophe. (1) Launch cost to low Earth orbit under $100 per kilogram. (2) A drive enabling Earth-to-asteroid-belt transit under 90 days for crewed vehicles. (3) Off-world power generation exceeding 1 gigawatt continuous. (4) Demonstrated healthy human gestation and childhood development in partial gravity, whether planetary or rotating habitat. (5) A self-sustaining commercial reason for more than 10,000 people to live off Earth. (6) A stable legal regime under which private persons can hold and transfer off-world property or residency. (7) A person born in 1986 alive and fit for spaceflight. Give the numbers as a table first, then the chains.

## Table

| # | Milestone | Factor | 2070 | 2080 | 2095 |
|---|---|---|---:|---:|---:|
| 1 | Launch to LEO under $100/kg (2026 USD) | L | 75% | 85% | 92% |
| 2 | Crewed Earth to main belt under 90 days | D | 50% | 65% | 80% |
| 3 | Off-world power over 1 GW continuous | E | 65% | 80% | 90% |
| 4 | Healthy gestation and childhood in partial gravity | B | 30% | 45% | 65% |
| 5 | Commercial reason for over 10,000 off-world residents | M | 30% | 45% | 65% |
| 6 | Stable transferable off-world property or residency rights | R | 70% | 82% | 92% |
| 7 | Person born 1986 alive and fit for spaceflight (COHORT reading, see note) | W (not usable) | 98% | 90% | 55% |

## Astra's operational definitions (matter for later scoring)

1. Launch: an actual repeatable commercial price for payload delivered to LEO, not propellant cost or aspirational marginal cost. Binding constraint is demand volume and competition, not physics.
2. Belt transit: a useful crewed vehicle from Earth's vicinity to a main-belt destination including arrival braking, in a favorable window; not every asteroid on that schedule. Nuclear thermal or high-power electric suffice; fusion is a possible route, not a prerequisite. Uncertainty is mostly whether demand funds and qualifies the vehicle.
3. Power: aggregate electrical generation outside the atmosphere, sustained around the clock (storage, distributed generation, or reactors); excludes intercepted sunlight and peak bursts. Can be met by automated facilities with no large population.
4. Biology: conception through birth and development into adolescence in a specified partial-gravity environment, multiple children, convincing health assessments. Rotating habitats raise the odds because gravity is selectable; lunar or Martian gravity specifically would score lower.
5. Economics: population supported by paying customers, not indefinite subsidy. Notes a large space economy could stay overwhelmingly robotic; the likely path combines productive activity with people paying to live off Earth.
6. Regime: enforceable, transferable ownership of facilities or long-duration occupancy rights; universal recognition of planetary territory is a stricter test. Expects limited-but-durable arrangements among major jurisdictions before any universal treaty.
7. Window: read as at least one person from the 1986 birth cohort, medically capable of a gentle orbital flight with ordinary assistance. Not the individual question the Belt Equation asks.

## Action items

- Re-ask item 7 as "a specific, currently healthy person born January 1986" and log separately. The cohort figure is not a W input.
- The A (access) branch was not asked and should not be put to an outside model before May 2027.
- Use this row as the first entry in an external-forecaster column when the v0 tree is scored; compare per factor, not on a headline product.

## Provenance

Model: GPT-6 Astra (ChatGPT desktop app, standard chat). Date: 2026-09-19. Elicited by John Fredrickson; filed by Claude (Cowork) the same day.
