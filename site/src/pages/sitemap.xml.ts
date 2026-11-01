// The sitemap at /sitemap.xml, built from the same export every page reads, the way the sister
// sites build theirs (upgrade-tree and quiet-galaxy, site/src/pages/sitemap.xml.ts; the shape is
// the parent site's). Every public page at its stable address, nothing else: the fixed pages, one
// page per factor, one per event in the tree, one per news post. Left out: the not-found page
// (noindex), and /method/ and /story/, which have been redirects to /about/ since 2026-10-21 and
// carry noindex. Added 2026-10-31, when a search for the family's sites by name found three of
// them hard to find and four, this one among them, serving no sitemap at all.
import type { APIRoute } from 'astro';
import { tree } from '../lib/tree';
import { allPosts, postPath } from '../lib/news';

const FIXED = ['/', '/tree/', '/run/', '/radar/', '/next/', '/missions/', '/news/', '/about/', '/feedback/'];

export const GET: APIRoute = async ({ site }) => {
  const posts = await allPosts();
  const urls: { loc: string; lastmod?: string }[] = [
    ...FIXED.map((p) => ({ loc: p })),
    ...tree.factors.map((f) => ({ loc: `/tree/${f.slug}/` })),
    ...tree.nodes.map((n) => ({ loc: n.path })),
    ...posts.map((p) => ({ loc: postPath(p), lastmod: p.data.date })),
  ];
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls
  .map((u) => `<url><loc>${new URL(u.loc, site).href}</loc>${u.lastmod ? `<lastmod>${u.lastmod}</lastmod>` : ''}</url>`)
  .join('\n')}
</urlset>
`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
