// Typed access to the JSON the export script writes (scripts/export.py), plus the
// small helpers the pages share. The JSON files are generated at build time and are
// not committed; run `npm run export` (or any build) to create them.
import treeJson from '../data/tree.json';
import changelogJson from '../data/changelog.json';
import snapshotsJson from '../data/snapshots.json';
import ledgerJson from '../data/ledger.json';

export type Ref = { id: string; name: string; factor: string; factor_slug: string };

export type Scenario = {
  key: string;
  name: string;
  window_year?: number;
  plus_or_minus?: number;
  refined_on?: string;
};

export type Factor = {
  letter: string;
  slug: string;
  /** The plain-English name the home page gives this factor: "cheap launch", "fast ships". */
  chain_link: string;
  name: string;
  meaning: string;
  path: string;
  node_count: number;
  with_probability: number;
  resolved: number;
};

export type TierRequirement =
  | { kind: 'tier'; key: string; name: string }
  | ({ kind: 'node' } & Ref);

export type Tier = {
  key: string;
  name: string;
  group: 'system' | 'access';
  definition: string;
  requires: TierRequirement[];
};

export type Revision = { date: string; field: string; old: unknown; new: unknown; why: string };

export type Node = {
  id: string;
  name: string;
  factor: string;
  factor_slug: string;
  kind: 'world' | 'choice';
  description: string;
  resolution: string;
  source: string;
  horizon: 'leaf' | 'mid' | 'root';
  status: 'open' | 'resolved-yes' | 'resolved-no' | 'superseded';
  long_shot: boolean;
  mechanism: string | null;
  breaking_point: string | null;
  depends_on: Ref[];
  depends_on_any: Ref[][];
  needed_by: Ref[];
  feeds_tiers: string[];
  choice_group: string | null;
  current_plan: boolean | null;
  probability: Record<string, number> | null;
  estimated_on: string | null;
  rationale: string | null;
  resolved_on: string | null;
  resolved_by: string | null;
  resolved_links: string[];
  superseded_by: string | null;
  revisions: Revision[];
  verify: string[];
  /** Extra search terms the weekly scan adds to the ones it writes from this record. */
  watch: string[];
  notes: string | null;
  file: string;
  path: string;
};

export type Numbers =
  | { available: false; reason: string; missing: string[] }
  | {
      available: true;
      runs: number;
      seed: number;
      computed_on: string;
      review_status?: string;
      tiers: Record<string, Record<string, number>>;
      nodes: Record<string, Record<string, number>>;
      /** Per factor letter, how often every gate node of that factor held in the same play-through. */
      chain: Record<string, Record<string, number>>;
      /** The gate nodes behind each chain link: what the headline tier requires, through the tiers under it. */
      chain_nodes: Record<string, string[]>;
    };

export type Tree = {
  exported_on: string;
  commit: string | null;
  headline_tier: string;
  scenarios: Scenario[];
  factors: Factor[];
  tiers: Tier[];
  nodes: Node[];
  counts: {
    nodes: number;
    with_probability: number;
    open_world_without_probability: number;
    resolved: number;
    leaves: number;
    long_shots: number;
    choice_points: number;
  };
  numbers: Numbers;
};

export type Changelog = {
  source: string;
  intro: string;
  days: { date: string; items: string[] }[];
};

export const tree = treeJson as unknown as Tree;
export const changelog = changelogJson as unknown as Changelog;

export const factorBySlug = (slug: string): Factor | undefined => tree.factors.find((f) => f.slug === slug);
export const factorByLetter = (letter: string): Factor | undefined => tree.factors.find((f) => f.letter === letter);
export const nodesOf = (letter: string): Node[] => tree.nodes.filter((n) => n.factor === letter);
export const tierByKey = (key: string): Tier | undefined => tree.tiers.find((t) => t.key === key);

/** 0.45 -> "45%", 0.025 -> "2.5%". */
export function percent(p: number): string {
  const v = p * 100;
  return (Number.isInteger(v) ? v.toFixed(0) : v.toFixed(1).replace(/\.0$/, '')) + '%';
}

export const horizonLabel: Record<Node['horizon'], string> = {
  leaf: 'Could be decided within 1 to 5 years',
  mid: 'Could be decided within 5 to 20 years',
  root: 'Plays out over the whole window',
};
export const horizonShort: Record<Node['horizon'], string> = { leaf: 'By 2031', mid: 'Within 20 years', root: 'Whole window' };

