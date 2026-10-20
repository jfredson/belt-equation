# The opening news post: sources and checks

The post: `site/src/content/news/2026-10-18-start-here.md`, live at https://beltequation.com/news/2026-10-18-start-here/ .
It went up on 2026-10-18 and was rewritten on 2026-10-19 under tracker pattern rule 4.19 (ruled by John
2026-10-19: a news post is a short story for a reader who has never seen the site). The rule keeps file
names, field names and sources-by-path out of the post's body, so the full fact check that used to sit
at the foot of the post lives here, and the post itself now shows a one-line list of the site's pages
it rests on (the sources line under every post, which the opener now carries too).

## The rewrite, 2026-10-19

- New title: "Will I live and work in space before I die? Where the odds stand, and what could change them"
  (was "Where the Belt Equation stands, and what to watch"). New summary, opening on the human question.
- Opens on John's wish to leave the planet and why he wants odds, not a mood; then the question; then
  how the steps are built; then the news section's purpose.
- Kept every figure as the record has it as of the post's date (the run of 2026-10-11): 0.5, 0.8 and
  9.3 percent; 1.2 and 14.8 percent on the dial; 75 and 5.9 percent for the likeliest and weakest of the
  seven links; zero, 0.9 and 0.4 percent for the first runs; 105 points; six readings; 8 November 2026;
  first quarter of 2027; December 2028; 1 November 2026; 3 January 2027.
- Left out, as detail for the record pages rather than the story: the five other link figures, the
  3.8 and 10.8 percent dial figures, the 81 and 17 step counts, the 0.14 and 0.27 point worths (the
  traffic authority is now "no other step that could happen next would move my odds as far", which is
  what being first on the Next list means), the 25 September 2026 rewording of every step (0.47 to 0.59
  percent), OpenAI's 372 mathematics result families (a side question the cold reader could not place),
  and the reactor's 20 kilowatts. Each is still on the page it was drawn from.
- **Correction.** The old post said the outside review went out "the next day" after the first run.
  The record says otherwise: the reviews were filed and all 105 rulings made on 2026-09-19, the day of the
  first run (`CHANGELOG.md`, 2026-09-19, "Step 27 RULED" and reviews 1 to 6 filed; the rulings document's
  status line), and they landed on the tree on 2026-09-20, when the headline fell to 0.4 percent. The
  rewrite says "the same day" and carries a dated one-line correction.
- "A fresh session searches" became "an automated search checks", the plain and honest description
  that names no tool; the Method page says who does what.

## Sources of the facts, re-opened 2026-10-19

