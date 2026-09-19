import { defineConfig } from 'astro/config';

// Same generator and settings as the sister sites (Sentient Horizons, Hearth and Void):
// a fully static build in dist/, served from Cloudflare Workers static assets.
export default defineConfig({
  site: 'https://beltequation.com',
  trailingSlash: 'always',
});
