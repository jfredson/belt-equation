#!/usr/bin/env python3
"""Checks the discovery watch's reader, scripts/discoveries.py (docs/discovery-sources.md; scan
procedure step 3d, added 2026-10-27). No network: each test feeds the parsers a few lines in the
shape the real sources use, as they stood on 2026-10-27. Plain Python, standard library only:

    python3 scripts/test_discoveries.py
"""
from __future__ import annotations

import datetime as dt
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import discoveries  # noqa: E402

RSS = """<?xml version="1.0"?><rss version="2.0"><channel><title>NOIRLab News</title>
<item><title>Science Release: Rubin Observatory Reveals Its First Dwarf Planet Candidate</title>
<link>http://noirlab.edu/public/news/noirlab2626/</link>
<description>&lt;img src="x.jpg" /&gt;In the outer reaches of our Solar System, Rubin has spotted 2026 ED138.</description>
<pubDate>Tue, 27 Oct 2026 11:45:00 -0700</pubDate></item>
<item><title>Photo Release: Seagull Nebula</title><link>http://noirlab.edu/public/news/noirlab2625/</link>
<description><![CDATA[Two years ago this month.]]></description>
<pubDate>Thu, 22 Oct 2026 09:00:00 -0700</pubDate></item>
<item><title>Undated thing</title><link>http://example.org/x</link><description>No date at all.</description></item>
</channel></rss>"""

RDF = """<?xml version="1.0" encoding="UTF-8" ?>
<rdf:RDF xmlns="http://purl.org/rss/1.0/" xmlns:dc="http://purl.org/dc/elements/1.1/"><channel rdf:about="https://global.jaxa.jp/">
<dc:date>2026-10-28T12:25:55+09:00</dc:date></channel>
<item rdf:about="https://global.jaxa.jp/press/2026/10/20261021-1_e.html"><dc:date>2026-10-21T14:00:00+09:00</dc:date>
<link>https://global.jaxa.jp/press/2026/10/20261021-1_e.html</link>
<title>[release] Completion of the Initial Critical Operations Phase of the MMX Spacecraft</title>
<description><![CDATA[ Today, on October 21, JAXA confirmed that the critical phase is complete.]]></description>
</item></rdf:RDF>"""

MPC = """<ul>
<p><li><a href="/mpec/K26/K26U86.html"><i>MPEC</i> 2026-U86</a> (2026 October 27)
   <ul>
   <li>2026 EE138
   </ul>
<p><li><a href="/mpec/K26/K26U84.html"><i>MPEC</i> 2026-U84</a> (2026 October 27)
   <ul>
   <li>DAILY ORBIT UPDATE (2026 October 27)
   </ul>
<p><li><a href="/mpec/K26/K26U70.html"><i>MPEC</i> 2026-U70</a> (2026 October 22)
   <ul>
   <li>OBSERVATIONS AND ORBITS OF COMETS AND A/ OBJECTS
   </ul>
</ul>"""

ARXIV = """<dl id='articles'>
    <h3>Mon, 26 Oct 2026 (showing 2 of 2 entries )</h3>
    <dt><a name='item1'>[1]</a><a href ="/abs/2610.31910" title="Abstract" id="2610.31910">arXiv:2610.31910</a></dt>
    <dd><div class='meta'><div class='list-title mathjax'><span class='descriptor'>Title:</span>
          Discovery of activity on Main Belt Asteroid 6993 (1995 BJ4)
        </div></div></dd>
    <dt><a name='item2'>[2]</a><a href ="/abs/2610.31911" title="Abstract" id="2610.31911">arXiv:2610.31911</a></dt>
    <dd><div class='meta'><div class='list-title mathjax'><span class='descriptor'>Title:</span>
          Tidal heating in a hot Jupiter atmosphere
        </div></div></dd>
    <h3>Thu, 22 Oct 2026 (showing 1 of 1 entries )</h3>
    <dt><a name='item3'>[3]</a><a href ="/abs/2610.29610" title="Abstract" id="2610.29610">arXiv:2610.29610</a></dt>
    <dd><div class='meta'><div class='list-title mathjax'><span class='descriptor'>Title:</span>
          A new moon of Uranus from JWST imaging
        </div></div></dd>
</dl>"""


