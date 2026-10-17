"""Page content. Everything stated here is checked against the app and its repository."""
from layout import (BASE, REPO, COLORS, breadcrumbs, esc, faq_schema, ico, icon, org_schema, page,
                    software_schema)

DL_ICON = icon("download")
GH_ICON = icon("github")


def shot(name, alt, w, h, eager=False, small=None):
    """A screenshot in a window frame, with dark and light variants."""
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    out = ['<div class="window"><div class="window-bar"><i></i><i></i><i></i><span>PadVibe</span></div>']
    for theme in ("dark", "light"):
        extra = f' srcset="/assets/img/app-{name}-{theme}-720.webp 720w, /assets/img/app-{name}-{theme}.webp {w}w" sizes="(max-width: 760px) 100vw, {w}px"' if small else ""
        out.append(f'<img class="shot-{theme}" src="/assets/img/app-{name}-{theme}.webp"{extra} width="{w}" height="{h}" alt="{esc(alt)}" {load}>')
    out.append("</div>")
    return "".join(out)


def crumbs(*items):
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(
        f'<a href="{u}">{n}</a>' if u else f"<span>{n}</span>" for n, u in items) + "</nav>"


def cta_band(title="Free to download. Ready in a minute.", text="No account, no subscription, no tracking. Install it, drop in a few sounds and hit a pad."):
    return f'''<section class="section"><div class="container"><div class="cta-band">
<h2>{title}</h2><p>{text}</p>
<div class="cta-row"><a class="btn btn-primary btn-lg" href="/download/">{DL_ICON} Download PadVibe</a><a class="btn btn-lg" href="{REPO}" rel="noopener">{GH_ICON} Star on GitHub</a></div>
</div></div></section>'''


def faq(items):
    rows = "".join(f"<details><summary>{esc(q)}</summary><div><p>{a}</p></div></details>" for q, a in items)
    return f'<div class="faq">{rows}</div>'


def plain(a):
    import re
    return re.sub(r"<[^>]+>", "", a)


# ── Home ────────────────────────────────────────────────────────────────────

PADS = [
    ("Kick", "kick", "1", 0.5), ("Snare", "snare", "2", 0.4), ("Hat", "hat", "3", 0.2), ("Clap", "clap", "4", 0.35),
    ("Airhorn", "airhorn", "q", 0.9), ("Rimshot", "rimshot", "w", 0.4), ("Ding", "ding", "e", 1.2), ("Whoosh", "whoosh", "r", 0.8),
    ("Buzzer", "buzzer", "a", 0.6), ("Laser", "laser", "s", 0.35), ("Chime", "arp", "d", 0.6), ("Drumroll", "roll", "f", 0.9),
]

HOME_FAQ = [
    ("What is PadVibe?", "PadVibe is a free desktop soundboard. You drop audio files onto pads, then play them with a click, a keyboard key, a MIDI controller or a URL. It is built for podcasters, streamers and live shows."),
    ("Is PadVibe free?", "Yes. PadVibe is free to download and use, with no account, subscription or ads. The source code is public on GitHub."),
    ("Which systems does it run on?", "macOS (Apple Silicon and Intel), Windows 10 and 11 (64-bit) and Linux (64-bit). The downloads are on the <a href=\"/download/\">download page</a>."),
    ("Which audio formats can I use?", "MP3, WAV, OGG and FLAC."),
    ("Does it work with MIDI controllers?", "Yes. Use MIDI learn to map any pad or mixer fader to any MIDI note or control change. It was built with RODECaster Pro pads in mind, and it also understands program change messages."),
    ("Can I send sound to OBS, Zoom or my mixer?", "Each pad can use its own output device, and on multi-channel interfaces its own channels. To send PadVibe into another app, choose a virtual audio device such as BlackHole on macOS or VB-Cable on Windows as the output and capture that in the other app."),
    ("How fast is it?", "Audio is decoded once and then played from memory, so a pad starts as soon as you hit it. Output latency is typically 20 to 60 milliseconds, depending on your audio interface."),
    ("Does it record or collect my data?", "No. PadVibe only plays audio. It has no account system and no analytics. Your sounds and settings stay on your computer. See the <a href=\"/privacy/\">privacy page</a>."),
]


