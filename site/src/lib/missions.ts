// The typed view of site/src/data/missions.json, which scripts/export.py writes from
// data/missions.toml (the Missions page; tracker pattern rule 4.20, ruled by John 2026-10-21).
// The missions never feed the number: nothing here touches a probability.
import missionsJson from '../data/missions.json';

export interface Source { label: string; url: string }
export interface StepRef { id: string; name: string; path: string }
export interface Milestone {
  what: string;
  state: 'done' | 'plan' | 'failed';
  mark: 'done' | 'plan' | 'span' | 'failed';
  start: string;
  end: string;
  words: string;
  net: boolean;
  main: boolean;
  note: string | null;
  was: { start: string; end: string; words: string; moved_on: string } | null;
  sources: Source[];
}
export interface FlatMilestone extends Milestone { mission: string; mission_name: string; bears: boolean }
export interface Mission {
  id: string;
  name: string;
  short: string;
  url: string;
  url_label: string;
  operator: string;
  group: string;
  what: string;
  why: string;
  why_draft: boolean;
  steps: StepRef[];
  step_note: string | null;
  step_near: StepRef | null;
  notes: string | null;
  status: 'watching' | 'ended';
  checked: string;
  milestones: Milestone[];
  next: Milestone | null;
}
export interface Missions {
  available: boolean;
  checked: string;
  coming_up_days: number;
  groups: { key: string; label: string }[];
  missions: Mission[];
  milestones: FlatMilestone[];
  coming_up: FlatMilestone[];
  next: { name: string; url: string; line: string; also?: Source[] }[];
  left_out: { name: string; url: string; line: string }[];
}

export const missions = missionsJson as unknown as Missions;
export const watching = missions.missions.filter((m) => m.status === 'watching');
export const ended = missions.missions.filter((m) => m.status === 'ended');
export const missionPath = (id: string) => `/missions/#${id}`;

const LINK = /\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g;
/** The file's prose may carry Markdown links ([words](address)); this drops them to their words. */
export const plain = (s: string | null | undefined) => (s ?? '').replace(LINK, '$1');
/** The same prose as HTML, with each link kept. Everything else is escaped. */
export function linked(s: string | null | undefined): string {
  const esc = (t: string) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  let out = '';
  let last = 0;
  const text = s ?? '';
  for (const m of text.matchAll(LINK)) {
    out += esc(text.slice(last, m.index));
    out += `<a href="${esc(m[2])}" rel="noopener">${esc(m[1])}</a>`;
    last = (m.index ?? 0) + m[0].length;
  }
  return out + esc(text.slice(last));
}

export const STATE_WORD: Record<string, string> = { done: 'happened', plan: 'planned', failed: 'failed' };
