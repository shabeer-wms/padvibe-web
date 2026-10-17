# Paid ad copy

Ready-to-paste copy for search and social ads. Character counts are checked (see `tools/check_ads.py` in the repo root).
Landing pages use UTM tags so you can tell campaigns apart: the site itself has no analytics (by design, see the privacy page),
so use your ad platform's reporting, or add Netlify Analytics / Plausible if you want site-side numbers.

## Google Search (Responsive Search Ad)

Headlines (max 30 characters each; use at least 3, up to 15):

1. Free Soundboard App
2. Soundboard for Podcasters
3. Soundboard for Streamers
4. Instant Sound Pads
5. MIDI Learn Soundboard
6. RODECaster Pro Pads
7. Mac, Windows & Linux
8. No Account Needed
9. Download PadVibe Free
10. Play Sounds Live
11. Per-Pad Output Routing
12. Free and Open Source
13. Intros, Stingers, Beds
14. Control It From Any URL
15. Pads, Keys or MIDI

Descriptions (max 90 characters each; use 2 to 4):

1. Drop in audio, hit a pad, and it plays. Free soundboard for podcasts, streams and shows.
2. MIDI learn, mixer faders, per-pad output routing and a local API. macOS, Windows, Linux.
3. Trigger sounds from a key, a MIDI controller or a URL. No account. Free download.
4. Colourful pads, level meters and a countdown timer. Built for live audio work.

Final URLs (with UTM):
- Ad group "podcast": `https://padvibe.pro26.in/use-cases/podcasting/?utm_source=google&utm_medium=cpc&utm_campaign=podcast`
- Ad group "streaming": `https://padvibe.pro26.in/use-cases/streaming/?utm_source=google&utm_medium=cpc&utm_campaign=streaming`
- Ad group "theatre": `https://padvibe.pro26.in/use-cases/theatre/?utm_source=google&utm_medium=cpc&utm_campaign=theatre`
- Ad group "general": `https://padvibe.pro26.in/download/?utm_source=google&utm_medium=cpc&utm_campaign=general`

Keywords (start with phrase and exact match):

- Podcast: "podcast soundboard", "soundboard for podcasting", "jingle player for podcasts", "podcast sound effects app"
- Streaming: "soundboard for twitch", "soundboard for obs", "stream soundboard app", "free soundboard for streamers"
- General: "free soundboard software", "soundboard app for mac", "soundboard for windows", "soundboard for linux", "midi soundboard"
- Live: "sound cue player", "theatre sound software free", "live sound effects software"
- Hardware: "rodecaster pro soundboard", "rodecaster pro midi"

Negative keywords: meme, prank, voice changer, text to speech, tts, discord bot, mobile, android, iphone, ringtone, crack, torrent, free sound effects download

Notes:
- "Free" is accurate: the app has no paid tier. Do not claim ratings, awards or user counts: there are no verifiable numbers to cite.
- "Soundboard for OBS" is fine as a search keyword. Do not imply an official OBS or RODE partnership in the ad text.

## Reddit ads (promoted post, community targeting)

Headline (max 150): `A free soundboard with MIDI learn, mixer faders and per-pad output routing`

Body: `Drop in audio, hit a pad, and it plays. Trigger it from a key, a MIDI controller or a URL. macOS, Windows and Linux. Free and open source.`

Call to action: Download. Image: `marketing/social/square-hero.png`.
Target: r/podcasting, r/WeAreTheMusicMakers, r/Twitch, r/letsplay, r/livesound, r/Theatre (check each community's advertising rules).

## Meta / Instagram / Facebook (image ad)

Primary text: `Your intros, stingers and sound effects, one tap away. PadVibe is a free soundboard for podcasters, streamers and live shows.`
Headline: `Free soundboard for creators`
Description: `macOS, Windows, Linux`
Image: `marketing/social/square-hero.png` (1080x1080).

## YouTube pre-roll / in-stream (15 s)

Voice-over: "Hit a pad. Sound plays. PadVibe is the free soundboard for podcasters, streamers and live shows. Trigger it from a key, a MIDI pad or a link. Download it free."
Visuals: screen recording of the pad grid with sounds firing; end card with the download URL.

## Sponsorships and newsletters

Pitch template for podcasting and streaming newsletters is in `copy.md` (section "Outreach email").
