// Typed access to the JSON the export script writes (scripts/export.py), plus the
// small helpers the pages share. The JSON files are generated at build time and are
// not committed; run `npm run export` (or any build) to create them.
import treeJson from '../data/tree.json';
import changelogJson from '../data/changelog.json';

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
