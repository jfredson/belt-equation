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
