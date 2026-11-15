import { defineConfig } from 'astro/config';

// Same generator and settings as the sister sites (Sentient Horizons, Hearth and Void):
// a fully static build in dist/, served from Cloudflare Workers static assets.
export default defineConfig({
  site: 'https://beltequation.com',
  trailingSlash: 'always',
  // Old addresses (/disagree/, /method/, /story/) are server redirects in public/_redirects, which
  // Cloudflare reads at deploy (since 2026-11-14; before that they were in-page forwards built here).
});
