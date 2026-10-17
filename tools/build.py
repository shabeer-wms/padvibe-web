#!/usr/bin/env python3
"""Builds the static site into the repository root and validates it.

    python3 tools/build.py

Sources: src/site.css, src/site.js, tools/layout.py, tools/pages.py.
Output (committed, served as-is by Netlify): HTML pages, hashed CSS/JS, sitemap, robots, headers.
"""
import glob
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from layout import BASE, TODAY  # noqa: E402
import pages  # noqa: E402


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = re.sub(r":\s+", ":", css)
    return css.replace(";}", "}").strip()


def hashed(src, ext, transform=lambda s: s):
    with open(os.path.join(ROOT, src), encoding="utf-8") as f:
        text = transform(f.read())
    digest = hashlib.sha256(text.encode()).hexdigest()[:10]
    name = f"site.{digest}.{ext}"
    for old in glob.glob(os.path.join(ROOT, "assets", f"site.*.{ext}")):
        os.remove(old)
    write(f"assets/{name}", text)
    return name


css_name = hashed("src/site.css", "css", minify_css)
js_name = hashed("src/site.js", "js")

built = pages.all_pages()
for rel, content in built.items():
    write(rel, content.replace("@@CSS@@", css_name).replace("@@JS@@", js_name))

# ── Sitemap, robots, manifest, llms.txt ────────────────────────────────────
urls = []
for rel in built:
    if rel == "404.html":
        continue
    loc = "/" + rel.replace("index.html", "")
    priority = "1.0" if loc == "/" else "0.9" if loc in ("/download/", "/features/") else "0.7" if loc in ("/privacy/", "/terms/") else "0.8"
    urls.append((loc, priority))
urls.sort(key=lambda u: (-float(u[1]), u[0]))
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{BASE}{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>{p}</priority></url>\n" for loc, p in urls) + "</urlset>\n")
write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /marketing/\n\nSitemap: {BASE}/sitemap.xml\n")
write("manifest.webmanifest", json.dumps({
    "name": "PadVibe", "short_name": "PadVibe", "description": "Free soundboard for podcasters, streamers and live shows.",
    "start_url": "/", "display": "browser", "background_color": "#09090b", "theme_color": "#09090b",
    "icons": [{"src": "/assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
              {"src": "/assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2) + "\n")
write("llms.txt", f"""# PadVibe

> PadVibe is a free, open source desktop soundboard for macOS, Windows and Linux. Users drop audio files (MP3, WAV, OGG, FLAC) onto pads and play them with a click, a keyboard key, a MIDI controller or an HTTP request. It has MIDI learn (including RODECaster Pro pads), mixer faders, per-pad output device and channel routing, level meters, a countdown timer and a local HTTP API.

## Pages
- [Home]({BASE}/): overview and a playable demo
- [Features]({BASE}/features/): what PadVibe can do
- [Download]({BASE}/download/): installers for macOS, Windows and Linux, and a Homebrew command
- [Local API]({BASE}/developers/): HTTP endpoints, webhook, WebSocket timer and OBS overlay
- [Podcasting]({BASE}/use-cases/podcasting/), [Streaming]({BASE}/use-cases/streaming/), [Theatre and live events]({BASE}/use-cases/theatre/)
- [Changelog]({BASE}/changelog/)
- [Source code](https://github.com/shabeer-wms/padvibe)

## Facts
- Price: free, no account. Platforms: macOS (Apple Silicon and Intel), Windows 10/11, Linux.
- Not a recorder and not a cue-list sequencer: it is a pad-based sound player.
""")
write("_headers", """/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self' https://api.github.com; base-uri 'self'; form-action 'self'; frame-ancestors 'self'

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: public, max-age=0, must-revalidate
""")
write("_redirects", """# Old URLs
/platforms        /download/   301
/download.html    /download/   301
/features.html    /features/   301
/og-image-v2.png  /assets/og/default.png  301
/og-image.jpg     /assets/og/default.png  301

# Internal material is not public
/marketing/*      /404.html    404!
/tools/*          /404.html    404!
/src/*            /404.html    404!
""")

# ── Validation ─────────────────────────────────────────────────────────────
errors = []
titles, descs = {}, {}
for rel, content in built.items():
    html = content.replace("@@CSS@@", css_name).replace("@@JS@@", js_name)
    title = re.search(r"<title>(.*?)</title>", html).group(1)
    desc = re.search(r'<meta name="description" content="(.*?)">', html).group(1)
    if title in titles:
        errors.append(f"duplicate title: {title} ({rel}, {titles[title]})")
    titles[title] = rel
    if desc in descs:
        errors.append(f"duplicate description ({rel}, {descs[desc]})")
    descs[desc] = rel
    if len(title) > 70:
        errors.append(f"{rel}: title too long ({len(title)})")
    if rel != "404.html" and not 70 <= len(desc) <= 165:
        errors.append(f"{rel}: description length {len(desc)}")
    if len(re.findall(r"<h1[ >]", html)) != 1:
        errors.append(f"{rel}: needs exactly one h1")
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.S):
        try:
            json.loads(block)
        except Exception as e:
            errors.append(f"{rel}: invalid JSON-LD ({e})")
    if "aggregateRating" in html or '"Review"' in html:
        errors.append(f"{rel}: contains rating/review markup")
    for img in re.findall(r"<img [^>]*>", html):
        if " alt=" not in img:
            errors.append(f"{rel}: image without alt")
    for ref in set(re.findall(r'(?:href|src)="(/[^"#?]*)', html)):
        target = ref.lstrip("/")
        candidates = [target, target + "index.html", os.path.join(target, "index.html")]
        if not any(os.path.exists(os.path.join(ROOT, c)) for c in candidates if c):
            errors.append(f"{rel}: broken link {ref}")
    for ref in set(re.findall(r'content="(https://padvibe\.pro26\.in/[^"]*)"', html)):
        target = ref.replace(BASE + "/", "")
        if target and "." in os.path.basename(target) and not os.path.exists(os.path.join(ROOT, target)):
            errors.append(f"{rel}: missing social image {ref}")

if errors:
    print("BUILD FAILED:")
    print("\n".join("  - " + e for e in errors))
    sys.exit(1)
print(f"Built {len(built)} pages, css={css_name}, js={js_name}")
for rel in sorted(built):
    print("  ", rel)