export const statusLabel: Record<Node['status'], string> = {
  open: 'Not yet',
  'resolved-yes': 'Happened',
  'resolved-no': 'Did not happen',
  superseded: 'Replaced',
};

export const kindLabel: Record<Node['kind'], string> = {
  world: 'Happens to the world',
  choice: 'My own decision',
};

export function scenarioWindow(s: Scenario): string {
  if (!s.window_year) return 'no deadline';
  return s.plus_or_minus ? `${s.window_year} ± ${s.plus_or_minus}` : String(s.window_year);
}

export const REPO = 'https://github.com/jfredson/belt-equation';

export function recordUrl(node: Node): string {
  return `${REPO}/blob/main/data/${node.file}`;
}

export function issueUrl(title: string, body = ''): string {
  const q = new URLSearchParams({ title, body });
  return `${REPO}/issues/new?${q.toString()}`;
}

/** Escape HTML, then turn `code` spans and [text](url) links into markup. */
export function inline(text: string): string {
  const escaped = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
  return escaped
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" rel="noopener">$1</a>');
}

// ---------------------------------------------------------------- the ledger and the runs
// Written by scripts/export.py from data/ledger.toml, data/snapshots/ and data/attribution/
// (docs/ledger-plan.md, steps 28 to 32). The same rule holds here as everywhere else on the
// site: the words on an entry are written by hand, and every number beside them is computed.


/** One number per longevity scenario, keyed as scenarios.toml keys them. */
export type ByScenario = Record<string, number>;

/** One point on a history chart: a run, the day it was taken, and the number it produced. */
export type SnapshotPoint = { key: string; date: string; value: number };

export type SnapshotSummary = {
  key: string;
  date: string;
  label: string | null;
  note: string | null;
  review_status: string;
  headline_tier: string;
  run: { runs: number; seed: number; world_spread: number; commit: string | null; taken_on: string };
  tiers: Record<string, ByScenario>;
  chain: Record<string, ByScenario>;
  chain_nodes: Record<string, string[]>;
  contact: Record<string, ByScenario>;
  decisions: Record<string, { options: { id: string; name: string; current_plan: boolean; headline: ByScenario }[] }>;
};

/** What one step of the tree would be worth to the headline if it settled now. */
export type Worth = {
  reaches_headline: boolean;
  headline: ByScenario;
  headline_if_yes: ByScenario;
  headline_if_no: ByScenario;
  if_yes: ByScenario;
  if_no: ByScenario;
};

export type Snapshot = SnapshotSummary & {
  nodes: Record<string, ByScenario>;
  worth: { headline: ByScenario; reaches_headline: string[]; nodes: Record<string, Worth> } | null;
};

export type Snapshots = {
  count: number;
  headline_tier: string;
  latest_key: string | null;
  /** How far a figure from the latest run can move for no reason but the dice. */
  noise: ByScenario | null;
  snapshots: SnapshotSummary[];
  latest: Snapshot | null;
  series: {
    tiers: Record<string, Record<string, SnapshotPoint[]>>;
    chain: Record<string, Record<string, SnapshotPoint[]>>;
  };
  change: {
    from: string; from_date: string; to: string; to_date: string;
    tiers: Record<string, ByScenario>;
    chain: Record<string, ByScenario>;
  } | null;
};

export type LedgerKind = 'event' | 'resolution' | 'revision' | 'structure' | 'decision' | 'held-steady';

export type LedgerNodeChange = {
  id: string;
  name: string;
  factor: string;
  factor_slug: string;
  path: string;
  status: Node['status'];
  before: ByScenario | null;
  after: ByScenario | null;
};

export type LedgerEntry = {
  id: string;
  date: string;
  occurred_on: string | null;
  kind: LedgerKind;
  title: string;
  body: string;
  source: string | null;
  /** Absent means John wrote it; "scan" means the weekly web scan did. */
  author: string | null;
  nodes: string[];
  checked_against: string[];
  node_changes: LedgerNodeChange[];
  factors: { letter: string; name: string; slug: string }[];
  links: string[];
  snapshot: string;
  snapshot_date: string | null;
  previous_snapshot: string | null;
  headline_before: ByScenario | null;
  headline_after: ByScenario | null;
  headline_change: ByScenario | null;
  contribution: ByScenario | null;
  /** Where the headline would have landed with this entry undone and the rest of its run left alone. */
  headline_without: ByScenario | null;
  separable: boolean;
  not_separable_why: string | null;
  attributed: boolean;
  watch: { node: string; name: string; path: string | null; predicted: ByScenario | null; predicted_at: string | null } | null;
  run_note: string | null;
  corrects: string | null;
};