def home():
    pads = "".join(
        f'<button class="pad" type="button" style="background:{COLORS[i % len(COLORS)]}" data-sound="{snd}" data-key="{key}" data-dur="{dur}" aria-label="{label} (key {key.upper()})">'
        f'<kbd>{key.upper()}</kbd><span>{label}</span><i class="bar"></i></button>'
        for i, (label, snd, key, dur) in enumerate(PADS))
    features = [
        ("zap", COLORS[2], "Instant playback", "Audio is decoded once and played from memory, so a pad fires the moment you hit it. Loop, restart and seek any pad."),
        ("midi", COLORS[5], "MIDI learn", "Map any pad or fader to any MIDI note or control. RODECaster Pro pads are supported, and so are program change messages."),
        ("sliders", COLORS[4], "Mixer faders", "Link groups of pads to a shared fader and drive it from one physical slider on your controller."),
        ("route", COLORS[1], "Output routing", "Send each pad to its own audio interface or to specific channels. Built for multi-channel rigs."),
        ("meter", COLORS[7], "Meters and limiter", "Live left and right level meters with peak hold, and a soft limiter on the master bus so loud pads do not clip."),
        ("api", COLORS[3], "Local API", "Read state, trigger pads and change volume over HTTP, get webhooks, and show a countdown in OBS."),
    ]
    feat_html = "".join(
        f'<div class="card hover">{ico(i, c)}<h3>{t}</h3><p>{d}</p></div>' for i, c, t, d in features)
    cases = [
        ("mic", COLORS[2], "Podcasting", "Intros, outros, stingers and beds, one tap away while you talk.", "/use-cases/podcasting/"),
        ("stream", COLORS[5], "Streaming", "Sound effects and alerts from a key, a MIDI pad or a URL.", "/use-cases/streaming/"),
        ("theatre", COLORS[4], "Theatre and live events", "Scene banks, a countdown timer and per-pad output routing.", "/use-cases/theatre/"),
    ]
    case_html = "".join(
        f'<a class="card" href="{u}">{ico(i, c)}<h3>{t}</h3><p>{d}</p><span class="more">Learn more &rarr;</span></a>'
        for i, c, t, d, u in cases)
    body = f'''
<section class="hero"><div class="container">
<div class="hero-grid">
<div>
<span class="pill"><span class="dot"></span>Free and open source &middot; <span data-version>latest release</span></span>
<h1 style="margin-top:18px">Instant sound pads for <span class="grad">podcasts, streams and live shows.</span></h1>
<p class="lead">PadVibe is a free desktop soundboard. Drop in your audio, hit a pad, and it plays. Trigger it from the keyboard, a MIDI controller or a URL.</p>
<div class="cta-row">
<a class="btn btn-primary btn-lg" href="/download/" data-dl-primary>{DL_ICON} <span>Download for <span data-os-label>your computer</span></span></a>
<a class="btn btn-lg" href="{REPO}" rel="noopener">{GH_ICON} View on GitHub</a>
</div>
<p class="fine">macOS, Windows and Linux &middot; No account &middot; MP3, WAV, OGG and FLAC</p>
</div>
<div class="padbox" role="group" aria-label="Try the pads">
<div class="padbox-head"><strong>Try it</strong><span>Click the pads, or press the keys shown</span></div>
<div class="padgrid" id="padgrid">{pads}</div>
<p class="pad-note">These sounds are synthesized in your browser. In PadVibe you play your own files.</p>
</div>
</div>
<div class="hero-shot">{shot("home", "PadVibe main window: a grid of colourful sound pads with waveforms, a mixer with faders, master level meters and a countdown timer", 1440, 900, eager=True, small=True)}</div>
</div></section>

<section class="section"><div class="container">
<div class="stats">
<div class="stat"><b>3 platforms</b><span>macOS, Windows, Linux</span></div>
<div class="stat"><b>No account</b><span>Nothing to sign up for</span></div>
<div class="stat"><b>20 to 60 ms</b><span>Typical output latency*</span></div>
<div class="stat"><b>Open source</b><span>Code is public on GitHub</span></div>
</div>
<p class="fine" style="margin-top:12px">*Depends on your audio interface and buffer. Measured at 21 to 63 ms on built-in, USB and virtual devices on macOS.</p>
</div></section>

<section class="section alt" id="features"><div class="container">
<div class="section-head"><span class="eyebrow">Features</span><h2>Everything a live audio rig needs, nothing it doesn't.</h2>
<p>Built for people who trigger sound while doing something else: talking, streaming, running a show.</p></div>
<div class="grid g3">{feat_html}</div>
<p style="margin-top:28px"><a class="btn" href="/features/">See all features &rarr;</a></p>
</div></section>

<section class="section"><div class="container">
<div class="split">
<div><span class="eyebrow">Set up in seconds</span><h2>Drop a file on a pad. That is the whole setup.</h2>
<p style="color:var(--muted)">Each pad has a name, a colour, a loop switch and its own volume. Open <strong>Pad settings</strong> to set a keyboard key, learn a MIDI control, pick an output device or link the pad to a fader. Everything for one pad lives in one place.</p>
<ul class="checks"><li><strong>Drag and drop</strong> files straight onto pads, or pick several at once.</li><li><strong>Keyboard keys and MIDI</strong> for hands-free triggering.</li><li><strong>Tabs</strong> keep a whole show organised: one bank per scene or episode.</li><li><strong>Background pads</strong> stay out of the API and the countdown, ideal for long beds.</li></ul></div>
<div>{shot("pad-settings", "PadVibe pad settings dialog with Playback, Triggers and Output tabs showing keyboard key and MIDI control assignment", 640, 470)}</div>
</div></div></section>

<section class="section alt"><div class="container">
<div class="split rev">
<div>{shot("settings", "PadVibe settings screen listing MIDI input devices with Connect buttons", 1100, 760)}</div>
<div><span class="eyebrow">Designed to stay out of the way</span><h2>A clear interface, in light or dark.</h2>
<p style="color:var(--muted)">Settings are grouped into General, Audio, MIDI, Integrations and Diagnostics. The layout adapts from a small window to a full screen, and the theme follows your system or your choice.</p>
<ul class="checks"><li>Responsive layout that rearranges as the window changes size.</li><li>A built-in <strong>Diagnostics</strong> view shows the audio engine status and where the logs are.</li><li>The audio engine restarts itself if it ever stops responding.</li></ul></div>
</div></div></section>

<section class="section"><div class="container">
<div class="section-head"><span class="eyebrow">Use cases</span><h2>Made for people who play sound live.</h2></div>
<div class="grid g3">{case_html}</div>
</div></section>

<section class="section alt"><div class="container">
<div class="section-head"><span class="eyebrow">How it works</span><h2>From download to first sound in three steps.</h2></div>
<div class="steps">
<div class="step"><h3>Add your sounds</h3><p>Drag audio files onto pads. PadVibe keeps its own copy, so moving the original never breaks a pad.</p></div>
<div class="step"><h3>Choose your triggers</h3><p>Set a keyboard key, or press Learn and hit a button on your MIDI controller.</p></div>
<div class="step"><h3>Play</h3><p>Click, press or tap. Route each pad to the right output and balance everything with faders.</p></div>
</div></div></section>

<section class="section"><div class="container">
<div class="split">
<div><span class="eyebrow">For developers and tinkerers</span><h2>Control it from anything that can open a URL.</h2>
<p style="color:var(--muted)">PadVibe runs a small HTTP server on your machine. Read the full state, trigger pads, set volumes, switch tabs, or have PadVibe post its state to your own webhook. It also serves a countdown overlay you can drop into OBS as a Browser Source.</p>
<p><a class="btn" href="/developers/">Read the API docs &rarr;</a></p></div>
<div><div class="codewrap"><button class="copy" type="button">Copy</button><pre><code><span class="tok-c"># read the live state</span>
curl http://localhost:9696/state

<span class="tok-c"># play the first pad, then stop everything</span>
curl http://localhost:9696/play/0
curl http://localhost:9696/stop_all

<span class="tok-c"># set the master volume to 60%</span>
curl http://localhost:9696/volume/master/0.6</code></pre></div></div>
</div></div></section>

<section class="section alt"><div class="narrow">
<div class="section-head center"><span class="eyebrow">FAQ</span><h2>Questions, answered.</h2></div>
{faq(HOME_FAQ)}
</div></section>
{cta_band()}'''
    schema = [software_schema(), *org_schema(), faq_schema([(q, plain(a)) for q, a in HOME_FAQ])]
    return page("/", "PadVibe: Free Soundboard App for macOS, Windows & Linux",
                "PadVibe is a free soundboard app. Drop in audio, hit a pad, and it plays. MIDI learn, mixer faders, per-pad output routing and a local API.",
                body, og="default", current="/", schema=schema)