class TheFeedsAreRead(unittest.TestCase):
    def test_an_rss_feed_gives_title_link_pacific_date_and_a_clean_first_line(self):
        items = discoveries.parse_rss(RSS)
        self.assertEqual(len(items), 3)
        first = items[0]
        self.assertEqual(first["title"], "Science Release: Rubin Observatory Reveals Its First Dwarf Planet Candidate")
        self.assertEqual(first["url"], "http://noirlab.edu/public/news/noirlab2626/")
        self.assertEqual(first["date"], dt.date(2026, 10, 27))
        self.assertNotIn("<img", first["line"])
        self.assertTrue(first["line"].startswith("In the outer reaches"))
        self.assertEqual(items[1]["line"], "Two years ago this month.")
        self.assertIsNone(items[2]["date"])

    def test_a_utc_timestamp_lands_on_the_pacific_date(self):
        feed = RSS.replace("Tue, 27 Oct 2026 11:45:00 -0700", "Wed, 28 Oct 2026 04:05:00 +0000")
        self.assertEqual(discoveries.parse_rss(feed)[0]["date"], dt.date(2026, 10, 27))

    def test_an_rdf_feed_takes_the_item_date_not_the_channel_date(self):
        items = discoveries.parse_rss(RDF)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["date"], dt.date(2026, 10, 20))  # 14:00 in Japan is the evening before, Pacific
        self.assertTrue(items[0]["title"].startswith("[release] Completion"))

    def test_the_minor_planet_center_list_skips_orbit_updates_and_marks_routine_designations(self):
        items = discoveries.parse_mpc(MPC)
        self.assertEqual([i["title"] for i in items],
                         ["MPEC 2026-U86: 2026 EE138", "MPEC 2026-U70: OBSERVATIONS AND ORBITS OF COMETS AND A/ OBJECTS"])
        self.assertEqual(items[0]["date"], dt.date(2026, 10, 27))
        self.assertEqual(items[0]["url"], "https://www.minorplanetcenter.net/mpec/K26/K26U86.html")
        self.assertTrue(items[0]["routine"])
        self.assertFalse(items[1]["routine"])

    def test_the_arxiv_listing_keeps_discovery_titles_under_their_day_and_counts_the_rest(self):
        items, left_out = discoveries.parse_arxiv(ARXIV)
        self.assertEqual(left_out, 1)
        self.assertEqual([(i["date"], i["url"]) for i in items],
                         [(dt.date(2026, 10, 26), "https://arxiv.org/abs/2610.31910"),
                          (dt.date(2026, 10, 22), "https://arxiv.org/abs/2610.29610")])


class TheWindowIsApplied(unittest.TestCase):
    def test_seven_days_ending_on_the_scan_date(self):
        self.assertEqual(discoveries.window(dt.date(2026, 10, 27), 7), (dt.date(2026, 10, 21), dt.date(2026, 10, 27)))

    def test_items_outside_the_window_are_dropped_and_undated_ones_kept_and_marked(self):
        items = discoveries.parse_rss(RSS)
        kept = discoveries.in_window(items, dt.date(2026, 10, 23), dt.date(2026, 10, 27))
        self.assertEqual([i["title"] for i in kept], [items[0]["title"], "Undated thing"])
        self.assertFalse(kept[0]["undated"])
        self.assertTrue(kept[1]["undated"])

    def test_a_source_that_does_not_answer_is_reported_and_the_rest_are_still_read(self):
        def getter(url):
            if "noirlab" in url:
                raise discoveries.SourceError("answered 503")
            return RSS
        sources = [s for s in discoveries.SOURCES if s["id"] in ("noirlab", "esa")]
        results = discoveries.run(sources, dt.date(2026, 10, 21), dt.date(2026, 10, 27), getter=getter)
        by_id = {r["id"]: r for r in results}
        self.assertEqual(by_id["noirlab"]["error"], "answered 503")
        self.assertEqual(by_id["noirlab"]["items"], [])
        self.assertIsNone(by_id["esa"]["error"])
        self.assertEqual(len(by_id["esa"]["items"]), 3)

    def test_the_sources_list_matches_the_document(self):
        """docs/discovery-sources.md and the script list the same addresses, in the same order."""
        doc = (Path(__file__).resolve().parent.parent / "docs" / "discovery-sources.md").read_text(encoding="utf-8")
        for s in discoveries.SOURCES:
            self.assertIn(s["page"], doc, f"{s['name']}: its page address is not in docs/discovery-sources.md")
            self.assertIn(s["feed"], doc, f"{s['name']}: its feed address is not in docs/discovery-sources.md")
        positions = [doc.index(s["feed"]) for s in discoveries.SOURCES]
        self.assertEqual(positions, sorted(positions), "the document lists the sources in another order than the script")


if __name__ == "__main__":
    unittest.main()
