# The discovery watch: where the weekly scan looks for solar-system discoveries

Written 2026-10-27. On 2026-10-27 John decided that the site should also keep readers up to date on
discoveries in our own solar system, starting with the Rubin Observatory's first dwarf planet
candidate (the first post of the `discovery` kind, `site/src/content/news/`). This file is the fixed
list of sources the weekly scan reads for that, in step 3d of docs/scan-procedure.md. The scan reads
these and nothing else: no web searches, no aggregators, no Reddit. A source earns its place by being
a primary record, the body that found the thing or runs the mission, and by publishing in a form a
script can read each week. `scripts/discoveries.py` fetches every source below and prints the past
week's items; its list and this one are kept in step by hand, and `scripts/test_discoveries.py` fails
when they differ.

Every address was opened and confirmed on 2026-10-27. "Feed" says whether the source publishes a
machine-readable list (RSS or Atom, or the older RDF form of RSS) that the script reads, and how far
back it reaches, which matters because the scan runs once a week.

## The sources, in the order the script reads them

1. **The Minor Planet Center, recent circulars.** Page: https://www.minorplanetcenter.net/mpec/RecentMPECs.html.
   What it covers: the register of record for every newly found asteroid, comet and distant body. A
   Minor Planet Electronic Circular is the moment a find becomes official; 2026 ED138's orbit was
   published in circular 2026-U85 on the day Rubin announced it. Feed: none (the address
   `RecentMPECs.rss` answers "not found"), so the script reads the page itself, which lists the newest
   hundred circulars with their dates (https://www.minorplanetcenter.net/mpec/RecentMPECs.html). The
   list is noisy: a dozen or more circulars a week each announce one routine near-Earth asteroid, and
   a daily orbit update is housekeeping. The script leaves the orbit updates out and prints the routine
   designations on one line, so the scan reads them only to match a designation named elsewhere.
2. **NOIRLab news.** Page: https://noirlab.edu/public/news/. Feed: https://noirlab.edu/public/news/feed/
   (RSS, ten items, which on 2026-10-27 reached back to July). Why it is here instead of the Rubin
   Observatory's own news page: NOIRLab runs Rubin for the National Science Foundation, and every Rubin
   science release is published here as "Science Release: ... Rubin Observatory ...", the dwarf planet
   candidate included. Rubin's own site (https://rubinobservatory.org/news) was opened and confirmed,
   but its news page is drawn by a script in the browser (a plain fetch sees no articles) and its feed
   addresses answer "forbidden", so a script cannot read it. The scan opens a Rubin release on Rubin's
   site when NOIRLab's feed names one.
3. **NASA Science, the solar system.** Page: https://science.nasa.gov/solar-system/. Feed:
   https://science.nasa.gov/category/solar-system/feed/ (RSS, ten items, about three weeks deep). NASA's
   own account of what its planetary missions found: a first measurement, a first image, an arrival.
   The site-wide feed (`science.nasa.gov/feed/`) was tried and left out: it mixes in every field and
   holds only a day. NASA's press-release feed was left out for the same reason, ten items covering two
   days.
4. **NASA's Jet Propulsion Laboratory, news.** Page: https://www.jpl.nasa.gov/news/. Feed:
   https://www.jpl.nasa.gov/feeds/news/ (RSS, a hundred items, more than a year deep). JPL runs most of
   NASA's planetary spacecraft and announces their firsts first; it overlaps the NASA Science feed and
   the overlap is cheap, since the script prints a repeated story twice and the scan writes it once.
5. **ESA, space science news.** Page: https://www.esa.int/Science_Exploration/Space_Science. Feed:
   https://www.esa.int/rssfeed/science (RSS, fifteen items, about two months deep). The European
   agency's missions: Juice on its way to Jupiter, BepiColombo at Mercury, Hera at the asteroid Didymos,
   and Euclid, which found its first comet in September 2026.
6. **JAXA, press releases.** Page: https://global.jaxa.jp/press/. Feed: https://global.jaxa.jp/rss/press.rdf
   (the RDF form of RSS, twenty items, about three months deep). The Japanese agency's missions,
   including MMX, launched on 2026-10-19 for the Martian moon Phobos, whose arrival will be a first.
7. **arXiv, planetary science papers of the past week.** Page:
   https://arxiv.org/list/astro-ph.EP/pastweek?skip=0&show=500. The preprint server's "Earth and
   Planetary Astrophysics" section is where a first measurement is written up, sometimes before any
   press release. Feed: the RSS feed (`rss.arxiv.org/rss/astro-ph.EP`) holds one day only, and the
   query interface answered "too many requests" when tried, so the script reads the past-week listing
   page, which carries every paper under its day (68 papers in the week to 2026-10-27). That is too
   many for a scan to read, so the script prints only the titles that carry a discovery word (discovery,
   first detection, new moon, interstellar object, dwarf planet, occultation, and so on) and says how
   many it left out. The net is deliberately narrow and is widened when a scan is shown to have missed
   something.

## Considered and left out, and why

- **The Rubin Observatory's news page** (https://rubinobservatory.org/news): opened and confirmed, but
  not readable by a script, as under NOIRLab above. It is read by hand when NOIRLab names a release.
- **The Asteroid Institute** (https://b612.ai/, the B612 Foundation's https://b612foundation.org/):
  opened and confirmed. Its finds reach the record through the Minor Planet Center, which the list
  already reads, and its own feeds (`b612.ai/rss.xml`, a newsletter with one item since July;
  `b612foundation.org/feed/`, last posted 2026-09-23) publish about once a month. A find of its own
  would show up in the circulars first.
- **The Planetary Society** (https://www.planetary.org/articles, feed https://www.planetary.org/rss/articles):
  opened and confirmed, fifty items. It is a good explainer and an advocacy body, not a primary record:
  it writes about what the agencies and observatories above announced. The scan procedure's rule on
  sources (primary records, never aggregators) keeps it off the list. A reader wanting the explainer
  can be pointed to it in a post.
- **Reddit**: not a primary record, and no Claude session can read it (`~/Code/CLAUDE.md`, "Reading a
  Reddit link").
- **Web searches**: the rest of the scan runs on them, and they stay out of this pass on purpose. A
  search finds what was widely written about, which for a discovery is the aggregators; the sources
  above are where the discovery is first recorded, and a feed is the same every week, so a quiet week
  is a real finding and not a search that happened to miss.

## What the scan does with the list

The rule, from the procedure's step 3d: read the past week's items, keep the ones that are a discovery
or a first in our own solar system (a new body, a first image, a first measurement, a mission
arrival), open each one, and write it as a `[[discovery]]` item in the scan record with its title, the
date it happened, the source's address, one plain sentence, and the step of the tree it touches, or
"none". A launch is the missions step's business (step 3c), not this one. A post is written only when
John says so; the record is what the site shows until then, in its own short list on the Radar page.

## Cost

A run of the script takes about half a minute and no money (standard library, no API). Reading its
output takes a scan a few minutes: on 2026-10-27 it printed about a dozen lines outside the routine
designations, from which the scan kept one item. The first run found the dwarf planet candidate through
two sources (NOIRLab's feed and the Minor Planet Center's list), which is the check a weekly read
wants: a find that is real appears in the body that found it and in the register that recorded it.
