# Launch copy

Everything here only claims what PadVibe actually does. Do not add user counts, ratings, awards or testimonials unless they are real and you can show the source.
Each community has its own self-promotion rules: read them before posting, be present in the comments, and answer questions honestly.

Site: https://padvibe.pro26.in  ·  Source: https://github.com/shabeer-wms/padvibe

## Names and taglines

- Product line: **PadVibe, the free soundboard for podcasters, streamers and live shows.**
- Tagline options: "Hit a pad. Sound plays." / "Instant sound pads." / "Your sounds, one tap away."
- One sentence: PadVibe is a free desktop soundboard for macOS, Windows and Linux with MIDI learn, mixer faders, per-pad output routing and a local API.
- Elevator (25 words): Drop audio onto colourful pads and play it with a click, a key, a MIDI controller or a URL. Free, open source, no account.

## Keywords (for tags, directories, ads)

soundboard, sound pads, audio palette, jingle player, podcast tools, streaming tools, OBS, MIDI, RODECaster Pro, live sound, sound cues, Flutter, open source

## X / Bluesky / Mastodon

1. `PadVibe is a free soundboard for podcasters, streamers and live shows. Drop in audio, hit a pad, it plays. MIDI learn, mixer faders, per-pad output routing. macOS, Windows, Linux. https://padvibe.pro26.in`
2. `Intros, stingers, beds and reactions, one tap away. PadVibe: free, open source, no account. https://padvibe.pro26.in/use-cases/podcasting/`
3. `Trigger sounds from a key, a MIDI pad or a URL. PadVibe has a local HTTP API, webhooks and an OBS timer overlay. https://padvibe.pro26.in/developers/`
4. `RODECaster Pro pads can trigger PadVibe over MIDI. Learn a note, map a fader, route each pad to its own output. https://padvibe.pro26.in/features/`
5. `PadVibe 1.10: audio engine starts in about a second (it took ~20), redesigned interface, Windows and Linux builds. https://padvibe.pro26.in/changelog/`
6. `Small windows, big shows: PadVibe's layout adapts from a laptop corner to a full screen, in light or dark. https://padvibe.pro26.in`

Attach `marketing/social/square-hero.png` or the screenshots from `assets/img/`.

## LinkedIn

> I built PadVibe, a free soundboard for people who play sound live: podcasters, streamers, theatre and event crews.
>
> Drop audio onto pads and trigger it from the mouse, a key, a MIDI controller or a URL. Each pad can have its own output device and channels, faders can group pads, and a small local API lets other tools read state and press pads.
>
> It runs on macOS, Windows and Linux, it is free and open source, and it needs no account.
>
> https://padvibe.pro26.in  #podcasting #streaming #livesound #opensource #flutter

## Product Hunt

- **Name:** PadVibe
- **Tagline (max 60):** `Free soundboard for podcasters, streamers and live shows`
- **Description (max 260):** `Drop audio onto colourful pads and play it instantly with a click, a key, a MIDI controller or a URL. MIDI learn, mixer faders, per-pad output routing, level meters and a local API. macOS, Windows, Linux. Free and open source.`
- **Topics:** Audio, Podcasting, Streaming, Open Source, Productivity
- **Gallery:** `app-home-dark.webp` (convert to PNG), `app-pad-settings-dark.webp`, `app-settings-dark.webp`, `square-midi.png`, plus a 30 to 60 s screen recording
- **First comment (maker):**
  > Hi, I'm the maker. PadVibe started as a simple pad player and grew the controls live work needs: MIDI learn (RODECaster Pro pads work), faders that group pads, and per-pad output routing for multi-channel interfaces. It runs its audio in a separate engine that restarts itself if anything goes wrong, so the interface never freezes. It is free and open source. I'd love to hear what is missing for your setup.

## Hacker News (Show HN)

