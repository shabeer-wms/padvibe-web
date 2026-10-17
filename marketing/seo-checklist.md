# SEO and launch checklist

Things only you (the site owner) can do, because they need your accounts. The site itself is already set up for them.

## Search engines

- [ ] **Google Search Console:** add the property `https://padvibe.pro26.in`, verify (HTML tag, DNS or Netlify), then submit `https://padvibe.pro26.in/sitemap.xml`. Use "URL inspection" on `/` and `/download/` and request indexing.
- [ ] **Bing Webmaster Tools:** import from Search Console, which also covers DuckDuckGo and other Bing-based engines.
- [ ] Check "Pages" and "Enhancements" reports a few days later for structured-data warnings.

## Domain

- [ ] The old page declared `padvibe.com` as canonical and in the sitemap, but that domain does not serve this site. All canonical links, Open Graph URLs and the sitemap now use `padvibe.pro26.in`. If you own `padvibe.com` and want it to be the main domain, point it at Netlify, make it the primary domain, and change `BASE` in `tools/layout.py`, then rebuild.
- [ ] In Netlify: enable HTTPS and "Force HTTPS", and set one primary domain so the others redirect to it.

## GitHub (needs repo admin)

- [ ] **Description:** `Free soundboard for podcasters, streamers and live shows. MIDI learn, mixer faders, per-pad output routing and a local API. macOS, Windows, Linux.` (the current one still mentions SoLoud)
- [ ] **Website:** `https://padvibe.pro26.in`
- [ ] **Topics:** add `soundboard`, `podcast`, `streaming`, `midi`, `obs`, `rodecaster`, `live-sound`.
- [ ] **Social preview:** upload `marketing/social/github-social-preview-1280x640.png` (Settings, then Social preview).
- [ ] **Add a LICENSE file.** The README says MIT, but the repository has no LICENSE file, so GitHub shows no licence and package directories may not list the project.
- [ ] Pin the latest release and write release notes that start with a one-line summary.

## Content that helps rankings

- [ ] Share the use-case pages (`/use-cases/podcasting/`, `/use-cases/streaming/`, `/use-cases/theatre/`) where those communities gather; each targets a different search intent.
- [ ] Write the developer article in `copy.md`: technical posts attract natural backlinks.
- [ ] Ask people who really use PadVibe for a quote, with permission, and add it to the site. Do not add reviews or ratings that are not real: search engines penalise fake review markup.

## After each release

- [ ] Update `RELEASES` in `tools/pages.py` (changelog) and `ANNOUNCE_ID` / text in `tools/layout.py`, run `python3 tools/build.py`, and push. The download page picks up the new version automatically from GitHub.
