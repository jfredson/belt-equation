# The Hera arrival post: sources and checks

The post: `site/src/content/news/2026-11-14-hera-arrives-at-the-asteroid-nasa-struck.md`, the site's first
mission news post about a mission reaching its target, written to the Euclid model
(`docs/website-plan.md`, Missions). Drafted 2026-11-14 by Claude at John's word ("Yes, draft it"), relayed
by the master session of 2026-11-14. Not yet published: merging it to `main` deploys it.

## Why it is three days late

Hera arrived on 2026-11-11. The roadmap step for this post (TimeAssembler task "First mission news post:
Hera arrives at its asteroids") waited on a day that ESA's mission page never gave; a check on 2026-11-14
found ESA's release of 2026-11-11. The post is dated the day it was written, inside the news check's
fourteen-day window for the arrival milestone.

## The odds

Nothing in the post is about the odds, under John's ruling of 2026-11-09 (mission news and discovery
posts stick to the news, and mention the odds only where the event bears on a step). The task's own note,
written before that ruling, asked for an ending on the odds; the later ruling governs.

**Does any step or estimate change under its own written test? No.** Checked 2026-11-14:

- Hera's record already says no step turns on it (`step_note`): it tests defending Earth from asteroids,
  not going out to them.
- `D-fast-transit-in-routine-use` (three missions in one year reach the asteroid belt within twelve months)
  needs arrivals at bodies at least 2.1 astronomical units from the Sun, within twelve months of leaving
  Earth orbit, three in one calendar year. Didymos is a near-Earth asteroid, Hera took about two years
  (launched 2024-10-07, arrived 2026-11-11), and it is one mission. Not met, and no evidence for it.
- `L-asteroid-material-delivered-to-orbit-at-scale` (a hundred tonnes of asteroid material to orbit in a
  year): Hera returns no material. Untouched.
- The crewed beyond-the-Moon step (`D-drive.toml`, the widened Mars step): Hera carries no crew. Untouched.

No change is proposed.

## Title