- **Title:** `Show HN: PadVibe, a free open source soundboard with MIDI learn and a local API`
- **Text:**
  > PadVibe is a pad-based soundboard for macOS, Windows and Linux. The UI is Flutter; audio and MIDI run in a separate Python process that the app supervises over a local WebSocket.
  >
  > Things I found interesting while building it:
  > - A PyInstaller one-file build re-extracts itself on every launch and macOS re-scans the extracted files each time: ~13 s to start. A one-dir build starts in under a second after the first run.
  > - Decoding mp3 on every play was the slow part of triggering a pad. Files are now decoded once into a shared in-memory cache used by playback and waveforms.
  > - A CoreAudio stop() that blocks while holding a lock froze the sidecar's event loop. Native audio calls now never run under the engine lock.
  >
  > It exposes an HTTP API on localhost (state, play/stop, volume, tabs) and can POST its state to a webhook. Source and downloads: https://github.com/shabeer-wms/padvibe. Feedback welcome, especially from people running live shows.

## Reddit

Follow each subreddit's rules (many limit self-promotion to a ratio or a weekly thread). Suggested framings:

- **r/podcasting:** "I made a free soundboard for firing intros, stingers and beds while recording (macOS/Windows/Linux). Looking for feedback from people who record solo." Link to `/use-cases/podcasting/`.
- **r/Twitch or r/streaming:** "Free open source soundboard that can be triggered from a MIDI pad or a URL, with a countdown overlay for OBS." Link to `/use-cases/streaming/`.
- **r/livesound or r/Theatre:** "A free pad-based sound player for small productions: scene banks, per-pad outputs, countdown timer. It is not a cue-list sequencer, so tell me if that's a dealbreaker." Link to `/use-cases/theatre/`.
- **r/opensource, r/FlutterDev:** a technical post using the Show HN text above.
- **r/macapps, r/windowsapps, r/linux:** a short "free app" post with a screenshot and the download link.

## Developer article (dev.to / Hashnode / personal blog)

Working title: **"From 13 seconds to under 1: how PyInstaller's one-file mode slowed my desktop app"**

Outline (all numbers are from measurements on a real Mac):
1. The symptom: an audio sidecar that took ~20 s to start on a Mac Pro.
2. Ruling out the obvious: imports took ~1 s from source; a hello-world frozen app still took ~8 s.
3. The cause: one-file extracts to a new temp dir each launch and macOS re-scans it; one-dir is scanned once. 13 s to under 1 s on repeat launches.
4. Lessons: measure first, check the second run, and keep native calls off your event loop (the CoreAudio stop() freeze).
5. Decode once: a shared in-memory cache turned a 183 ms decode per play into a lookup.

## YouTube demo (60 to 90 seconds)

1. (0:00) Cold open: hit pads, sounds fire. Caption: "Hit a pad. Sound plays."
2. (0:10) Drag three files onto pads; set a loop on a bed.
3. (0:25) Pad settings: learn a MIDI note, set a key.
4. (0:40) Route one pad to a different output; show the mixer fader moving the bed.
5. (0:55) Browser: `curl http://localhost:9696/play/0`, and the OBS timer overlay.
6. (1:10) End card: padvibe.pro26.in, "Free for macOS, Windows and Linux".

## Outreach email (podcasting and streaming newsletters)

Subject: `A free soundboard for [podcasters / streamers]`

> Hi [name],
>
> I make PadVibe, a free open source soundboard for macOS, Windows and Linux. You drop audio onto pads and play it from the mouse, a key, a MIDI controller or a URL; each pad can use its own output and a fader can group pads. It also has a local API and an OBS timer overlay.
>
> I thought it might suit your readers who [record solo / run live streams]. A link and a screenshot are below; I'm happy to answer questions or send a build.
>
> https://padvibe.pro26.in
>
> Thanks for your time,
> [your name]

## Directories and lists to submit to

- AlternativeTo (list as an alternative to other soundboard apps), Slant, MacUpdate, Softpedia
- GitHub: set the repository description, website and topics (see `seo-checklist.md`)
- Awesome lists that fit: awesome-flutter, awesome-open-source-desktop apps lists, audio tool lists
- Homebrew: already available via the tap `shabeer-wms/padvibe`; consider submitting to the main `homebrew-cask` once the app is code-signed
- Product Hunt and Hacker News (above)