Every link in the post was opened on 2026-10-19 and resolved (OpenAI's home page is no longer linked).
Figures were checked again on 2026-10-19 against https://beltequation.com/data/headline.json (computed
2026-10-11, last reading 2026-10-18, nothing moved), the home page's seven links (14, 75, 6.8, 9.7, 5.9,
21 and 9.3 percent by 2071), the Next list from the run of 2026-10-11, Wikipedia's Starship flight 15
page (launch "NET November 8, 2026") and its Space Reactor-1 Freedom page ("proposed for launch in
December 2028"). The Expanse and "at home where nobody thought people could be" and "I want to see a
solar system like that unfold": the home page, "Why the name". "40 years old": the home page, "Who is
asking". "An automated search", the weekly and monthly scope: the Radar page's introduction and
`docs/scan-procedure.md` section 0.

The fact check as the original post carried it, checked on 2026-10-18 at commit `ef80607`:

Every fact above was checked on 2026-10-18 against the page or record named here. Repository paths are on the `main` branch of [github.com/jfredson/belt-equation](https://github.com/jfredson/belt-equation) at commit `ef80607`.

- The question: the home page's description, https://beltequation.com/ (also `README.md` line 3 and `docs/definitions.md`, "The question").
- "I want to leave the planet before I die …": https://beltequation.com/ , "Who is asking".
- Settled steps scored each January: https://beltequation.com/method/ , "Scoring the forecasts".
- Headline 0.5 percent (0.00465), second number 9.3 percent, the bar (the third milestone) 0.8 percent, the four longer-life figures (0.01205, 0.03775, 0.1075, 0.1484), run date 2026-10-11: https://beltequation.com/data/headline.json . Plain names of each: https://beltequation.com/ (the dial) and `data/tiers.toml`.
- 2071 as life expectancy at about 85: https://beltequation.com/ , the dial note.
- The seven links and their figures by 2071, "the weakest link is a reason to go", "not independent dice", 81 smaller steps: https://beltequation.com/ , "Why so low".
- Five deadlines never combined: https://beltequation.com/method/ .
- What the weekly reading does and may do: https://beltequation.com/radar/ (introduction); `docs/scan-procedure.md` sections 0 and 1. Sunday evenings, Pacific time: `README.md` line 42 ("every Sunday at 18:00 Pacific"). The 17 near-term steps and the whole tree on the first reading of each month: `docs/scan-procedure.md` section 0. Annual review 2027-01-03: `README.md` line 43.
- Pages: https://beltequation.com/radar/ , /story/ , /next/ , /run/ , /method/ , /feedback/ (all opened 2026-10-18). No feed: /rss.xml and /feed.xml return 404; the planned feed is step 33 of `docs/ledger-plan.md`.
- First run zero, the world draw and the four rulings, second run 0.9 percent: `CHANGELOG.md` lines 102 to 104; `docs/runs/2026-09-19-first-run.md`.
- The outside review, 105 rulings, 0.9 to 0.4 percent on 2026-09-20 and what caused the fall: `CHANGELOG.md` lines 74 and 80; `docs/reviews/2026-09-19-rulings.md`; the brief as worded on https://beltequation.com/method/ , "Where the numbers come from".
- Function over route, 0.47 to 0.59 percent: `CHANGELOG.md` line 60; https://beltequation.com/method/ , "The thing needed, not one way of getting it".
- Starship in orbit 2026-09-28 with neither stage caught, number held: ledger entry `2026-10-04-starship-reaches-orbit-no-recovery` in `data/ledger.toml`; `data/scans/2026-10-04.toml`; https://www.space.com/space-exploration/launches-spacecraft/starship-just-reached-orbit-for-the-1st-time-whats-next-for-the-spacex-megarocket
- 372 mathematics results, none peer reviewed, the Contact Clause (the line beside the equation) unchanged and never multiplied in: ledger entry `2026-10-11-openai-math-batch-not-peer-reviewed`; `data/scans/2026-10-11.toml`; https://beltequation.com/ (the equation line).
- Near half a percent since 2026-09-20, no number moved by a reading: `README.md` lines 38 and 42.
- Flight 15 and the first ship catch attempt, "no earlier than 2026-10-19": `data/scans/2026-10-11.toml` line 58. Latest planning date, no earlier than 2026-11-08, from an air-traffic planning conference of 2026-10-08: https://en.wikipedia.org/wiki/Starship_flight_15 (opened 2026-10-18).
- The both-stages step, its test and its worth (+0.14 points by 2080): `data/L-launch.toml`; https://beltequation.com/next/
- Space traffic authority (+0.27 points, +22 percent), radiation shielding, off-Earth propellant: https://beltequation.com/next/ , the list from the run of 2026-10-11.
- Haven-1 no earlier than the first quarter of 2027: https://payloadspace.com/vast-delays-haven-1-launch-to-2027/ (cited in `data/scans/2026-09-19.toml`).
- Space Reactor-1 Freedom, more than 20 kilowatts, proposed for December 2028: https://en.wikipedia.org/wiki/Space_Reactor-1_Freedom , citing https://www.nasaspaceflight.com/2026/03/nasa-sr1-freedom-mars-2028/ (cited in `data/scans/2026-10-11.toml`).
- The whole-tree reading on 2026-11-01: the scope rule in `docs/scan-procedure.md` section 0, applied to the first Sunday of November.

## Plain reading pass, 2026-10-19

Run over the whole post after drafting (`sentient-horizons/editorial/plain-reading-pass.md`). Changes:

- "As of the run of 11 October" became "As of the last calculation, on 11 October"; "first run" and
  "second run" likewise (rule 7: "run" reads as computer jargon). Fact unchanged: the snapshot of
  2026-10-11.
- "a fixed brief" became "the same instructions for each reviewer" (rule 7). Same fact.
- "I ruled on 105 points" became "I decided each of the 105 points" (rule 7).
- "seven new requirements on the chain" became "seven new steps that now also have to go right"
  (rules 2 and 7; checked against the story entry "nine steps added, seven of them on the chain").
- "neither stage was caught" became "neither part of the rocket was recovered" (rule 7; ledger entry
  "starship-reaches-orbit-no-recovery").
- "power out there" became "a power supply out there" (rule 1: a reader took "power" as political).
- "treated every step as an independent roll of the dice" became "as if it had nothing to do with the
  others" (rule 1: a reader took the dice as the same as the seven maybes).
- "Not for a visit, but ..." and "worked out from the whole tree, not by multiplying the seven": the
  "X, not Y" pairs recast (voice protocol).
- Bracketed link labels folded into the sentence wherever the sentence allowed it (rule 1).
- Two explanations drafted from inference and not on the record were cut before review: a reason why
  the station-or-Moon-base number is higher, and an example of how the steps lean on each other (rule 8).

## Cold-reader checks, 2026-10-19

Two cold reads, each by a reader given only the rendered text and asked to read as John's father: an
intelligent retired man in his seventies, new to the site, not a space or statistics enthusiast.

First read, of the first draft. Stops: stray link labels; how "industry" and "me" fit together; "the
tree" unexplained; "run"; the three numbers and why the station number is larger; 9.3 percent appearing
twice; 2071 against 2080; "percentage points"; too many counts (7, 81, 17); who reads the news; "two
independent records"; "a fixed brief"; tree against chain; the OpenAI paragraph; "catch" the rocket;
20 kilowatts. Missing: why he wants space. Cut: how the readings work, the OpenAI paragraph, the
two plans, the dial's four figures. Acted on: all of it, except that the how-it-works paragraph and the
two plans were kept shorter (the first is why a reader can trust the number; the second answers John's
own linking ruling), and the correction stays because a dated correction is owed.

Second read, of the revised draft. Understood: the son's real odds, half a percent, why so low, what
news could raise them; the personal why came through. Stops: industry on Mars (the question's own
words, kept); "decided"; "power out there"; who does the checking; dice against maybes; "If medicine
gives me that extra decade, it would raise my odds by about a fifth" (the worst stop: unclear "it", and
a fifth set against the dial's doubling); the next reading two weeks away when readings are weekly;
stray link labels. Acted on: each of these, with the wording above, and a line for the stranger in the
opening ("the same calculation runs for your birth year").
