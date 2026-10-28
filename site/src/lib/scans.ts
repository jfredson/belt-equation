// Typed access to the weekly scan records the export script writes (scripts/export.py,
// docs/scan-plan.md steps 34 and 37), plus the wording the pages share. Like tree.json, the
// file is generated at build time and is not committed; run `npm run export` to create it.
//
// A scan is one week's reading of the tree against the news: for each node it checked, what
// was searched, what was found, and one of five verdicts. The Radar page shows every scan,
// the home page shows a line about the latest one, and each node page shows its last checks.
import scansJson from '../data/scans.json';
import { longDate } from './dates';

export type Verdict = 'quiet' | 'noted' | 'moved' | 'resolved' | 'flagged';

/** A ledger entry a scan item points at. The ledger arrives with ledger plan step 31; until
    the entry is written there is nothing to link to, and `path` stays null. */
export type LedgerRef = { id: string; written: boolean; path: string | null };

export type ScanItem = {
  node: string;
  node_name: string;
  factor: string;
  factor_slug: string;
  /** The plain-English name of the link this node's factor is on, as the home page says it. */
  chain_link: string;
  path: string;
  verdict: Verdict;
  queries: string[];
  found: string;
  sources: string[];
  ledger: LedgerRef | null;
  for_john: string | null;
  /** On a flagged item: what took it off my list and when; null while it is still waiting. */
  picked_up: { on: string; how: string } | null;
};

/** A step of the tree a discovery touches, resolved to its page. */
export type DiscoveryNode = { id: string; name: string; path: string };

/** One thing the discovery watch found (scan procedure step 3d, added 2026-10-27): a discovery or a
    first in our own solar system, read from the fixed list of primary sources in
    docs/discovery-sources.md. It never moves a number. */
export type Discovery = {
  title: string;
  /** The day it happened or was announced, YYYY-MM-DD. */
  date: string;
  /** The primary record, an https address the scan opened before writing the item. */
  source: string;
  found: string;
  /** Which source on the list surfaced it, or null. */
  via: string | null;
  node: DiscoveryNode | null;
};

/** A discovery as the Radar's list shows it: knowing the record it came from. */
export type ListedDiscovery = Discovery & { scan_date: string; scan_file: string; test: boolean };

export type Scan = {
  date: string;
  ran_at: string;
  scope: 'weekly' | 'monthly';
  /** Zero on a record that holds only the discovery pass (the first, run by hand on 2026-10-27);
      such a record is not a reading of the tree and is never the latest scan. */
  nodes_checked: number;
  searches: number;
  commit_before: string;
  /** True on a hand-made record that stands in for a real week. The site says so wherever it shows one. */
  test: boolean;
  /** A line about the run, when the record has one. */
  note: string | null;
  file: string;
  counts: Record<Verdict, number>;
  items: ScanItem[];
  /** How many sources the discovery watch read, or null when the record predates it. */
  discovery_sources: number | null;
  discoveries: Discovery[];
};

/** One node's own check, as the node page shows it: the scan it came from, flattened in. */
export type NodeCheck = {
  date: string;
  scope: Scan['scope'];
  test: boolean;
  file: string;
  verdict: Verdict;
  found: string;
  sources: string[];
  ledger: LedgerRef | null;
  for_john: string | null;
  picked_up: { on: string; how: string } | null;
};

export type WaitingItem = ScanItem & { scan_date: string; scan_file: string; test: boolean };

export type Scans = {
  exported_on: string;
  scans: Scan[];
  waiting_on_john: WaitingItem[];
  by_node: Record<string, NodeCheck[]>;
  /** Every discovery on the record, newest first. */
  discoveries: ListedDiscovery[];
  /** The newest record whose discovery pass ran, found anything or not; null before the first. */
  last_discovery_pass: { date: string; file: string; sources: number; found: number } | null;
  counts: {
    scans: number;
    real_scans: number;
    test_scans: number;
    items: number;
    waiting_on_john: number;
    discoveries: number;
  };
};

export const scans = scansJson as unknown as Scans;

/** The scans that read the tree, newest first. A record holding only the discovery pass
    (nodes_checked of zero) is left out: it is a list of finds, not a reading. */
export const readings: Scan[] = scans.scans.filter((s) => s.nodes_checked > 0);

/** The most recent scan that read the tree, or null before the first one has run. */
export const latestScan: Scan | null = readings[0] ?? null;

/** Every check on one node, newest first. */
export const checksFor = (nodeId: string): NodeCheck[] => scans.by_node[nodeId] ?? [];

/** The badge on a card: what the scan decided, in two or three words. */
export const verdictLabel: Record<Verdict, string> = {
  quiet: 'Nothing new',
  noted: 'No change',
  moved: 'A number moved',
  resolved: 'It happened',
  flagged: 'Waiting on me',
};

/** The same five, in a sentence, for the key on the Radar page and the node pages. */
export const verdictMeaning: Record<Verdict, string> = {
  quiet: 'Nothing in the week bore on what this node is waiting for.',
  noted: 'Something relevant happened and it did not meet the test, so no number changed.',
  moved: 'The evidence changed the odds, within the limit a scan is allowed to move them.',
  resolved: 'The test was met and two independent public records agreed.',
  flagged: 'Something the scan is not allowed to do on its own, written up for me to rule on.',
};

