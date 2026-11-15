# The Starship Flight 15 post: sources and checks

The post: `site/src/content/news/2026-11-13-starship-flight-15-reaches-orbit-booster-catch-called-off.md`,
a mission news post written to the Euclid model, drafted 2026-11-13 by Claude at John's request, about
three hours after liftoff. Not yet published: merging it to `main` deploys it. It sits on the local
branch `draft/starship-flight-15-2026-11-13`, which is not pushed.

## The flight was not over when this was written

The upper stage was still in orbit at the time of writing (about 5:50 p.m. Pacific, 2026-11-13). Its catch
attempt is due about 3:17 p.m. Texas time on 2026-11-14 (1:17 p.m. Pacific). Before the post goes up,
either the post is updated with the outcome, or it goes up as a launch-day post and a second post or an
added section covers the catch. That is John's call. The post's first sentence says "as I write", which
must go once the flight has ended.

`data/missions.toml` is not changed. The Flight 15 milestone still reads `plan`; the next reading marks
it once the upper stage's outcome is known (launch done, booster catch failed, ship catch done or failed).
The news check passes on the milestone's move of 2026-11-05.

## Title

"Starship's fifteenth flight reaches orbit, but SpaceX calls off the booster catch". Claude's draft, not
John's. It names the subject and makes a plain claim, and says only what the sources say. Not yet run
against `title-rules.md`, which was not at `sentient-horizons/editorial/` when this session looked. No
Reddit title.

## Facts, each against its source (opened 2026-11-13)

- SpaceX's page for the flight (https://www.spacex.com/launches/starship-flight-15, opened in a browser;
  still the pre-launch text): first flight planned to return both the booster and the upper stage to the
  launch site for catch; "the first full recovery of an orbital launch system"; an orbit of about 275 km,
  about 14 orbits, more than 22 hours; 26 Starlink V3 satellites, three with cameras to scan the heat
  shield; first catch attempt for a version 3 booster; three version 1 boosters caught, two flown again;
  return to launch site only if the systems for reentry, landing burn and tower approach are healthy.
- Space.com's launch report by Josh Dinner
  (https://www.space.com/space-exploration/launches-spacecraft/spacex-starship-flight-15-chopsticks-double-catch-super-heavy-ship,
  updated 7:10 p.m. Eastern): liftoff 4:47 p.m. Texas time; stage separation about 2.5 minutes in; catch
  called off, "controlled splashdown in the Gulf of Mexico about 6.5 minutes after launch, for reasons
  that were not immediately clear"; orbit at about 275 km after a burn at 26 minutes 10 seconds; second
  time in orbit, the first being Flight 14 on 28 September; 26 satellites released over 42 minutes from
  35 minutes; early-return points at about 10 minutes after deployment, 7 hours 15 minutes and 20 hours
  41 minutes; a fallback splashdown zone in the Gulf; catch at about 3:17 p.m. Texas time on Saturday.
- Space.com's live updates
  (https://www.space.com/news/live/spacex-starship-flight-15-live-updates-nov-13-2026-starship-first-double-landing-attempt,
  latest entry read 2026-11-14 01:30 UTC): Dan Huot's words on the abort; the first early-return option
  passed over; Huot, "this is now going to be the longest Starship mission we've ever flown".