# ── Features ────────────────────────────────────────────────────────────────

def features():
    def block(eyebrow, title, text, items, image=None, rev=False):
        left = f'<div><span class="eyebrow">{eyebrow}</span><h2>{title}</h2><p style="color:var(--muted)">{text}</p><ul class="checks">' + "".join(f"<li>{i}</li>" for i in items) + "</ul></div>"
        if not image:
            return f'<section class="section"><div class="narrow">{left}</div></section>'
        return f'<section class="section"><div class="container"><div class="split{" rev" if rev else ""}">{left}<div>{image}</div></div></div></section>'

    body = f'''
<section class="page-hero"><div class="container">{crumbs(("Home", "/"), ("Features", None))}
<h1>Features</h1>
<p class="lead">PadVibe is a pad-based soundboard with the controls live audio work needs: fast playback, hardware control, routing and an API.</p></div></section>
{block("Playback", "Fast, predictable playback", "Each file is decoded once and kept in memory, so triggering a pad does not wait on disk or on decoding. Playback and the waveform share the same decoded audio.", [
        "<strong>Play, pause, resume, loop and seek</strong> on every pad, with a short fade-in that avoids clicks.",
        "<strong>Per-pad volume</strong> and a <strong>master volume</strong>, with a soft limiter on the master bus.",
        "<strong>Waveforms</strong> drawn on every pad, so you can see where you are.",
        "<strong>MP3, WAV, OGG and FLAC</strong>, including very long files, which stream from disk.",
        "Stops are immediate and the audio engine stays responsive when you hit pads quickly."], shot("home", "PadVibe pad grid with waveforms and a playing pad", 1440, 900, small=True))}
{block("Control", "Play it however your hands prefer", "Pads respond to the mouse, the keyboard and MIDI. Everything for a pad is in a single Pad settings dialog with three tabs: Playback, Triggers and Output.", [
        "<strong>Keyboard keys</strong>: press the key to play, hold Shift to stop.",
        "<strong>MIDI learn</strong>: press Learn, then hit a pad or button on your controller. Notes, control changes and program change messages all work.",
        "<strong>RODECaster Pro support</strong>: channel-aware trigger IDs, so pads on different MIDI channels stay separate.",
        "<strong>Mixer faders</strong>: create faders, link groups of pads to them, and map each to a hardware slider."], shot("pad-settings", "Pad settings dialog, Triggers tab", 640, 470), rev=True)}
{block("Routing", "Send each pad where it belongs", "Choose an output device for the whole app, then override it per pad. On a multi-channel interface you can pick the exact output channels for each pad.", [
        "<strong>Per-pad output device</strong>: effects to the monitors, music to the stream.",
        "<strong>Channel mapping</strong> for interfaces with more than two outputs.",
        "<strong>Virtual devices</strong> such as BlackHole or VB-Cable let you feed PadVibe into OBS, Zoom or a DAW.",
        "If a device changes while the app is open, PadVibe re-resolves it and falls back to your system default instead of going silent."])}
{block("Show tools", "Built for running a show", "A few small things make a big difference when you are live.", [
        "<strong>Tabs</strong> for scenes, episodes or segments, each with its own pads.",
        "<strong>Countdown timer</strong> that shows how much of the playing audio is left, with a detachable floating window.",
        "<strong>Background pads</strong> for long beds, kept out of the timer and the API.",
        "<strong>Level meters</strong> with independent left and right peak and RMS.",
        "<strong>Light and dark themes</strong> that follow your system.",
        "A <strong>responsive layout</strong>: the mixer tucks into a side panel when the window is narrow."])}
{block("Integration", "Connect it to the rest of your setup", "PadVibe exposes what is happening, and lets other tools drive it. See the <a href='/developers/'>developer docs</a> for every endpoint.", [
        "<strong>Local HTTP API</strong> on port 9696: state, levels, timer, play, stop, volume, seek, tabs, faders, audio and MIDI devices.",
        "<strong>Webhook</strong>: PadVibe posts its full state as JSON to a URL you choose, about once a second.",
        "<strong>Timer overlay</strong>: a ready-made page for an OBS Browser Source, fed by a WebSocket.",
        "Works with anything that can open a URL, including automation tools and button decks."])}
{block("Reliability", "An engine that looks after itself", "PadVibe runs its audio and MIDI in a separate background process, so a problem there cannot freeze the interface.", [
        "If the audio engine stops responding, PadVibe restarts it and reconnects automatically.",
        "Detailed logs are written for every launch, with crash dumps, so problems are easy to diagnose.",
        "Your files are copied into PadVibe's own library: moving or renaming the original never breaks a pad. Clearing a pad cleans up its copy.",
        "No network access is needed to use it."])}
{cta_band()}'''
    return page("/features/", "PadVibe Features: MIDI Learn, Faders, Output Routing & API",
                "Explore PadVibe: instant playback, MIDI learn with RODECaster Pro support, mixer faders, per-pad output routing, level meters, a countdown timer and a local API.",
                body, og="features", current="/features/",
                schema=[breadcrumbs([("Home", "/"), ("Features", "/features/")])])


# ── Use cases ───────────────────────────────────────────────────────────────

