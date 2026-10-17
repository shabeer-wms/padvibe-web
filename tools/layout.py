"""Shared layout: <head> with SEO tags, header, footer, structured data."""
import html
import json

BASE = "https://padvibe.pro26.in"
REPO = "https://github.com/shabeer-wms/padvibe"
SITE_NAME = "PadVibe"
TODAY = "2026-10-17"
ANNOUNCE_ID = "1.10"

ICONS = {
    "download": '<path d="M12 3v12m0 0 4-4m-4 4-4-4M4 19h16"/>',
    "github": '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>',
    "zap": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "midi": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M8 5v8m4-8v8m4-8v8M6 19v-3m4 3v-3m4 3v-3m4 3v-3"/>',
    "sliders": '<path d="M4 21v-7m0-4V3m8 18v-9m0-4V3m8 18v-5m0-4V3M1 14h6m2-6h6m2 8h6"/>',
    "route": '<circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h8a3 3 0 0 0 0-6H8a3 3 0 0 1 0-6h8"/>',
    "meter": '<path d="M3 20h18M6 20v-6m4 6V8m4 12v-9m4 9V4"/>',
    "api": '<path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "tabs": '<path d="M3 8h6l2-3h10v14H3z"/>',
    "mic": '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0m-7 7v4"/>',
    "stream": '<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8m-4-4v4m-3-9 6-3-6-3z"/>',
    "theatre": '<path d="m12 2 3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7z"/>',
    "moon": '<path d="M21 12.800A9 9 0 1 1 11.200 3a7 7 0 0 0 9.800 9.800z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.900 4.900l1.400 1.400m11.400 11.400 1.400 1.400M2 12h2m16 0h2M4.900 19.100l1.400-1.400M17.700 6.300l1.400-1.400"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "shield": '<path d="M12 3 4 6v6c0 5 3.500 8 8 9 4.500-1 8-4 8-9V6z"/>',
    "keyboard": '<rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 10h.01M10 10h.01M14 10h.01M18 10h.01M7 14h10"/>',
    "monitor": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8m-4-4v4"/>',
    "heart": '<path d="M20.800 4.600a5.500 5.500 0 0 0-7.800 0L12 5.700l-1-1.100a5.500 5.500 0 0 0-7.800 7.800l1 1.100L12 21l7.800-7.500 1-1.100a5.500 5.500 0 0 0 0-7.800z"/>',
}
COLORS = ["#29397a", "#3a9db5", "#f19237", "#de5b5b", "#245b9a", "#be2473", "#2574ab", "#82408a"]


def icon(name, size=None):
    s = f' width="{size}" height="{size}"' if size else ""
    return (f'<svg viewBox="0 0 24 24"{s} fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def ico(name, color):
    return f'<div class="ico" style="background:{color}">{icon(name)}</div>'


def esc(s):
    return html.escape(s, quote=True)


def jsonld(*blocks):
    return "\n".join(
        f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False, separators=(",", ":"))}</script>'
        for b in blocks)


def software_schema():
    # No aggregateRating or review markup: the project has no verifiable ratings.
    return {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "PadVibe",
        "url": BASE + "/",
        "applicationCategory": "MultimediaApplication",
        "applicationSubCategory": "Soundboard",
        "operatingSystem": "macOS, Windows, Linux",
        "description": "PadVibe is a free desktop soundboard for podcasters, streamers and live shows, with MIDI learn, mixer faders, per-pad output routing and a local HTTP API.",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "downloadUrl": BASE + "/download/",
        "installUrl": BASE + "/download/",
        "softwareHelp": BASE + "/developers/",
        "isAccessibleForFree": True,
        "image": BASE + "/assets/og/default.png",
        "screenshot": [BASE + "/assets/img/app-home-dark.webp", BASE + "/assets/img/app-pad-settings-dark.webp"],
        "featureList": [
            "Instant playback from memory",
            "MIDI learn for pads and faders, including RODECaster Pro",
            "Mixer faders linked to groups of pads",
            "Per-pad output device and channel routing",
            "Level meters with a soft limiter",
            "Local HTTP API, webhooks and a timer overlay for OBS",
            "Tabs, drag and drop, keyboard shortcuts, light and dark themes",
        ],
        "sameAs": [REPO],
    }


