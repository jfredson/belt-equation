// Typed access to the weekly scan records the export script writes (scripts/export.py,
// docs/scan-plan.md steps 34 and 37), plus the wording the pages share. Like tree.json, the
// file is generated at build time and is not committed; run `npm run export` to create it.
//
// A scan is one week's reading of the tree against the news: for each node it checked, what
// was searched, what was found, and one of five verdicts. The Radar page shows every scan,
// the home page shows a line about the latest one, and each node page shows its last checks.
import scansJson from '../data/scans.json';

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
};

export type Scan = {
  date: string;
  ran_at: string;
  scope: 'weekly' | 'monthly';
  nodes_checked: number;
  searches: number;
  commit_before: string;
  /** True on a hand-made record that stands in for a real week. The site says so wherever it shows one. */
  test: boolean;
  file: string;
  counts: Record<Verdict, number>;
  items: ScanItem[];
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
};

export type WaitingItem = ScanItem & { scan_date: string; scan_file: string; test: boolean };

export type Scans = {
  exported_on: string;
  scans: Scan[];
  waiting_on_john: WaitingItem[];
  by_node: Record<string, NodeCheck[]>;
  counts: {
    scans: number;
    real_scans: number;
    test_scans: number;
    items: number;
    waiting_on_john: number;
  };
};

export const scans = scansJson as unknown as Scans;

/** The most recent scan, or null before the first one has run. */
export const latestScan: Scan | null = scans.scans[0] ?? null;

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
  return `${time} Pacific, ${day}`;
}

/** "6 nodes read, one moved and one resolved" — the line the home page strip and the Radar
    page both use, so the site says the same thing about a scan in both places. */
export function scanSummary(scan: Scan): string {
  const read = `${scan.nodes_checked} node${scan.nodes_checked === 1 ? '' : 's'} read`;
  const parts: string[] = [];
  if (scan.counts.moved) parts.push(`${plainCount(scan.counts.moved)} moved`);
  if (scan.counts.resolved) parts.push(`${plainCount(scan.counts.resolved)} resolved`);
  if (scan.counts.flagged) parts.push(`${plainCount(scan.counts.flagged)} left for me`);
  if (parts.length === 0) return `${read}, nothing moved`;
  const joined = parts.length === 1 ? parts[0] : parts.slice(0, -1).join(', ') + ' and ' + parts[parts.length - 1];
  return `${read}, ${joined}`;
}
