import { defineConfig } from 'astro/config';

// Same generator and settings as the sister sites (Sentient Horizons, Hearth and Void):
// a fully static build in dist/, served from Cloudflare Workers static assets.
export default defineConfig({
  site: 'https://beltequation.com',
  trailingSlash: 'always',
  // /disagree/ was the page's address until 2026-09-25; the intro essay and older links still point there.
  redirects: { '/disagree/': '/feedback/' },
  // /method/ and /story/ became the two parts of /about/ on 2026-10-21; their redirect pages are in
  // src/pages/method.astro and src/pages/story.astro, so a link to one entry (/story/#an-entry) keeps its place.
});
