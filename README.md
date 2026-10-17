# padvibe-web

Source for the PadVibe website ([padvibe.pro26.in](https://padvibe.pro26.in)). It is a plain static site served by Netlify: the generated HTML is committed, so there is no build step on the host.

## Edit and rebuild

```bash
python3 tools/build.py        # regenerates every page, the sitemap, robots, headers; validates links, titles, JSON-LD
python3 -m http.server 8000   # preview at http://localhost:8000
```

| Path | What it is |
| --- | --- |
| `tools/pages.py` | Page content (copy, features, API reference, changelog) |
| `tools/layout.py` | Shared head (SEO tags), header, footer, structured data. `BASE` is the site's domain |
| `src/site.css`, `src/site.js` | Styles and scripts. The build hashes them into `assets/site.<hash>.css/js` |
| `tools/make_assets.py` | Builds images and social cards from app screenshots and the logo |
| `marketing/` | Launch copy, ad copy and SEO checklist (not published) |

After a release: update `RELEASES` in `tools/pages.py` and the announcement in `tools/layout.py`, rebuild, push. The download page reads the latest version from GitHub at runtime.

## Principles

- No frameworks, no third-party scripts or fonts, no cookies, no analytics: fast and private by default.
- No invented claims. Ratings, reviews and user counts are not added unless they are real. The build fails if rating or review markup appears.
