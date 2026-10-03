import { defineConfig } from 'astro/config';

// Same generator and settings as the sister sites (Sentient Horizons, Hearth and Void):
// a fully static build in dist/, served from Cloudflare Workers static assets.
export default defineConfig({
  site: 'https://beltequation.com',
  trailingSlash: 'always',
  // /disagree/ was the page's address until 2026-09-25; the intro essay and older links still point there.
  redirects: { '/disagree/': '/feedback/' },
});