export type Ledger = {
  count: number;
  headline_tier: string;
  kinds: { key: LedgerKind; label: string; meaning: string }[];
  entries: LedgerEntry[];
  totals: { by_kind: Record<string, number>; by_author: Record<string, number> };
  movers: {
    year: string;
    rows: {
      id: string; title: string; kind: LedgerKind; date: string; author: string | null;
      links: string[]; contribution: ByScenario | null; sort_by: number;
      moved_nothing: boolean; not_separable_why: string | null;
    }[];
  }[];
  runs: {
    key: string; date: string; label: string | null; note: string | null; review_status: string | null;
    previous: string | null; runs: number | null; noise: ByScenario | null;
    total_move: ByScenario | null; attributed: ByScenario | null;
    remainder: ByScenario | null; unseparated: string[]; entries: string[];
  }[];
};

export const snapshots = snapshotsJson as unknown as Snapshots;
export const ledger = ledgerJson as unknown as Ledger;

/** The scenario the year dial starts on, and the one every ranking is ordered by. */
export const DEFAULT_SCENARIO = 'baseline';

/** 0.0087 -> "0.9%", 0.14 -> "14%". The home page's rounding, used everywhere numbers are shown. */
export function odds(p: number | null | undefined): string {
  if (p === null || p === undefined) return 'not yet';
  const v = p * 100;
  return (v < 10 ? v.toFixed(1) : Math.round(v).toString()) + '%';
}

/** A change in the headline, in percentage points, with its sign: "+0.9 points", "unchanged". */
export function movePoints(delta: number | null | undefined, places = 1): string {
  if (delta === null || delta === undefined) return 'not known';
  const points = delta * 100;
  if (Math.abs(points) < 0.05) return 'unchanged';
  return `${points > 0 ? '+' : '−'}${Math.abs(points).toFixed(places)} points`;
}

/** What a step is worth, for a watch list. A figure inside the run's own noise is reported as
 *  too small to tell rather than rounded to "unchanged", which would claim more than is known. */
export function worthOf(delta: number | null | undefined, noise: number | null | undefined): string {
  if (delta === null || delta === undefined) return 'not yet worked out';
  if (Math.abs(delta) <= (noise ?? 0)) return 'too small to tell apart from chance';
  return movePoints(delta);
}

/** The noise band, in percentage points. Always a size, never "unchanged": it is how big a
 *  figure has to be before it is worth reading, so rounding it away would defeat the point. */
export function band(v: number | null | undefined): string {
  if (v === null || v === undefined) return 'a tenth of a point';
  const points = v * 100;
  return `${points < 0.01 ? points.toFixed(3) : points.toFixed(2)} points`;
}

/** Up, down, or level: the arrow beside a number, and the word for people who cannot see it. */
export function direction(delta: number | null | undefined): { arrow: string; word: string; tone: string } {
  if (delta === null || delta === undefined) return { arrow: '·', word: 'no earlier run to compare with', tone: 'flat' };
  const points = delta * 100;
  if (points > 0.05) return { arrow: '▲', word: 'up', tone: 'up' };
  if (points < -0.05) return { arrow: '▼', word: 'down', tone: 'down' };
  return { arrow: '—', word: 'steady', tone: 'flat' };
}

export const ledgerKindLabel: Record<LedgerKind, string> = Object.fromEntries(
  ledger.kinds.map((k) => [k.key, k.label]),
) as Record<LedgerKind, string>;

/** Who wrote an entry, in words. Nothing recorded means John wrote it himself. */
export function authorLabel(author: string | null): string {
  if (!author) return 'Written by me';
  if (author === 'scan') return 'Written by the weekly web scan';
  return `Written by ${author}`;
}

export const entryPath = (id: string): string => `/story/#${id}`;

/** The plain name of a chain link, by factor letter: what the home page calls it. */
export const linkShort: Record<string, string> = {
  L: 'cheap launch',
  E: 'power off Earth',
  D: 'fast ships',
  B: 'bodies that hold up',
  M: 'a reason to go',
  R: 'governments',
  A: 'a seat for me',
};