def usecase_hub():
    items = [
        ("mic", COLORS[2], "Podcasting", "Intros, stingers and beds without leaving the mic.", "/use-cases/podcasting/"),
        ("stream", COLORS[5], "Streaming", "Effects and alerts from a key, a MIDI pad or a URL.", "/use-cases/streaming/"),
        ("theatre", COLORS[4], "Theatre and live events", "Scene banks, a countdown timer and output routing.", "/use-cases/theatre/"),
    ]
    cards = "".join(f'<a class="card" href="{u}">{ico(i, c)}<h3>{t}</h3><p>{d}</p><span class="more">Read more &rarr;</span></a>' for i, c, t, d, u in items)
    body = f'''<section class="page-hero"><div class="container">{crumbs(("Home", "/"), ("Use cases", None))}
<h1>Where PadVibe fits</h1><p class="lead">Anywhere you need sound on demand while your hands and attention are busy.</p></div></section>
<section class="section"><div class="container"><div class="grid g3">{cards}</div></div></section>{cta_band()}'''
    return page("/use-cases/", "PadVibe Use Cases: Podcasting, Streaming, Live Events",
                "See how podcasters, streamers and live-event crews use PadVibe, a free soundboard with MIDI control and per-pad output routing.",
                body, og="default", current="/use-cases/",
                schema=[breadcrumbs([("Home", "/"), ("Use cases", "/use-cases/")])])


def usecase(slug, title, seo_title, desc, h1, lead, why, steps, tips, faq_items, og, note=None):
    steps_html = "".join(f'<div class="step"><h3>{t}</h3><p>{d}</p></div>' for t, d in steps)
    tips_html = "".join(f"<li>{t}</li>" for t in tips)
    why_html = "".join(f"<p>{p}</p>" for p in why)
    note_html = f'<div class="callout warn"><strong>Good to know.</strong> {note}</div>' if note else ""
    body = f'''<section class="page-hero"><div class="container">{crumbs(("Home", "/"), ("Use cases", "/use-cases/"), (title, None))}
<h1>{h1}</h1><p class="lead">{lead}</p>
<div class="cta-row"><a class="btn btn-primary btn-lg" href="/download/">{DL_ICON} Download PadVibe</a><a class="btn btn-lg" href="/features/">See all features</a></div></div></section>
<section class="section"><div class="container"><div class="split">
<div class="prose">{why_html}{note_html}</div>
<div>{shot("home", f"PadVibe pad grid set up for {title.lower()}", 1440, 900, small=True)}</div></div></div></section>
<section class="section alt"><div class="container"><div class="section-head"><span class="eyebrow">Set up</span><h2>A working setup in five minutes</h2></div>
<div class="steps">{steps_html}</div></div></section>
<section class="section"><div class="narrow prose"><h2>Tips from the way PadVibe works</h2><ul>{tips_html}</ul></div></section>
<section class="section alt"><div class="narrow"><div class="section-head center"><span class="eyebrow">FAQ</span><h2>Common questions</h2></div>{faq(faq_items)}</div></section>
{cta_band()}'''
    return page(f"/use-cases/{slug}/", seo_title, desc, body, og=og, current="/use-cases/",
                schema=[breadcrumbs([("Home", "/"), ("Use cases", "/use-cases/"), (title, f"/use-cases/{slug}/")]),
                        faq_schema([(q, plain(a)) for q, a in faq_items])])


def usecases():
    pod = usecase(
        "podcasting", "Podcasting", "Podcast Soundboard App for Intros, Stingers & Beds | PadVibe",
        "A free soundboard for podcasters. Fire intros, outros, stingers and music beds from pads, keys or a MIDI controller, and route each to the right output.",
        "A soundboard for podcasters", "Keep your intros, stingers and music beds one tap away, so the show keeps its rhythm and you keep your focus.",
        ["Editing jingles into a recording takes time. Playing them live as you talk keeps the pacing natural and saves the edit.",
         "PadVibe gives every sound its own pad. Loop a music bed, fire a stinger on a key press, and fade levels with a fader mapped to a hardware slider. If you use a RODECaster Pro, its pads can trigger PadVibe over MIDI."],
        [("Add your sounds", "Drop your intro, outro, stingers and beds onto pads. Name and colour them so you can find them at a glance."),
         ("Set loops and levels", "Turn on Loop for beds. Link beds to a Music fader and effects to an Effects fader."),
         ("Choose triggers and output", "Assign keys or learn MIDI notes. Pick the output that feeds your mixer or recorder.")],
        ["Put long beds on a <strong>looping pad</strong>, mark it as a <strong>background pad</strong>, and link it to a <strong>Music fader</strong> so you can duck it under your voice.",
         "Use <strong>tabs</strong> to keep a bank per segment or episode.",
         "Use the <strong>countdown timer</strong> to see how much of a clip is left before you need to speak.",
         "To record PadVibe together with your voice, send it to a mixer channel on your audio interface, or capture a virtual device such as BlackHole or VB-Cable in your recording software.",
         "Keyboard keys work while PadVibe is the active window. For hands-free triggering, use a MIDI controller."],
        [("Does PadVibe record my podcast?", "No. PadVibe plays sound. Record with your usual software and feed PadVibe into it through your audio interface or a virtual audio device."),
         ("Which file types work?", "MP3, WAV, OGG and FLAC."),
         ("Can I trigger sounds from my RODECaster Pro?", "Yes. PadVibe supports RODECaster Pro pad messages over MIDI, so its pads can trigger PadVibe pads."),
         ("Is it really free?", "Yes. There is no account, subscription or paid tier.")],
        "podcasting")
    strm = usecase(
        "streaming", "Streaming", "Soundboard for Twitch & YouTube Streamers | PadVibe",
        "A free soundboard for streamers. Trigger sound effects from keys, a MIDI pad or a URL, send them into OBS with a virtual audio device, and show a countdown overlay.",
        "A soundboard for streamers", "Sound effects, stingers and reactions on demand, from a keyboard, a MIDI pad or a link, without alt-tabbing out of your game.",
        ["Good timing makes a sound effect land. PadVibe plays from memory the instant you trigger it, and it can be triggered from places that do not need the PadVibe window in front.",
         "Use a MIDI controller or any button deck that can open a URL, and fire pads while another app has focus."],
        [("Add your effects", "Drop sounds onto pads and set the output you want."),
         ("Feed your stream", "Choose a virtual audio device (BlackHole on macOS, VB-Cable on Windows) as the pad output, then add that device as an audio source in OBS. A separate output can stay on your headphones."),
         ("Trigger hands-free", "Learn MIDI notes, or call <code>http://localhost:9696/play/0</code> from a button that opens a URL.")],
        ["The <strong>local API</strong> lets other tools press pads: <code>/play/{index}</code>, <code>/stop/{index}</code> and <code>/stop_all</code>.",
         "Add the <strong>timer overlay</strong> as an OBS Browser Source: <code>http://localhost:9696/overlay/timer</code>. You can set <code>size</code>, <code>color</code> and <code>bg</code> in the URL.",
         "Use <strong>per-pad output routing</strong> to keep private cues on your headphones and public sounds on the stream.",
         "<strong>Background pads</strong> are left out of the API state, which keeps stream automations simple."],
        [("Does it work with OBS?", "Yes. Send PadVibe to a virtual audio device and capture that device in OBS, or capture the output device directly. The countdown overlay runs as a Browser Source."),
         ("Can I trigger sounds while a game is focused?", "Use a MIDI controller or the local API. Keyboard keys work when the PadVibe window is active."),
         ("Is there a Stream Deck plugin?", "There is no plugin. Anything that can open a URL can control PadVibe through the local API."),
         ("Does it cost anything?", "No. It is free and open source.")],
        "streaming",
        note="PadVibe does not capture or mix game audio. It plays your sounds to the output you choose.")
    th = usecase(
        "theatre", "Theatre and live events", "Sound Cue Software for Theatre & Live Events | PadVibe",
        "A free pad-based sound player for theatre, schools and live events. Scene banks, a countdown timer, looping beds and per-pad output routing.",
        "Sound cues for theatre and live events", "Scene banks, looping ambience and per-pad outputs, on a screen you can read from the back of the booth.",
        ["For small productions, schools, churches and events, a pad per cue is often all you need. PadVibe puts every cue on a clearly named, colour-coded pad, with a tab for each scene.",
         "Route front-of-house sounds and on-stage monitors to different channels of a multi-channel interface, and keep ambience on a looping pad with its own fader."],
        [("Build a bank per scene", "Create a tab for each scene or act and name the pads after the cues."),
         ("Set levels and loops", "Loop ambience, set each pad's volume, and link groups to faders."),
         ("Route outputs", "Choose the output device or channels each cue should use, then test each one.")],
        ["Use the <strong>floating countdown timer</strong> to see how much of the playing cue remains.",
         "Pads can be triggered from a <strong>MIDI controller</strong>, which many operators prefer to a mouse.",
         "Move between scenes with tabs. Switching tabs stops running sounds, so the next scene starts clean.",
         "PadVibe copies audio into its own library, so a pad keeps working if the original file moves.",
         "Rehearse with your real audio interface connected: device names and channel counts come from the system."],
        [("Is PadVibe a cue-list sequencer?", "No. It is a pad-based player: you trigger each cue yourself. There is no timeline or automatic follow-on cue."),
         ("How reliable is it?", "The audio runs in a separate process that PadVibe restarts automatically if it stops responding, and detailed logs are kept. As with any live system, rehearse with your actual setup."),
         ("Can I use several audio outputs?", "Yes. Each pad can use its own output device and, on multi-channel interfaces, its own channels."),
         ("Is it free for schools and churches?", "Yes. PadVibe is free to download and use.")],
        "theatre",
        note="PadVibe has not been audited for safety-critical use. Always have a backup plan for live shows.")
    return [pod, strm, th]


