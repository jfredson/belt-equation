// The news posts (tracker pattern, rules 4.10 to 4.16, ruled by John 2026-10-18): one Markdown file
// per event of note in site/src/content/news/YYYY-MM-DD-slug.md. Everything else the site shows comes
// from the records through scripts/export.py; a post explains a change the records already carry,
// and scripts/check_news.py refuses a post that cannot be trusted (no record, no source, a figure
// in a paragraph with no link, a record that shows no change near the post's date).
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// 'mission-news' is the Belt's eighth kind (tracker pattern rule 4.20, ruled by John 2026-10-21): a post
// about a mission on the Missions page, which names missions (`missions`) instead of records.
// 'discovery' is the ninth kind (asked for by John 2026-10-27, on Rubin's first dwarf planet candidate): something
// newly found in the solar system, worth knowing about whether or not it touches a step. It names no record and
// no mission, carries its sources, and ends on what it does and does not change for the odds.
export const NEWS_KINDS = ['start-here', 'rung-reached', 'estimate-revised', 'flagged-item-ruled', 'claim', 'headline-moved', 'method-changed', 'mission-news', 'discovery'] as const;

// YAML reads a bare 2026-10-18 as a date; the site keeps dates as YYYY-MM-DD strings.
const isoDate = z.union([z.string().regex(/^\d{4}-\d{2}-\d{2}$/), z.date().transform((d) => d.toISOString().slice(0, 10))]);

const news = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/news' }),
  schema: z.object({
    title: z.string(),
    date: isoDate,
    kind: z.enum(NEWS_KINDS),
    summary: z.string(),
    records: z.array(z.string()).default([]),
    missions: z.array(z.string()).default([]),
    sources: z.array(z.object({ label: z.string(), url: z.string().url() })).default([]),
    reading: isoDate.optional(),
    before: z.string().optional(),
    after: z.string().optional(),
    stand_in: z.boolean().default(false),
  }),
});

export const collections = { news };
