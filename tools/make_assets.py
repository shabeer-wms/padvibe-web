"""Builds the site's images from the app screenshots and logo.

Usage: python3 tools/make_assets.py <screenshots-dir> <roboto-fonts-dir>
  screenshots-dir  PNGs rendered from the real app (home-*.png, pad-settings-*.png, settings-midi-*.png)
  roboto-fonts-dir Flutter SDK bin/cache/artifacts/material_fonts (for Roboto-Bold/Regular.ttf)
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SHOTS, FONTS = sys.argv[1], sys.argv[2]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
ICONS = os.path.join(ROOT, "assets", "icons")
SOCIAL = os.path.join(ROOT, "marketing", "social")
BRAND = [(0x29, 0x39, 0x7A), (0x3A, 0x9D, 0xB5), (0xF1, 0x92, 0x37), (0xDE, 0x5B, 0x5B),
         (0x24, 0x5B, 0x9A), (0xBE, 0x24, 0x73), (0x25, 0x74, 0xAB), (0x82, 0x40, 0x8A)]


def font(weight, size):
    return ImageFont.truetype(os.path.join(FONTS, f"Roboto-{weight}.ttf"), size)


def webp(img, name, width=None, quality=82):
    if width and img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    path = os.path.join(IMG, name)
    img.convert("RGB").save(path, "WEBP", quality=quality, method=6)
    print(f"  {name}  {img.width}x{img.height}  {os.path.getsize(path)//1024} KB")


print("screenshots")
loaded = {}
for theme in ("dark", "light"):
    home = Image.open(os.path.join(SHOTS, f"home-{theme}.png")).convert("RGB")
    webp(home, f"app-home-{theme}.webp", 1440)
    webp(home, f"app-home-{theme}-720.webp", 720)
    pad = Image.open(os.path.join(SHOTS, f"pad-settings-{theme}.png")).convert("RGB")
    pad = pad.crop((400, 215, 1040, 685))
    webp(pad, f"app-pad-settings-{theme}.webp", 640)
    st = Image.open(os.path.join(SHOTS, f"settings-midi-{theme}.png")).convert("RGB")
    webp(st, f"app-settings-{theme}.webp", 1100)
    loaded[theme] = home

print("logo + icons")
logo = Image.open(os.path.join(ROOT, "assets", "logo.png")).convert("RGBA")
mark = logo.crop((146, 262, 878, 762))  # tight crop of the pad-grid mark


def square_icon(size, bg=(12, 12, 16), pad_ratio=0.2, radius_ratio=0.22):
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((0, 0, size - 1, size - 1), radius=int(size * radius_ratio), fill=bg + (255,))
    inner = int(size * (1 - 2 * pad_ratio))
    m = mark.copy()
    m.thumbnail((inner, inner), Image.LANCZOS)
    canvas.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
    return canvas


for size, name in ((32, "favicon-32.png"), (192, "icon-192.png"), (512, "icon-512.png"), (180, "apple-touch-icon.png")):
    square_icon(size).save(os.path.join(ICONS, name))
square_icon(48).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
logo_png = mark.copy()
logo_png.thumbnail((256, 256), Image.LANCZOS)
logo_png.save(os.path.join(ICONS, "logo-mark.png"))

# Vector version of the mark, traced from the logo geometry.
cell = 183
cells = [(0, 0, 0), (1, 0, 1), (2, 0, 2), (3, 0, 3), (0.5, 1, 4), (2.5, 1, 5), (0, 2, 6), (1, 2, 1), (2, 2, 7)]
rects = "".join(
    f'<rect x="{round(x*cell)}" y="{round(y*167)}" width="{cell}" height="167" fill="#{BRAND[c][0]:02x}{BRAND[c][1]:02x}{BRAND[c][2]:02x}"/>'
    for x, y, c in cells)
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 732 500" role="img" aria-label="PadVibe">{rects}</svg>'
open(os.path.join(ICONS, "logo-mark.svg"), "w").write(svg)
fav = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="22" fill="#0c0c10"/>'
       f'<g transform="translate(14 28) scale(0.1)">{rects}</g></svg>')
open(os.path.join(ICONS, "favicon.svg"), "w").write(fav)

print("social images")


def gradient_bg(w, h):
    bg = Image.new("RGB", (w, h), (9, 9, 11))
    glow = Image.new("RGB", (w, h), (0, 0, 0))
    d = ImageDraw.Draw(glow)
    d.ellipse((-w * 0.2, -h * 0.5, w * 0.55, h * 0.7), fill=(86, 64, 190))
    d.ellipse((w * 0.5, h * 0.35, w * 1.2, h * 1.5), fill=(190, 36, 115))
    glow = glow.filter(ImageFilter.GaussianBlur(min(w, h) * 0.22))
    return Image.blend(bg, Image.eval(glow, lambda v: v), 0.38)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def framed(shot, width):
    """The screenshot in a rounded, softly shadowed frame (RGBA)."""
    s = shot.copy().resize((width, round(shot.height * width / shot.width)), Image.LANCZOS)
    frame = Image.new("RGBA", (s.width + 12, s.height + 12), (48, 48, 64, 255))
    ImageDraw.Draw(frame).rounded_rectangle((0, 0, frame.width - 1, frame.height - 1), radius=18, outline=(110, 110, 140), width=2)
    mask = Image.new("L", s.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, s.width, s.height), radius=14, fill=255)
    frame.paste(s, (6, 6), mask)
    return frame


def paste_with_shadow(img, frame, x, y):
    shadow = Image.new("RGBA", (frame.width + 120, frame.height + 120), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((60, 75, frame.width + 60, frame.height + 75), radius=20, fill=(0, 0, 0, 190))
    shadow = shadow.filter(ImageFilter.GaussianBlur(26))
    img.paste(shadow, (x - 60, y - 60), shadow)
    img.paste(frame, (x, y), frame)


def card(w, h, title, sub, shot, name, out_dir, layout="side", badge="Free · macOS · Windows · Linux"):
    img = gradient_bg(w, h)
    d = ImageDraw.Draw(img)
    pad = int(min(w, h) * 0.06)
    m = mark.copy()
    m.thumbnail((int(h * 0.1 * 1.46), int(h * 0.1)), Image.LANCZOS)
    img.paste(m, (pad, pad), m)
    d.text((pad + m.width + 16, pad + int(h * 0.005)), "PadVibe", font=font("Bold", int(h * 0.075)), fill=(244, 244, 245))

    if layout == "side":
        text_w = int(w * 0.44) - pad
        f_t, f_s = font("Bold", int(h * 0.088)), font("Regular", int(h * 0.042))
        y = int(h * 0.28)
        for line in wrap(d, title, f_t, text_w):
            d.text((pad, y), line, font=f_t, fill=(255, 255, 255))
            y += int(h * 0.105)
        y += int(h * 0.015)
        for line in wrap(d, sub, f_s, text_w):
            d.text((pad, y), line, font=f_s, fill=(170, 170, 184))
            y += int(h * 0.056)
        frame = framed(shot, int(w * 0.62))
        paste_with_shadow(img, frame, int(w * 0.52), int(h * 0.26))
        badge_y = h - pad - int(h * 0.08)
    else:  # stack: text on top, screenshot bleeding off the bottom
        text_w = w - 2 * pad
        f_t, f_s = font("Bold", int(h * 0.074)), font("Regular", int(h * 0.036))
        y = int(h * 0.19)
        for line in wrap(d, title, f_t, text_w):
            d.text((pad, y), line, font=f_t, fill=(255, 255, 255))
            y += int(h * 0.088)
        y += int(h * 0.012)
        for line in wrap(d, sub, f_s, text_w):
            d.text((pad, y), line, font=f_s, fill=(170, 170, 184))
            y += int(h * 0.048)
        frame = framed(shot, int(w * 0.88))
        paste_with_shadow(img, frame, (w - frame.width) // 2, max(y + int(h * 0.05), int(h * 0.50)))
        badge_y = None

    if badge and badge_y is not None:
        f_b = font("Bold", int(h * 0.034))
        bw = d.textlength(badge, font=f_b) + 40
        d.rounded_rectangle((pad, badge_y, pad + bw, badge_y + int(h * 0.075)), radius=int(h * 0.038), fill=(28, 28, 40), outline=(90, 90, 118))
        d.text((pad + 20, badge_y + int(h * 0.017)), badge, font=f_b, fill=(214, 214, 226))
    img.save(os.path.join(out_dir, name), optimize=True)
    print(f"  {os.path.relpath(os.path.join(out_dir, name), ROOT)}  {os.path.getsize(os.path.join(out_dir, name))//1024} KB")


home = loaded["dark"]
pad_dark = Image.open(os.path.join(SHOTS, "pad-settings-dark.png")).convert("RGB").crop((400, 215, 1040, 685))
OG = os.path.join(ROOT, "assets", "og")
os.makedirs(OG, exist_ok=True)
og = {
    "default": ("Instant sound pads for podcasts, streams and live shows.", "A free desktop soundboard with MIDI control and a local API.", home),
    "features": ("Everything a live audio rig needs.", "Pads, MIDI learn, faders, routing, meters and an API.", home),
    "download": ("Download PadVibe. Free.", "macOS, Windows and Linux. No account needed.", home),
    "developers": ("Control PadVibe from anything.", "A local HTTP API, webhooks and a timer overlay for OBS.", pad_dark),
    "podcasting": ("A soundboard for podcasters.", "Fire intros, stingers and beds without leaving the mic.", home),
    "streaming": ("A soundboard for streamers.", "Sound effects from a key, a MIDI pad or a URL.", home),
    "theatre": ("Sound cues for live theatre.", "Reliable pads, a countdown timer and output routing.", home),
    "press": ("PadVibe press kit.", "Logos, screenshots and facts about the free soundboard.", home),
}
for key, (t, s, shot) in og.items():
    card(1200, 630, t, s, shot, f"{key}.png", OG)

card(1080, 1080, "Hit a pad. Sound plays.", "Free soundboard for podcasters, streamers and live shows.", home, "square-hero.png", SOCIAL, layout="stack")
card(1080, 1080, "Map any pad to any MIDI control.", "MIDI learn, mixer faders and RODECaster Pro support.", pad_dark, "square-midi.png", SOCIAL, layout="stack")
card(1080, 1080, "Control it from a URL.", "Local HTTP API and webhooks. Works with anything that can open a link.", home, "square-api.png", SOCIAL, layout="stack")
card(1500, 500, "The free pad soundboard.", "macOS · Windows · Linux", home, "banner-1500x500.png", SOCIAL, badge="padvibe.pro26.in")
print("done")