- CNBC's report by Lora Kolodny
  (https://www.cnbc.com/2026/11/13/spacex-launches-starship-in-key-test-flight-of-massive-rocket.html):
  FAA authorisation "earlier on Friday"; the booster diverted "to splash into the Gulf of Mexico, where
  it burst into flames". The post gives the flames as CNBC's report.

## Left out, with the reason

- Wikipedia's article on the flight says the booster's flight termination system was set off after
  engine shutdown and it broke apart. The sentence carries no citation, so it is not in the post.
- CNBC's headline summary says the booster was "exploding"; Space.com says "controlled splashdown". The
  post says only where it came down, and gives the flames as CNBC's.
- The nationwide FAA ground stop of the same afternoon: no source ties it to the flight.
- The vehicle numbers (Booster 22, Ship 42), the tile fitted by a YouTube personality, and Musk's
  launch-rate targets: not needed for the news.
- SpaceNews's report is behind a registration wall past its first sentence, so it is not cited.
- No picture: no image with a checked licence was found in this session.

## Link what you name

Opened 2026-11-13 and answering: SpaceX (https://www.spacex.com/), Starship
(https://www.spacex.com/vehicles/starship/), Starbase (Wikipedia, https://en.wikipedia.org/wiki/SpaceX_Starbase,
since SpaceX has no page for the site that could be found), the Federal Aviation Administration
(https://www.faa.gov/), Flight 14 (Wikipedia, https://en.wikipedia.org/wiki/Starship_flight_14), Starlink
(https://www.starlink.com/), NASA's Artemis programme (https://www.nasa.gov/humans-in-space/artemis/).
Not linked: Dan Huot, who has no page of his own that was looked for; he is named with his company.
CNBC and Space.com are linked at the reports themselves.

## Still to do before publishing

- The outcome of the upper stage's return, and SpaceX's reason for the booster abort if given.
- John's voice pass. The full Voice Calibration and Cold Reader passes were not run in this session; the
  draft was only checked for em dashes and for a link beside every figure (`scripts/check_news.py`: OK).
- The sentence "would cost far less per flight than one that is thrown away" is a plain statement of why
  reuse matters and carries no source; cut it or source it.
- The share kit and the outreach task that every news post gets.

## Published 2026-11-13 (John: "Publish tonight")

John chose to publish on launch night as a launch-day post, with the flight still under way. Before
publishing, Space.com's live updates were read again (about 5:57 p.m. Pacific): no change, the upper stage
still coasting. Three edits were made: the opening now says the upper stage "was still flying that
evening"; the unsourced sentence on the cost of reuse was cut; and "No one has caught an upper stage"
became "No Starship upper stage has yet been recovered", which is what Space.com's report supports. The
Voice Calibration and Cold Reader passes, the title-rules check and the share kit are still not done. The
upper stage's outcome on 2026-11-14 goes in a follow-up post or an added section, and in
`data/missions.toml`.

## Updated 2026-11-14, after the upper stage came back (on a branch, not published)

Asked for by John's master session of 2026-11-14, following the reminder John asked for on 2026-11-13.
The update is on the branch `claude/starship-flight-15-return-2026-11-14` in a pull request; merging it
publishes it, and that is John's.

What the sources say (each opened 2026-11-14, about 2:40 p.m. Pacific):

- Space.com's live updates (https://www.space.com/news/live/spacex-starship-flight-15-live-updates-nov-14-2026-starship-first-double-landing-attempt; the page's address now ends "nov-14", and the old address forwards to
  it): entry of 21:31 UTC, "SpaceX caught the Starship upper stage today (Nov. 14) for the first time
  ever", at "about 4:20 p.m. EST (2120 GMT)", 22.5 hours after launch; Dan Huot, "We caught a Starship,
  and now everything changes." Entry of 20:42 UTC, Kate Tice: "Early indications are that the booster
  ended its boostback [burn] early due to a low fuel mass alarm", the cause still being investigated,
  and the booster's guidance "correctly aborted itself from the tower catch and went for an offshore
  water divert". Entry of 20:29 UTC: a 10-second, single-engine deorbit burn. Entry of 19:28 UTC: the
  final early-return check passed. Entry of 13:00 UTC: the second early-return check passed; Huot on the
  heat shield being "in a good posture for a reentry".
- CNBC's report by Lora Kolodny (https://www.cnbc.com/2026/11/14/spacex-plans-to-try-first-ever-catch-of-starship-rocket-from-orbit.html, published 4:14 p.m. Eastern): SpaceX "successfully caught the
  upper stage"; it "flew around the Earth 14 times"; the booster was diverted "to an offshore splashdown
  in the Gulf of Mexico where it exploded before hitting the water".
- SpaceX's own page for the flight still carried its pre-launch text when opened, so the outcome rests
  on Space.com and CNBC, and on SpaceX's broadcast as Space.com quotes it.

Changes to the post: the summary, the opening and the booster paragraphs are rewritten; "What comes
next" becomes "The catch"; "Why it matters" and "What to watch for" are rewritten; an "Updated" line
is added under the title. CNBC's first report said the booster "burst into flames" in the Gulf; its
second says it exploded before reaching the water, and the post now gives the second. Space.com's live
updates also say the booster's flight termination system was set off; the post does not say so, since
the line is a picture caption and not a SpaceX statement.

Not verified: whether SpaceX says the caught upper stage can fly again (no source read says either
way; the post says so); the exact minute of the catch (Space.com gives "about 4:20 p.m. EST" in one
entry and a plan of 4:16 in others; the post says "about 3:20 in the afternoon, Texas time").

The title is unchanged, because a published title is John's to change. It now covers only half the
story. A suggestion for him: "SpaceX catches a Starship upper stage for the first time, a day after
losing the booster". The post's address would stay as it is.

The record: `data/missions.toml` now marks the Flight 15 milestone done, with what happened to each
part. Nothing in the tree changes in this pull request. The step this flight bears on, "A heavy launcher
recovers both of its stages intact from one orbital flight", asks for both parts from a single flight,
retrieved and confirmed fit to fly again; the booster was lost, so the step is not met and no number
moves. Proposed, not applied: a held-steady ledger entry for this flight, like the one written for
Flight 14, at Sunday's scan.

Still owed: the title-rules check, the Voice Calibration and Cold Reader passes, and a picture.

## Title changed 2026-11-14 (on a branch, for the master session to merge)

John's words, as his master session passed them on: "merge 78 with the new title". Pull request 78 had
already been merged and published at John's "Merge and publish" earlier the same afternoon, so the
title change is its own pull request. The title goes from "Starship's fifteenth flight reaches orbit, but SpaceX calls off the booster catch" to "SpaceX catches a Starship upper stage for the first time, a day after losing the booster". The post's address and
file name stay as they are: the post is public at that address, and the site takes the address from the
file name, not from the title.

Against the title rules (`sentient-horizons/editorial/title-rules.md`, read 2026-11-14 on that
repository's main line; it was not in the checked-out branch on launch night): rule 1, a stranger can
say what the post is about from the title alone; rule 2, it names SpaceX and Starship; rule 3, no coined
phrase; rule 4, a plain claim; rule 5 does not apply; rule 6 does not apply; rule 7, the Reddit title in
the share kit says the same and more. No attention device. One thing the rules say that this goes
against: "After publishing, the title and the address stay." This is a change to a published title, made
on John's word the day after publishing, like the two exceptions the rules record; unlike them, the
address is kept. Every claim in the title is in the post with its source: the catch and that it is the
first (Space.com's live updates, CNBC), and the booster lost the day before (Space.com, CNBC).

## Rewritten 2026-11-14 as an essay (branch `claude/flight-15-essay-2026-11-14`, not merged)

Asked for by John's brief of 2026-11-14 (drafted in his planning chat): rewrite the post from scratch so
that it leads with why the upper stage's catch matters, carries the cost argument and the chain up the
tree, connects to the Quiet Galaxy, states the caveats, keeps the flight to one short section, and ends
on what to watch. It is also meant to stand alone for a Sentient Horizons newsletter reader. Nothing is
merged, deployed or sent. The address is unchanged.

### The approach, reviewed before writing

- **Reversing the proportions is right**, and it fits the Frontier Dispatch rule in
  `sentient-horizons/editorial/content-strategy.md` ("a dispatch that reads as mission recap or roadmap
  cheerleading has failed").
- **One correction to the brief's framing, built into the essay.** The brief says the launch-cost link is
  the one every later link depends on. In the tree that is true of every rung of the outcome ladder:
  Tier 1 needs `M-hundred-people-working-off-earth-for-pay`, which depends on the hundred-flight year,
  and every tier from Tier 2 up requires the $200-a-kilogram step. But the published essay *The Belt
  Equation* says launch is "the healthy part of the chain" and that the Belt "is gated by whether anyone
  ever makes money out there more than by rockets". To stay coherent with it, the essay says launch holds
  up the ladder and is one of the healthiest links, and names the tightest link (something made off Earth
  sold at a profit, about 6 percent by 2071). It does not say the biology steps depend on launch, because
  they do not.
- **Fit with the news section.** The post stays `kind: mission-news`, which `scripts/check_news.py`
  accepts, and the Starship milestone is still marked within fourteen days. At about 2,150 words it is far
  longer than the other posts. The Quiet Galaxy section reaches beyond a Belt news post; it is kept
  because the brief asks for it and because it is what makes the piece newsletter material. If John wants
  the Belt post shorter, that section is the one to move into the Sentient Horizons copy only.
- **"Two Silences" does not exist.** No file, branch or commit in `sentient-horizons`, `quiet-galaxy`,
  `calibration-problem` or anywhere under `~/Code` carries that title, and the live Sentient Horizons
  feed and the Quiet Galaxy site have no such piece (searched 2026-11-14). The Quiet Galaxy connection is
  drawn instead from *The Quiet Galaxy Hypothesis*, the corpus ledger's position 25 ("the Great Filter
  reframes as a threshold from reach to restraint") and three of the Quiet Galaxy's explanation records:
  `interstellar-travel-impractical`, `expansion-stalls` and `inward-turn`, each quoted from its own
  `would_strengthen` or `would_weaken` line. If "Two Silences" is a working title for something not yet
  written, John can say which.
- **Other trackers left out.** The AGI Zeitgeist, The Upgrade Tree and Outrunning Ageing have no direct
  link to a rocket catch, so none is named.

### The newsletter: the post cannot go out as it is

The Sentient Horizons newsletter (`sentient-horizons/ops/newsletter/README.md`) is one Buttondown issue
per Sentient Horizons essay, and the draft makes itself only when an essay's status becomes `published`
on that repository's `master`. A tracker news post has no route into it. So sharing this piece means a
Sentient Horizons copy, published as a Frontier Dispatch, the way the AGI Zeitgeist dispatch of
2026-10-24 was. The copy can carry the same text with three changes: drop the "Rewritten" note at the
top, say in the first lines that the Belt Equation is John's tracker and link it (already done in the
body), and pass the featured-image gate (`ops/protocols.md`: no `published` status without the woodcut
banner, which John generates and approves). The other route, a hand-made Buttondown issue that links to
the Belt post, breaks the one-issue-per-essay format and is not recommended. Nothing in
`sentient-horizons` was changed in this session.

### Title and address

- **Title** changed to "Why SpaceX catching Starship's upper stage matters for everything beyond Earth".
  It follows `title-rules.md` (names the subject, says the question the piece answers, no coined phrase).
  This replaces John's own retitle of earlier today ("SpaceX catches a Starship upper stage for the first
  time, a day after losing the booster", pull request #79), so it is his call; the old title is the
  alternative and would still be accurate, though it describes the flight more than the essay.
- **Address kept**: `/news/2026-11-13-starship-flight-15-reaches-orbit-booster-catch-called-off/`. The
  post has been live since launch night and its address may have been shared. The slug describes the
  first version, but readers rarely read an address, and keeping it needs no redirect. If John wants an
  address that matches, the title-rules exceptions of 2026-10-24 and 2026-10-25 are the precedent: a new
  file name and a permanent (301) redirect from the old address.

### Dates

The brief's example was "November 14, 2026". The site and John's ruling of 2026-10-21 spell dates in
public prose as "November 14th, 2026", and the earlier version of this post did the same, so the essay
keeps the house form. One find-and-replace changes it if John meant the brief literally.

### Facts and their sources (each opened 2026-11-14)

- **Launch, pad, vehicles.** Wikipedia's article on the flight (https://en.wikipedia.org/wiki/Starship_flight_15):
  liftoff "November 13, 2026, 22:47:36 UTC (4:47:36 pm CST)", "from Orbital Launch Pad 2 at Starbase",
  "The mission used Booster 22 and Ship 42". The essay gives 4:47 p.m. Texas time and links Wikipedia;
  the universal time is left out of the prose because one time is enough for a reader.
- **Booster abort and loss.** Space.com's launch report (Josh Dinner, link above): catch called off about
  6.5 minutes after launch. Space.com's live updates (entry of 20:42 UTC, 2026-11-14): Kate Tice, "low fuel
  mass alarm". CBS News (William Harwood, https://www.cbsnews.com/news/spacex-catch-starship-rocket/,
  updated 2026-11-14 6:06 p.m. Eastern): it "ran out of fuel and exploded moments before hitting the water";
  "the first such recovery of a Starship from orbit"; Dan Huot, "We caught a Starship, and now everything
  changes"; Musk on early ships and boosters being "already outdated by improved designs in production or
  on the test stand".
- **Ship.** CNBC (Lora Kolodny, 2026-11-14): 26 Starlink V3 satellites; "flew around the Earth 14 times".
  Wikipedia: caught "November 14, 2026, 21:20:03 UTC (3:20:03 pm CST)", 22 hours 32 minutes after liftoff.
  Space.com's live updates: "about 4:20 p.m. EST", a single-engine deorbit burn of about ten seconds.
- **Shotwell and Musk, 2026-10-20.** The Motley Fool's transcript of SpaceX's third-quarter earnings call
  (https://www.fool.com/earnings/call-transcripts/2026/10/20/spacex-spcx-q3-2026-earnings-call-transcript/):
  Shotwell, "refly the second stage by early next year" and "We'll attempt an on-orbit refueling early
  next year"; Musk, the goal to "immediately land the rocket and launch it again just like an airplane",
  "a little bit of refurbishment that's needed between each flight" at first, and "We expect Starship to
  fly weekly at some point in the first half next year". Only the first half of the transcript was read
  word for word; every quotation used comes from that half. Two trade sites carry the same Shotwell
  target (eeNews Europe, 2026-10-23; New Space Economy, 2026-10-21); the transcript is cited instead.
- **Falcon 9.** Wikipedia (https://en.wikipedia.org/wiki/Falcon_9): first booster landing "on flight 20 in
  December 2015"; "Since 2018, SpaceX has routinely reused first stages"; the factory "continues to
  produce one (expendable) second stage for each launch". Wikipedia's article on the launch market
  (https://en.wikipedia.org/wiki/Space_launch_market_competition): a table of estimated cost per kilogram
  giving Falcon 9 US$2,720 (no year stated, so the essay attributes it to "Wikipedia's table"), and the
  record of price cuts from reused stages. "About a fourteenth" is 200 / 2,720 = 0.074.
- **Space Shuttle.** Wikipedia (https://en.wikipedia.org/wiki/Space_Shuttle): "Five complete Space Shuttle
  orbiter vehicles were built and flown on a total of 135 missions from 1981 to 2011"; cost per launch
  "US$450 million (2011)", citing a NASA Kennedy Space Center page; the main engines "would be removed and
  replaced in between flights"; the external tank "the only major component of the Space Shuttle system
  that was not reused". The essay says these were among the reasons, and does not claim they were all
  of them.
- **Starship's design aim.** Wikipedia (https://en.wikipedia.org/wiki/SpaceX_Starship): "If completed as
  designed, Starship would be the first fully reusable orbital rocket"; "SpaceX states that its goal is to
  reduce launch costs by reusing and mass-producing both stages".
- **The tree's figures** come from `data/L-launch.toml` and `data/M-motive.toml` (baseline scenario, 2071)
  and `data/headline.json` (0.465 percent, computed 2026-10-11, last reading 2026-11-08). The 6 percent for
  the profit step is the figure published in *The Belt Equation* essay. The August 2026 date for the first
  planned ship catch is from the step's own description. "Three times in 2026" before this flight is from
  the 2026-11-08 scan.
- **Earlier verified, reused.** SpaceX's own flight page (opened 2026-11-13 by the session that wrote the
  first version): three first-version boosters caught, two flown again. Its text could not be read on
  2026-11-14 (the page returns no body text to a fetch), so it rests on the 2026-11-13 reading recorded
  above.

### Dropped, with the reason

- **The Bernstein note.** The brief said a Bernstein note before launch reportedly called demonstrating
  reusability "the most important step" for SpaceX's valuation, and to find the original or drop it. The
  only public trace is an Investing.com report (Rachael Rajan, 2026-08-02, also on Yahoo Finance) of a
  different Bernstein note, written before SpaceX's first quarterly results and not tied to Flight 15. Its
  wording is "the most important topic is the achievement of rapid reuse of Starship rockets", and it
  names no analyst. The note itself is not public. Dropped. If John wants it, the honest sentence is
  "Analysts at the investment firm Bernstein wrote in August that the most important question for
  SpaceX's value is whether it can reuse Starship quickly", linked to the Investing.com report.
- **Musk's line that the booster loss "does not change our timeline"** (CBS): a promise about the future,
  left out as not needed.
- **The universal time of launch and catch**: in this file, not in the prose.

### Links opened

Every link in the post answered on 2026-11-14 (HTTP 200): the five Belt Equation step pages, the Radar
page and home page, the two Sentient Horizons essays, the Quiet Galaxy home page and its three explanation
pages, the Wikipedia articles (the flight, Falcon 9, the launch market, the Space Shuttle, Starship,
Starbase, the Fermi Paradox, Gwynne Shotwell), CBS News, CNBC, the Motley Fool transcript, Starlink and
SpaceX. The two Space.com pages and SpaceX's flight page answer but return no body text to a fetch; their
content rests on the readings recorded above.

### Voice Calibration (final gate) and Cold Reader passes, 2026-11-14

Run from the master on `calibration-problem`'s `main` (master version 2026-10-18), plus Pattern 28 (keep
the connecting words) from the workspace rules.

- **Substance gate.** Every factual sentence carries a link; judgment is owned in the first person ("I
  think that is right", "my estimate"). Adversarial read: a hostile expert's strongest objection is that
  catching a stage proves nothing about cost, which the Shuttle paragraph meets head on, and that the
  Quiet Galaxy link is a stretch, which the essay meets by saying no number moves there and that low orbit
  is a long way from another star. Corpus coherence: checked against ledger position 25 and the *Belt
  Equation* essay's "healthy part of the chain"; both now agree with the text.
- **Fixed in the pass.** A mixed metaphor (floors and rungs; now the ladder throughout); "holds up
  everything else in the tree" (overclaimed, since the biology steps do not rest on launch); an
  announcing opener to the hopeful paragraph; "reading reads"; "the healthiest link" (the energy link is
  as healthy); an unsourced detail about spent stages; and a causal "because" about the Shuttle's costs
  that the source does not carry.
- **Counted and kept.** No em dashes. Four contrasts, each a comparison the argument needs: "it does not
  make the money", "A catch is also not a reflight", "narrower than 'the first reusable upper stage'", and
  the Shuttle's "saves far less than it seems to". One imperative ("Think of an airline"), granting a
  premise. "We" only for humanity, never for the reader's agreement.
- **Cold Reader report.** Ninety-second test: the first paragraph needs no project vocabulary, and the
  first term a newcomer meets ("upper stage") is explained in the same sentence. Coinage budget: "the
  tree" and "steps" are the only project words, both explained where they arrive. Closed loop: the body
  links outward far more than inward (Wikipedia, CBS, CNBC, Space.com, the transcript); the two corpus
  links are named and introduced. Journey test: each section's turn has its reason in the paragraph
  before it. The likeliest place a newcomer slips is the numbered chain, where "if the step before it has
  already happened" carries the meaning of every figure; it is said once, before the list, in plain words.
  The change that would help a newcomer most, as an option for John: cut the Quiet Galaxy bullets to
  two, keeping "expansion stalls" and "the inward turn", whose evidence lines name Earth directly.

### Still owed before publishing

- John's read, and his rulings on the title, the tree proposal
  (`docs/news/2026-11-14-flight-15-tree-proposal.md`) and the date style.
- A share kit (`sentient-horizons/ops/tracker-news/share-kits/README.md`). The launch-night kit, if any,
  describes the old piece.
- If the newsletter route is taken, the Sentient Horizons copy and its banner.