# ── Download ────────────────────────────────────────────────────────────────

DL_FAQ = [
    ("Is PadVibe free to download?", "Yes. It is free, with no account or subscription."),
    ("Why does macOS or Windows warn me when I open it?", "PadVibe is not yet code-signed with a paid developer certificate, so the system asks you to confirm. On macOS, right-click the app and choose Open. On Windows, choose More info, then Run anyway."),
    ("Which macOS version do I need?", "PadVibe is built for macOS 10.15 (Catalina) and later, on Apple Silicon and Intel Macs. It has been tested on macOS 15 and 26. If a download will not open, tell us on GitHub."),
    ("Where does PadVibe store its data?", "In your user account's application support folder: your pad layout, a copy of your audio files and log files. Nothing is sent anywhere."),
]


def download():
    cards = f'''<div class="grid g3">
<div class="card os-card" id="macos">{ico("monitor", COLORS[4])}<h3>macOS</h3><p>Apple Silicon and Intel. Open the DMG and drag PadVibe to Applications.</p>
<a class="btn btn-primary" href="{REPO}/releases/latest" data-dl="mac-arm">{DL_ICON} Apple Silicon (.dmg)</a>
<a class="btn" style="margin-top:10px" href="{REPO}/releases/latest" data-dl="mac-intel">{DL_ICON} Intel (.dmg)</a>
<span class="alt">Not sure? Apple menu &rarr; About This Mac. "Chip: Apple" means Apple Silicon.</span></div>
<div class="card os-card" id="windows">{ico("monitor", COLORS[1])}<h3>Windows</h3><p>Windows 10 and 11, 64-bit. Unzip and run <code>pads.exe</code>.</p>
<a class="btn btn-primary" href="{REPO}/releases/latest" data-dl="windows">{DL_ICON} Download (.zip)</a></div>
<div class="card os-card" id="linux">{ico("monitor", COLORS[2])}<h3>Linux</h3><p>64-bit. Extract the archive and run <code>bundle/pads</code>.</p>
<a class="btn btn-primary" href="{REPO}/releases/latest" data-dl="linux">{DL_ICON} Download (.tar.gz)</a>
<span class="alt">Needs GTK 3 and ALSA or PulseAudio/PipeWire.</span></div>
</div>'''
    body = f'''<section class="page-hero"><div class="container">{crumbs(("Home", "/"), ("Download", None))}
<h1>Download PadVibe</h1>
<p class="lead">Free for macOS, Windows and Linux. Current release: <strong data-version>see releases</strong>.</p></div></section>
<section class="section" style="padding-top:20px"><div class="container">{cards}
<p class="fine" style="margin-top:16px">All downloads come from <a href="{REPO}/releases/latest" rel="noopener">GitHub Releases</a>. Each release lists what changed.</p></div></section>

<section class="section alt"><div class="narrow prose">
<h2>Install on macOS with Homebrew</h2>
<p>If you use Homebrew, one command installs PadVibe and keeps it updatable:</p>
<div class="codewrap"><button class="copy" type="button">Copy</button><pre><code>brew tap shabeer-wms/padvibe
brew install --cask padvibe</code></pre></div>
<h2>First launch</h2>
<p>The first time you open a new version, macOS checks the app, so it can take about 15 seconds to start. Later launches take about a second.</p>
<div class="callout warn"><strong>"Cannot be opened because the developer cannot be verified"?</strong> PadVibe is not yet signed with a paid Apple Developer certificate. Right-click PadVibe in Applications, choose <strong>Open</strong>, then confirm. Or run <code>xattr -dr com.apple.quarantine /Applications/PadVibe.app</code> in Terminal.</div>
<div class="callout warn"><strong>Windows SmartScreen.</strong> Choose <strong>More info</strong>, then <strong>Run anyway</strong>.</div>
<h2>Linux notes</h2>
<p>Install GTK 3 and an audio stack (ALSA, PulseAudio or PipeWire). Then extract the archive and run <code>./bundle/pads</code>.</p>
<h2>System requirements</h2>
<ul><li>macOS 10.15 or later (Apple Silicon or Intel), Windows 10 or 11 (64-bit), or a 64-bit Linux desktop.</li><li>Roughly 100 to 250 MB of disk space depending on the platform, plus your audio files.</li><li>An audio output device. MIDI is optional.</li></ul>
<h2>Your data stays with you</h2>
<p>PadVibe needs no account and makes no network requests to use. Read the <a href="/privacy/">privacy page</a>.</p>
</div></section>
<section class="section"><div class="narrow"><div class="section-head center"><span class="eyebrow">FAQ</span><h2>Download questions</h2></div>{faq(DL_FAQ)}</div></section>'''
    schema = [breadcrumbs([("Home", "/"), ("Download", "/download/")]), software_schema(),
              faq_schema([(q, plain(a)) for q, a in DL_FAQ])]
    return page("/download/", "Download PadVibe: Free Soundboard for Mac, Windows & Linux",
                "Download PadVibe for free. Installers for macOS (Apple Silicon and Intel), Windows and Linux, plus a Homebrew command. No account needed.",
                body, og="download", current="/download/", schema=schema)