Three candidates, each run through the title rules (`sentient-horizons/editorial/title-rules.md`, read from
that repository's `main` on 2026-11-14; the main checkout there sits on another branch without the file):

| Candidate | Rule 1 (a stranger can tell) | Rule 2 (names the subject) | Rule 3 (no coinage) | Rule 4 (a claim, not a label) | Note |
|---|---|---|---|---|---|
| **"Four years after NASA struck an asteroid on purpose, ESA's Hera spacecraft has arrived to see what changed"** (in the file) | yes | Hera, ESA, NASA | yes | yes | Longest; says why anyone cares without a single unexplained name. Recommended. |
| "ESA's Hera spacecraft has reached the asteroid that NASA's DART struck in 2022" | mostly | yes | yes | yes | Shorter, but "DART" is an acronym a stranger may not know. |
| "Hera arrives at Didymos and Dimorphos, the asteroid pair NASA struck in 2022" | partly | names the asteroids | yes | yes | The asteroids' names mean nothing to most readers; weakest on rule 1. |

Rules 5 and 6 do not apply. Rule 7 (write the title last, from the Reddit title): there is no Reddit title
yet. The file name follows the chosen title; it changes freely until publishing.

## Facts, each against its source (opened 2026-11-14)

- ESA's release of 2026-11-11, read in full
  (https://www.esa.int/articles/about-us/directorates/operations/space-safety/hera/hera-spacecraft-in-rectangular-orbit-around-target-asteroids):
  Hera "has arrived at its target asteroids"; 30 to 25 km from the pair; "early characterisation phase";
  Michael Kueppers, mission scientist, and his quotation; Didymos 780 m across with gravity about 40,000
  times weaker than Earth's, Dimorphos 151 m and about 200,000 times weaker; no ordinary circular orbit;
  12 cm/s, "about as fast as a rapidly-crawling insect"; thruster firings that turn the path 90 degrees on a
  cycle of three days then four, giving "rectangular orbits"; a failed firing leaves it drifting away; next
  month, a closer phase from around 20 km; controlled from Darmstadt, about eight hours a day, across 196.5
  million km, through four 35-metre antennas in Argentina, Spain and Australia; DART, 26 September 2022,
  580 kg, 6.1 km/s, a plume across 10,000 km, the orbit changed by around 33 minutes; the open questions
  (crater or reshaping, makeup, structure and mass, why the push was larger than predicted); two
  shoebox-sized satellites, "eventually progressing to landing". The release does not itself give the
  arrival day; its publication date is 2026-11-11.
- ESA's picture release of 2026-11-12
  (https://www.esa.int/articles/about-us/directorates/operations/space-safety/hera/hera-spies-a-half-hidden-asteroid-moonlet):
  the picture from 56 km; boulders, smoother regions and a sharp ridge at the equator; Didymos turns every
  2.2 hours, near to coming apart; models suggest material flows toward the equator and may be thrown off,
  "potentially accounting for" Dimorphos; Dimorphos mostly hidden; "Detailed images of both asteroids will
  be unveiled on 25 November."
- Sky & Telescope's report of 2026-11-13 by Emily Lakdawalla
  (https://skyandtelescope.org/astronomy-news/spacecraft-investigates-asteroid-after-impact/): "Hera
  rendezvoused with the Didymos-Dimorphos pair on November 11th"; ESA is saving the reveal of Dimorphos
  "for a special event to be held in Berlin, Germany, on November 25th"; 25 to 30 km; the early phase lasts
  two rectangular cycles, "until December 2nd", then 8 to 20 km. Both facts the brief asked to confirm are
  on the page.
- ESA's page for the Hera mission
  (https://www.esa.int/missions/about-us/directorates/operations/space-safety/hera), opened 2026-11-14:
  "Launch: 7 October 2024". The post cites this page for the launch date, in place of Wikipedia.
- Wikipedia's article on Hera (https://en.wikipedia.org/wiki/Hera_(space_mission)): launch 7 October 2024
  (matches ESA); the second braking burn "later in October 2026", 2,300 km from Didymos, 70 m/s (used only in the
  Missions record, not the post).

## Left out, with the reason

- "A quartet of 35-m-diameter" antennas: the post says "large dish antennas", since the count adds nothing.
- ESA's note that the flying pattern comes from its Rosetta comet mission: it would need its own name and
  link for one clause.
- Wikipedia's 6.6 km/s for DART's speed: the post uses ESA's 6.1 km/s, from the release it cites. The two
  differ; ESA is the operator's figure.
- ESA's "Hera Space Companion" chatbot, at the foot of both releases: not news.
- No picture: no image licence was checked in this session. ESA's pictures usually carry a Creative
  Commons licence, as Euclid's did; adding one is a small follow-up if John wants it.

## Link what you name

Opened 2026-11-14 and answering: the European Space Agency (https://www.esa.int/); Hera (ESA's mission
page; the old address https://www.esa.int/Space_Safety/Hera now forwards to
https://www.esa.int/missions/about-us/directorates/operations/space-safety/hera, and the post links the new
one); NASA's DART (https://science.nasa.gov/mission/dart/); Dimorphos
(https://en.wikipedia.org/wiki/Dimorphos) and Didymos (https://en.wikipedia.org/wiki/65803_Didymos), which
have no official pages of their own; Sky & Telescope and ESA's releases, linked at the reports. Not
linked: NASA itself at its one mention (the DART link carries it); Michael Kueppers, for whom no page was
looked for, named with his role; Darmstadt, Berlin and the three countries, as places.

## Missions page (`data/missions.toml`)

- The file's `checked` date and Hera's moved to 2026-11-14. Pull request 78 (the Starship Flight 15
  update), which also edits this file, was merged to `main` while this draft was being written; this
  branch was rebased onto it and the checks re-run, so no merge order remains.
- Second braking burn: marked done, dated to the month (October 2026), since Wikipedia gives no day; note
  added.
- Arrival: marked done on 2026-11-11, with ESA's release and Sky & Telescope as sources and a note on the
  orbit and the next phase.
- New milestone, announced by ESA: the first detailed pictures of Dimorphos on 2026-11-25, in Berlin.
- The "why I follow it" line is untouched (still John's to rewrite).

## Checks run, 2026-11-14

`python3 scripts/missions.py` OK (16 missions, 65 milestones; one note, the Starship Flight 15 milestone,
which pull request 78 handles); `python3 scripts/export.py` OK; `python3 scripts/check_news.py` OK (5
posts); `python3 -m unittest scripts/test_news.py` OK; `npm run build` in `site/` OK (107 pages);
`python3 scripts/check_site.py` OK.

## Fixes after review, 2026-11-14 (John: "Yes, send them"; the title stays)

1. Launch date: now sourced to ESA's own Hera page, which gives "Launch: 7 October 2024". Wikipedia is no
   longer a source of the post.
2. The open question about the size of the push: ESA's release asks "which properties explain a deflection
   so much greater than impact simulations predicted?", meaning which of Dimorphos's own properties
   explain it. The post said only "why the push was so much larger than computer models had predicted",
   which was broader. It now reads "which of its properties explain why the push was so much larger than
   computer simulations of the impact had predicted".
3. The distance from Earth: ESA's release, published on the day of arrival, gives 196.5 million km. The
   post now says "across a gap that was 196.5 million kilometres on the day it arrived".
4. "What to watch for" no longer opens "The first is ..."; it opens "First comes the picture of Dimorphos".
5. Added to "Why it matters", in John's voice: "I follow Hera because holding a spacecraft steady beside a
   body with almost no gravity is the same skill that any work at an asteroid will need." No claim about
   the odds or any estimate.

The branch was then rebased onto `origin/main` (pull requests 79, 81 and 82 merged that day). Only the
changelog conflicted; main's lines were kept and this post's two lines re-applied beneath them, with "for
John's go" changed to "not yet published" to match pull request 81's rule that changelog lines say what
was decided, not who ruled. `data/missions.toml` merged without conflict. The checks below were re-run
after the fixes.

## Still to do before publishing

- John's read, and his choice of title.
- The Voice Calibration and Cold Reader passes were not run as full passes; the draft was written to the
  plain-language rule and checked for em dashes (none in prose) and a link beside every figure.
- The share kit and the outreach task that every news post gets.
- After 2026-11-25: a follow-up post or an added section on the pictures of Dimorphos, and the milestone
  marked done.

## Voice Calibration and Cold Reader passes, after publishing (2026-11-14)

John published the post on 2026-11-14 (pull request 80) and asked for both passes ("Yes, do both").
Changes are on the branch `claude/hera-voice-cold-read-2026-11-14`. The title and address are unchanged,
because the post is public. The site's practice for correcting a published post is a dated line in
italics (the opening post's "*Corrected October 19th, 2026:*"; the Starship post's "*Updated ...*"). One
was drafted, then left off on John's word (see below).

**How the passes were run.** Voice Calibration: the master in `calibration-problem/editorial/`
(version 2026-10-18, with Pattern 28 of 2026-10-21), passes 0 to 3 and the final check, read from that
repository's `main`. Pass 4 (texture) is for essays only and was skipped. Cold Reader
(`calibration-problem/editorial/cold-reader-protocol.md`): one reader working in a separate session, given
only the rendered text, read it in both of the protocol's lenses: the skeptic with ninety seconds, and the
uninformed reader modelled on John's father. No paid or outside service was used.

**Voice Calibration findings.**

- Substance gate (every claim checked again against ESA's two releases and Sky & Telescope):
  - The opening called the asteroids "the pair that NASA struck". NASA struck one of them, so this was
    stronger than the source. Fixed: "a pair that includes the one NASA struck".
  - "Hera cannot settle into an ordinary circular orbit". ESA says such an orbit is "impractical".
    Fixed: "ESA calls an ordinary circular orbit around them impractical".
  - "not yet a method anyone can rely on". ESA's wording is that the method is not yet "a
    well-understood planetary defence technique". Fixed: "not yet understood well enough to rely on".
  - "which will show what the impact did to it" (the 25 November picture). Sky & Telescope says the
    picture shows what Dimorphos "looks like now, post-smash". Fixed: "the first clear view of it since
    the impact".
  - John's sentence said "holding a spacecraft steady beside" the asteroids. The post's own flying
    section has Hera drifting and turning corners 25 to 30 kilometres away, so "steady" and "beside"
    were both wrong. It also said "the same skill that any work at an asteroid will need", which claimed
    too much. See below.
- Pass 1, vocabulary: no flagged words. Pattern 27 (first mentions): every name is introduced. DART is
  never spelled out, but the sentence says what it did, so it was left alone.
- Pass 2, patterns: every sentence has a main verb. No em dashes in prose; the en dash inside Kueppers's
  quotation is his and stays. There is one contrast ("drifting away from them, not into them"), which
  carries the point. Pattern 28 (missing connecting words): two cases, both also found by the cold
  reader. The two gravity figures did not say which asteroid each belonged to. The safety sentence did
  not say why a failed firing leaves Hera drifting away; ESA's release gives the reason (each firing
  comes while it is moving away), and the post now says so.
- Pass 3 and the final check: the opening states the news, and the ending looks ahead without summing up.

**Cold Reader findings** (the reader's points are marked here as faults or taste).

- Ninety-second test: attention dipped at the figures in "What happened" (mass, speed, minutes, plume),
  because none of them had a scale. Fixed by giving the orbit time: Dimorphos takes about 12 hours to go
  around Didymos (Sky & Telescope). The point that the push was far larger than the simulations
  predicted now sits beside the 33 minutes, so it no longer first appears at the end (ESA's release).
- Uninformed reader, faults fixed: which gravity figure goes with which asteroid; why a failed firing is
  safe; "flowing toward its middle", which read as the asteroid's centre and now reads "toward its
  equator, where the ridge is".
- Uninformed reader, left as they are:
  - Why weak gravity rules out an ordinary orbit. ESA gives no reason, so the post now just reports
    ESA's word "impractical" and adds no reason of its own.
  - "which could be how Dimorphos came to exist": the step from material thrown off to a moon is left
    to ESA's own wording.
  - 196.5 million kilometres has no scale; the reader called that taste.
  - Which event in Berlin, and a landing on which asteroid: neither source says.
  - DART is not spelled out.
- Genre pattern-match: the post does not read as machine-written. Every figure is credited, and the
  quotation admits the forecasts may all be wrong. The reader's one doubt was John's sentence.
- John's sentence: the reader could not tell who "I" was, since nothing in the post says so. The
  sentence also came from nowhere, straight after a paragraph about protecting Earth, and it overclaimed
  in the ways listed above.

**John's sentence, rewritten for his read.** It now ends the flying section, where the skill it names
has just been described, and it says who is speaking:

> On this site I keep track of whether I will live and work in space before I die. I follow Hera
> because flying safely near a body with almost no gravity, as it is doing now, is one of the skills
> that any work at an asteroid will need.

It makes no claim about the odds or an estimate, and it does not write the site as if it acts. It speaks
for John, so it is his to keep, change or cut.

**Checks re-run:** `scripts/missions.py`, `scripts/export.py`, `scripts/check_news.py`, the full test
suite, the site build and `scripts/check_site.py`.

**John's four changes, 2026-11-14 ("Yes, all four"), relayed by the master session:**

1. John's sentence now reads only: "I follow Hera because flying safely near a body with almost no
   gravity is one of the skills that any work at an asteroid will need." Two things were cut: the
   sentence before it ("On this site I keep track of whether I will live and work in space before I
   die."), because John ruled today that tracker news never leans on "before I die" and that a news post
   can stick to the news; and "as it is doing now".
2. The dated correction line is left off the page, on John's word, because the post had not yet been
   shared anywhere; he dropped the same kind of note from an essay today for the same reason. The
   changelog line stays.
3. The 25 November picture now reads "the first detailed pictures of Dimorphos", which matches the post's
   summary. ESA's picture release says "Detailed images of both asteroids will be unveiled on 25
   November"; it does not say "first clear view since the impact", so that phrase went.
4. "The change was far larger than computer simulations of the impact had predicted" is cut from "What
   happened", because "Why it matters" already says it. The 12-hour orbit stays there for scale.