export const scopeLabel: Record<Scan['scope'], string> = {
  weekly: 'the nodes that could resolve within five years',
  monthly: 'every open node in the world\u2019s branches, the first scan of the month',
};

/** Counts read better as words at the low end: "none", "one", then digits. */
export function plainCount(n: number): string {
  return n === 0 ? 'none' : n === 1 ? 'one' : String(n);
}

/** The moment the scan finished, in John's own time zone (the record keeps universal time,
    and the scan's date is already a Pacific date). Formatted at build time, so the page never
    shows a machine timestamp or a day that disagrees with the scan's date. */
export function ranAtLabel(scan: Scan): string {
  const d = new Date(scan.ran_at);
  if (Number.isNaN(d.getTime())) return scan.ran_at;
  const time = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Los_Angeles', hour: 'numeric', minute: '2-digit' }).format(d);
  const day = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Los_Angeles', year: 'numeric', month: '2-digit', day: '2-digit' }).format(d);
  return `${time} Pacific, ${longDate(day)}`;
}

/** "6 events read, one moved and one resolved" — the line the home page strip and the Radar
    page both use, so the site says the same thing about a scan in both places. It says "events",
    never "nodes": the tracker pattern (section 8) keeps "node", "leaf" and "trunk" off public
    pages, and "events" is what the tree page already calls them (changed 2026-10-17, the first
    adoption from the lessons review of 2026-10-17). */
export function scanSummary(scan: Scan): string {
  const read = `${scan.nodes_checked} event${scan.nodes_checked === 1 ? '' : 's'} read`;
  const parts: string[] = [];
  if (scan.counts.moved) parts.push(`${plainCount(scan.counts.moved)} moved`);
  if (scan.counts.resolved) parts.push(`${plainCount(scan.counts.resolved)} resolved`);
  if (scan.counts.flagged) {
    const open = scan.items.filter((i) => i.verdict === 'flagged' && !i.picked_up).length;
    parts.push(open ? `${plainCount(open)} left for me` : `${plainCount(scan.counts.flagged)} decided since`);
  }
  if (parts.length === 0) return `${read}, nothing moved`;
  const joined = parts.length === 1 ? parts[0] : parts.slice(0, -1).join(', ') + ' and ' + parts[parts.length - 1];
  return `${read}, ${joined}`;
}

/** The Radar's one-line form of a check (the one-column layout John approved 2026-10-21): the
 *  first sentence of what was found, and the rest for when the entry is opened. Nothing is
 *  rewritten; the split is at the first full stop, question or exclamation mark followed by a
 *  space and a capital, a digit or an opening bracket, skipping initials ("U.S.") and the common
 *  abbreviations. A note with no such break is all line. Copied from Outrunning Ageing's reading. */
const ABBREVIATIONS = /(?:^|\s)(?:e\.g|i\.e|etc|vs|cf|al|Dr|Mr|Mrs|Ms|Prof|St|No|Fig|approx|Inc|Ltd|Co|Jr|Sr)\.$/;
export function splitFirstSentence(note: string): { line: string; rest: string } {
  const text = note.replace(/\s+/g, ' ').trim();
  const breakAt = /[.!?]["'’”)]?\s+(?=[A-Z0-9(“"‘'])/g;
  let m: RegExpExecArray | null;
  while ((m = breakAt.exec(text)) !== null) {
    const upTo = text.slice(0, m.index + 1);
    if (ABBREVIATIONS.test(upTo) || /(?:^|[\s.])[A-Z]\.$/.test(upTo)) continue;
    const end = m.index + m[0].trimEnd().length;
    return { line: text.slice(0, end), rest: text.slice(end).trim() };
  }
  return { line: text, rest: '' };
}

/** Which checks open by default: every verdict except quiet ("Nothing new"), so anything noted,
 *  anything that moved or happened, and anything left for me, ruled on or not. */
export const opensByDefault = (item: ScanItem): boolean => item.verdict !== 'quiet';

/** "17 events read · 15 nothing new · 1 no change · 1 left for me, since ruled": the counts line
 *  under the Radar's heading, in the verdicts' own words (the same ones scanSummary uses for
 *  moved, resolved and left for me). */
export function scanCountLine(scan: Scan): string {
  const parts = [`${scan.nodes_checked} event${scan.nodes_checked === 1 ? '' : 's'} read`];
  const c = scan.counts;
  if (c.quiet) parts.push(`${c.quiet} nothing new`);
  if (c.noted) parts.push(`${c.noted} no change`);
  if (c.moved) parts.push(`${c.moved} moved`);
  if (c.resolved) parts.push(`${c.resolved} resolved`);
  if (c.flagged) {
    const open = scan.items.filter((i) => i.verdict === 'flagged' && !i.picked_up).length;
    const ruled = c.flagged - open;
    let part = `${c.flagged} left for me`;
    if (ruled > 0) part += open === 0 ? (c.flagged === 1 ? ', since ruled' : `, all ${c.flagged} since ruled`) : `, ${ruled} since ruled`;
    parts.push(part);
  }
  return parts.join(' · ');
}