# ── Developers ──────────────────────────────────────────────────────────────

ENDPOINTS = [
    ("/state", "Full snapshot: global state (timer, master volume and levels, active tab, output device) and every non-background pad."),
    ("/levels", "Master levels: <code>rms_l</code>, <code>rms_r</code>, <code>peak_l</code>, <code>peak_r</code>."),
    ("/timer", "Remaining time of the playing audio: <code>remaining_seconds</code>, <code>formatted_remaining_timer</code> and an estimated completion time."),
    ("/overlay/timer", "A countdown page for OBS Browser Sources. Optional query: <code>size</code>, <code>color</code>, <code>bg</code>, <code>host</code>, <code>port</code>."),
    ("/play/{index}", "Play (or resume) the pad at <code>index</code> in the active tab."),
    ("/stop/{index}", "Stop that pad."),
    ("/stop_all", "Stop every pad."),
    ("/volume/master/{0-1}", "Set the master volume."),
    ("/volume/pad/{index}/{0-1}", "Set one pad's volume."),
    ("/volume/fader/{index}/{0-1}", "Set a mixer fader's volume."),
    ("/seek/{index}/{0-1}", "Seek a pad to a position, as a fraction of its length."),
    ("/groups", "List the tabs: <code>id</code>, <code>name</code>, <code>pad_count</code>."),
    ("/groups/{index}/switch", "Switch to a tab. This stops running sounds."),
    ("/faders", "List the mixer faders."),
    ("/audio/devices", "List audio output devices."),
    ("/audio/devices/{id}/select", "Choose the output device."),
    ("/midi/devices", "List MIDI input devices."),
    ("/midi/devices/{name}/connect", "Connect a MIDI input device."),
    ("/midi/refresh", "Rescan MIDI devices."),
]


def developers():
    rows = "".join(f"<tr><td><code>GET {p}</code></td><td>{d}</td></tr>" for p, d in ENDPOINTS)
    body = f'''<section class="page-hero"><div class="container">{crumbs(("Home", "/"), ("Developers", None))}
<h1>Local API and integrations</h1>
<p class="lead">PadVibe serves a small HTTP API on your own machine. Read its state, trigger pads, or have it call your server.</p></div></section>
<section class="section" style="padding-top:20px"><div class="narrow prose">
<div class="callout warn"><strong>Security.</strong> The API has no password, allows requests from any web page (CORS is open) and listens on all network interfaces. Use it on trusted networks only, and close PadVibe when you do not need it.</div>
<h2>Base URL</h2>
<p>PadVibe listens on port <code>9696</code>. From the same computer use <code>http://localhost:9696</code>. From another device use the computer's address, shown in <strong>Settings &rarr; Integrations</strong>.</p>
<div class="codewrap"><button class="copy" type="button">Copy</button><pre><code>curl http://localhost:9696/state
curl http://localhost:9696/play/0
curl http://localhost:9696/volume/pad/0/0.5
curl http://localhost:9696/stop_all</code></pre></div>
<h2>Endpoints</h2>
<p>All endpoints use <code>GET</code>. Indexes are zero-based positions within the active tab. Volumes and positions are numbers from 0 to 1.</p>
</div>
<div class="container" style="margin-top:20px"><div class="table-wrap"><table><thead><tr><th>Endpoint</th><th>What it does</th></tr></thead><tbody>{rows}</tbody></table></div></div>
<div class="narrow prose">
<h2>State example</h2>
<p><code>/state</code> returns a <code>global</code> object and a <code>pads</code> array. Pads marked as background are left out.</p>
<div class="codewrap"><button class="copy" type="button">Copy</button><pre><code>{{
  "global": {{
    "remaining_timer_seconds": 133.0,
    "formatted_remaining_timer": "02:13",
    "master_volume": 1.0,
    "master_volume_levels": {{ "left": 0.31, "right": 0.29 }},
    "active_group": {{ "index": 0, "id": "default", "name": "Podcast" }},
    "audio_device": {{ "id": 0, "name": "Studio Monitors" }}
  }},
  "pads": [
    {{
      "id": 4,
      "name": "Rimshot",
      "keyboard_shortcut": null,
      "settings": {{ "is_looping": false }},
      "playback": {{ "state": "playing", "position_seconds": 1.2,
                    "duration_seconds": 3.4, "progress_percent": 0.35 }}
    }}
  ]
}}</code></pre></div>
<p>Playback <code>state</code> is one of <code>empty</code>, <code>stopped</code>, <code>playing</code> or <code>paused</code>.</p>
<h2>Webhook</h2>
<p>In <strong>Settings &rarr; Integrations</strong>, enter a URL. PadVibe then sends the same JSON as <code>/state</code> to it with an HTTP <code>POST</code> about once a second. Leave it empty to turn the webhook off.</p>
<h2>Timer over WebSocket</h2>
<p>Connect to <code>ws://localhost:9697</code> to receive the countdown twice a second:</p>
<div class="codewrap"><button class="copy" type="button">Copy</button><pre><code>{{"remaining_seconds": 133.0, "formatted": "02:13"}}</code></pre></div>
<h2>Show the countdown in OBS</h2>
<p>Add a <strong>Browser Source</strong> and use this URL. Adjust the look with query parameters.</p>
<div class="codewrap"><button class="copy" type="button">Copy</button><pre><code>http://localhost:9696/overlay/timer?size=120&amp;color=ffffff&amp;bg=transparent</code></pre></div>
<h2>Under the hood</h2>
<p>PadVibe is a Flutter app. Audio and MIDI run in a separate Python process that the app starts and supervises, and the two talk over a local WebSocket. The code is on <a href="{REPO}" rel="noopener">GitHub</a>. Bug reports and pull requests are welcome.</p>
</div></section>{cta_band("Build something with it", "Found something missing from the API? Open an issue and tell us what you are building.")}'''
    return page("/developers/", "PadVibe Local API: Control Your Soundboard Over HTTP",
                "Documentation for PadVibe's local HTTP API, webhook, WebSocket timer and OBS timer overlay. Trigger pads and read state from any tool.",
                body, og="developers", current="/developers/",
                schema=[breadcrumbs([("Home", "/"), ("Developers", "/developers/")])])