def org_schema():
    return [
        {"@context": "https://schema.org", "@type": "Organization", "name": "PadVibe", "url": BASE + "/",
         "logo": BASE + "/assets/icons/icon-512.png", "sameAs": [REPO]},
        {"@context": "https://schema.org", "@type": "WebSite", "name": "PadVibe", "url": BASE + "/"},
    ]


def breadcrumbs(crumbs):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": BASE + url}
            for i, (name, url) in enumerate(crumbs)],
    }


def faq_schema(items):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items],
    }


NAV = [("Features", "/features/"), ("Use cases", "/use-cases/"), ("Developers", "/developers/"), ("Changelog", "/changelog/")]


def header(current):
    links = "".join(
        f'<a href="{u}"{" aria-current=\"page\"" if current == u else ""}>{n}</a>' for n, u in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="announce" id="announce" data-id="{ANNOUNCE_ID}"><div class="container"><span><span class="long">PadVibe 1.10 is out: faster startup, a redesigned interface, and Windows and Linux builds.</span><span class="short">PadVibe 1.10 is out.</span> <a href="/changelog/">See what's new</a></span><button type="button" aria-label="Dismiss announcement">&times;</button></div></div>
<header class="site-header"><div class="container">
<a class="brand" href="/" aria-label="PadVibe home"><img src="/assets/icons/logo-mark.svg" width="34" height="23" alt="">PadVibe</a>
<nav class="nav" id="nav" aria-label="Main" data-open="false">{links}<a href="{REPO}" rel="noopener">GitHub</a></nav>
<div class="header-actions">
<a class="btn btn-primary btn-sm" href="/download/">Download</a>
<button class="icon-btn" id="theme-toggle" type="button" aria-label="Toggle light and dark theme">{icon("sun", 18)}</button>
<button class="icon-btn menu-btn" id="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav">{icon("menu", 18)}</button>
</div></div></header>'''


def footer():
    return f'''<footer class="site-footer"><div class="container">
<div class="footer-grid">
<div><a class="brand" href="/"><img src="/assets/icons/logo-mark.svg" width="34" height="23" alt="">PadVibe</a>
<p class="footer-note">A free, open source soundboard for podcasters, streamers and live shows. macOS, Windows and Linux.</p></div>
<div><h4>Product</h4><ul><li><a href="/features/">Features</a></li><li><a href="/download/">Download</a></li><li><a href="/changelog/">Changelog</a></li><li><a href="/press/">Press kit</a></li></ul></div>
<div><h4>Use cases</h4><ul><li><a href="/use-cases/podcasting/">Podcasting</a></li><li><a href="/use-cases/streaming/">Streaming</a></li><li><a href="/use-cases/theatre/">Theatre and live events</a></li></ul></div>
<div><h4>Resources</h4><ul><li><a href="/developers/">Local API</a></li><li><a href="{REPO}" rel="noopener">GitHub</a></li><li><a href="{REPO}/issues" rel="noopener">Report an issue</a></li><li><a href="/privacy/">Privacy</a></li><li><a href="/terms/">Terms</a></li></ul></div>
</div>
<div class="footer-bottom"><span>&copy; <span data-year>2026</span> PadVibe. Made for creators.</span><span>Not affiliated with RODE, Apple, Microsoft or the Linux Foundation. Product names belong to their owners.</span></div>
</div></footer>'''


THEME_SCRIPT = ("<script>(function(){var t=null;try{t=localStorage.getItem('pv-theme')}catch(e){}"
                "if(!t){t=window.matchMedia&&window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark'}"
                "document.documentElement.setAttribute('data-theme',t)})()</script>")


def page(path, title, description, body, og="default", current="", schema=(), noindex=False):
    url = BASE + path
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    og_img = f"{BASE}/assets/og/{og}.png"
    return f'''<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#09090b">
<meta name="color-scheme" content="dark light">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="PadVibe: colourful sound pads, mixer faders and level meters">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{og_img}">
{THEME_SCRIPT}
<link rel="preload" href="/assets/@@CSS@@" as="style">
<link rel="stylesheet" href="/assets/@@CSS@@">
{jsonld(*schema)}
</head>
<body>
<div class="glow" aria-hidden="true"></div>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/@@JS@@" defer></script>
</body>
</html>
'''