# ── Changelog ───────────────────────────────────────────────────────────────

RELEASES = [
    ("1.10.0", "2026-10-17", [
        "Much faster start: the audio engine starts in about a second after the first launch (it took around 20 seconds).",
        "Redesigned interface: a sectioned Settings dialog, one tabbed Pad settings dialog, a four-item pad menu, refreshed light and dark themes and colourful pads.",
        "Responsive layout: the mixer moves into a side panel and the grid adapts when the window is narrow.",
        "Windows and Linux builds, alongside separate macOS builds for Apple Silicon and Intel.",
        "Audio is decoded once and shared by playback and waveforms, and a pad's copy is cleaned up when you clear it.",
        "The audio engine restarts itself if it stops responding, recovers from audio-device changes, and keeps detailed logs.",
        "Fixed: a second click on a starting pad no longer stacks duplicate sounds.",
        "Fixed: opening PadVibe a second time no longer crashes the copy that is already running.",
    ]),
    ("1.9.0", "2026-05-23", ["MIDI program change support.", "WebSocket timer overlay for OBS.", "Homebrew tap: <code>brew install --cask padvibe</code>."]),
    ("1.8.0", "2026-04-15", ["Stability fix for a freezing issue."]),
    ("1.7.0", "2026-02-16", ["Dark mode.", "Performance and audio engine improvements."]),
    ("1.6.0", "", ["RODECaster Pro MIDI support.", "Mixer panel with faders.", "Background pads.", "SQLite storage for pads and settings."]),
]


def changelog():
    sections = "".join(
        f'<section class="card" style="margin-bottom:16px"><h2 style="font-size:1.4rem">{v} <span class="fine" style="font-size:0.9rem;font-weight:500">{d}</span></h2><ul class="checks">'
        + "".join(f"<li>{i}</li>" for i in items) + "</ul></section>" for v, d, items in RELEASES)
    body = f'''<section class="page-hero"><div class="container">{crumbs(("Home", "/"), ("Changelog", None))}
<h1>Changelog</h1><p class="lead">What changed in each release. Full notes and downloads are on <a href="{REPO}/releases" rel="noopener">GitHub Releases</a>.</p></div></section>
<section class="section" style="padding-top:20px"><div class="narrow">{sections}</div></section>{cta_band()}'''
    return page("/changelog/", "PadVibe Changelog: Release Notes & What's New",
                "Release notes for PadVibe: what is new in 1.10 and earlier versions of the free soundboard.",
                body, og="default", current="/changelog/",
                schema=[breadcrumbs([("Home", "/"), ("Changelog", "/changelog/")])])


# ── Press ───────────────────────────────────────────────────────────────────

def press():
    shots = "".join(
        f'<a class="card" href="{u}" download><img src="{u}" width="{w}" height="{h}" alt="{esc(a)}" loading="lazy" style="border-radius:10px;margin-bottom:12px"><p>{a}</p></a>'
        for u, w, h, a in [
            ("/assets/img/app-home-dark.webp", 1440, 900, "Main window, dark theme"),
            ("/assets/img/app-home-light.webp", 1440, 900, "Main window, light theme"),
            ("/assets/img/app-pad-settings-dark.webp", 640, 470, "Pad settings"),
            ("/assets/img/app-settings-dark.webp", 1100, 760, "Settings")])
    social = "".join(
        f'<a class="card" href="/assets/og/{n}.png" download><img src="/assets/og/{n}.png" width="1200" height="630" alt="{a}" loading="lazy" style="border-radius:10px;margin-bottom:12px"><p>{a}</p></a>'
        for n, a in [("default", "Social card"), ("features", "Features card")])
    body = f'''<section class="page-hero"><div class="container">{crumbs(("Home", "/"), ("Press kit", None))}
<h1>Press kit</h1><p class="lead">Everything you need to write about PadVibe. All assets are free to use when covering the app.</p></div></section>
<section class="section" style="padding-top:20px"><div class="narrow prose">
<h2>About PadVibe</h2>
<p><strong>One line:</strong> PadVibe is a free, open source soundboard for macOS, Windows and Linux, built for podcasters, streamers and live shows.</p>
<p><strong>Short description:</strong> PadVibe lets you drop audio files onto colourful pads and play them instantly with a click, a keyboard key, a MIDI controller or a URL. It offers MIDI learn with RODECaster Pro support, mixer faders, per-pad output routing, level meters, a countdown timer and a local HTTP API.</p>
<h2>Key facts</h2>
<ul><li><strong>Price:</strong> free, no account.</li><li><strong>Platforms:</strong> macOS (Apple Silicon and Intel), Windows 10 and 11, Linux.</li><li><strong>Formats:</strong> MP3, WAV, OGG, FLAC.</li><li><strong>Built with:</strong> Flutter, with a Python audio and MIDI engine.</li><li><strong>Source:</strong> <a href="{REPO}" rel="noopener">github.com/shabeer-wms/padvibe</a></li><li><strong>Contact:</strong> open an issue on <a href="{REPO}/issues" rel="noopener">GitHub</a>.</li></ul>
<h2>Logo</h2>
<p><a href="/assets/icons/logo-mark.svg" download>Logo mark (SVG)</a> &middot; <a href="/assets/icons/icon-512.png" download>App icon (PNG, 512 px)</a></p>
</div>
<div class="container" style="margin-top:20px"><h2>Screenshots</h2><div class="grid g2" style="margin-top:16px">{shots}</div><h2 style="margin-top:36px">Social cards</h2><div class="grid g2" style="margin-top:16px">{social}</div></div></section>{cta_band()}'''
    return page("/press/", "PadVibe Press Kit: Logos, Screenshots & Facts",
                "Press kit for PadVibe, the free soundboard for podcasters, streamers and live shows: descriptions, key facts, logos and screenshots.",
                body, og="press", current="",
                schema=[breadcrumbs([("Home", "/"), ("Press kit", "/press/")])])


# ── Legal ───────────────────────────────────────────────────────────────────

def privacy():
    body = f'''<section class="page-hero"><div class="container">{crumbs(("Home", "/"), ("Privacy", None))}<h1>Privacy</h1><p class="lead">The short version: PadVibe does not collect your data.</p></div></section>
<section class="section" style="padding-top:20px"><div class="narrow prose">
<p><em>Last updated: 17 October 2026.</em></p>
<h2>The app</h2>
<ul><li>PadVibe has no accounts, no analytics and no advertising.</li><li>Your pad layout, settings and a copy of your audio files are stored on your computer, in your user account's application support folder.</li><li>PadVibe writes log files to the same folder to help diagnose problems. They stay on your computer. If you send one to us for support, you choose to.</li><li>The app does not need the internet to work. The local API and webhook only talk to addresses you configure. The webhook is off until you enter a URL.</li></ul>
<h2>This website</h2>
<ul><li>No cookies and no analytics or tracking scripts.</li><li>Your theme choice (light or dark) is saved in your browser's local storage, and nowhere else.</li><li>The download page asks GitHub for the latest release so it can show the right download links. GitHub sees that request, as with any request to its API.</li><li>Our hosting provider may keep standard server logs, such as IP addresses, for security and operation.</li></ul>
<h2>Third parties</h2>
<p>Downloads are served by <a href="{REPO}/releases" rel="noopener">GitHub</a>, and Homebrew installs are served by the Homebrew project. Their own privacy policies apply to those services.</p>
<h2>Contact</h2>
<p>Questions about privacy? Open an issue on <a href="{REPO}/issues" rel="noopener">GitHub</a>.</p>
</div></section>'''
    return page("/privacy/", "Privacy Policy | PadVibe",
                "PadVibe collects no personal data: no accounts, no analytics and no tracking. Read how the app and this website handle information.",
                body, og="default", schema=[breadcrumbs([("Home", "/"), ("Privacy", "/privacy/")])])


def terms():
    body = f'''<section class="page-hero"><div class="container">{crumbs(("Home", "/"), ("Terms", None))}<h1>Terms of use</h1><p class="lead">Plain terms for using the PadVibe app and this website.</p></div></section>
<section class="section" style="padding-top:20px"><div class="narrow prose">
<p><em>Last updated: 17 October 2026.</em></p>
<h2>Using PadVibe</h2>
<p>PadVibe is free to download and use. Its source code is in the <a href="{REPO}" rel="noopener">GitHub repository</a>; see the repository for licence details.</p>
<h2>Your content</h2>
<p>You are responsible for the audio you play with PadVibe, including having the rights to use it. PadVibe does not upload your audio anywhere.</p>
<h2>No warranty</h2>
<p>PadVibe is provided "as is", without warranty of any kind. Audio software can fail: for live or important events, rehearse with your actual setup and keep a backup. We are not liable for losses arising from its use, to the extent the law allows.</p>
<h2>The local API</h2>
<p>The local API is unauthenticated. You are responsible for who can reach it on your network.</p>
<h2>This website</h2>
<p>Content on this site is provided for information. Product and company names are trademarks of their owners and are used only to describe compatibility.</p>
<h2>Changes and contact</h2>
<p>We may update these terms. The date above shows the latest version. Questions? Open an issue on <a href="{REPO}/issues" rel="noopener">GitHub</a>.</p>
</div></section>'''
    return page("/terms/", "Terms of Use | PadVibe",
                "Plain-language terms for using the PadVibe soundboard app and this website, including the local API and your responsibilities.",
                body, og="default", schema=[breadcrumbs([("Home", "/"), ("Terms", "/terms/")])])


def not_found():
    body = '''<section class="page-hero"><div class="narrow" style="text-align:center;padding:60px 0">
<h1>That page is not here</h1><p class="lead" style="margin-inline:auto">The link may be old or mistyped.</p>
<div class="cta-row" style="justify-content:center"><a class="btn btn-primary btn-lg" href="/">Go home</a><a class="btn btn-lg" href="/download/">Download PadVibe</a></div></div></section>'''
    return page("/404.html", "Page not found | PadVibe", "This page could not be found.", body, noindex=True)


def all_pages():
    pages = {
        "index.html": home(), "features/index.html": features(), "use-cases/index.html": usecase_hub(),
        "download/index.html": download(), "developers/index.html": developers(), "changelog/index.html": changelog(),
        "press/index.html": press(), "privacy/index.html": privacy(), "terms/index.html": terms(), "404.html": not_found(),
    }
    for slug, content in zip(["podcasting", "streaming", "theatre"], usecases()):
        pages[f"use-cases/{slug}/index.html"] = content
    return pages
