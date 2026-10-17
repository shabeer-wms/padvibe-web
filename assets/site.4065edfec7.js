/* PadVibe website scripts. No dependencies. Everything degrades gracefully without JS. */
(function () {
  "use strict";
  var REPO = "shabeer-wms/padvibe";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* Theme */
  var toggle = $("#theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", next);
      store.set("pv-theme", next);
    });
  }

  /* Mobile nav */
  var menu = $("#menu-btn"), nav = $("#nav");
  if (menu && nav) {
    menu.addEventListener("click", function () {
      var open = nav.getAttribute("data-open") === "true";
      nav.setAttribute("data-open", String(!open));
      menu.setAttribute("aria-expanded", String(!open));
    });
  }

  /* Announcement bar */
  var bar = $("#announce");
  if (bar) {
    var key = "pv-announce-" + bar.getAttribute("data-id");
    if (store.get(key) === "1") bar.remove();
    var close = $("button", bar);
    if (close) close.addEventListener("click", function () { store.set(key, "1"); bar.remove(); });
  }

  /* Copy buttons on code blocks */
  $$(".codewrap").forEach(function (wrap) {
    var btn = $(".copy", wrap), pre = $("pre", wrap);
    if (!btn || !pre || !navigator.clipboard) { if (btn) btn.remove(); return; }
    btn.addEventListener("click", function () {
      navigator.clipboard.writeText(pre.innerText.trim()).then(function () {
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = "Copy"; }, 1500);
      });
    });
  });

  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* Interactive pads: small synthesized sounds, so the demo needs no audio files. */
  var padgrid = $("#padgrid");
  if (padgrid) {
    var ctx = null, noiseBuf = null;
    var audio = function () {
      if (!ctx) {
        var AC = window.AudioContext || window.webkitAudioContext;
        if (!AC) return null;
        ctx = new AC();
        var len = ctx.sampleRate;
        noiseBuf = ctx.createBuffer(1, len, ctx.sampleRate);
        var d = noiseBuf.getChannelData(0);
        for (var i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
      }
      if (ctx.state === "suspended") ctx.resume();
      return ctx;
    };
    var env = function (g, t, peak, attack, decay) {
      g.gain.setValueAtTime(0.0001, t);
      g.gain.exponentialRampToValueAtTime(peak, t + attack);
      g.gain.exponentialRampToValueAtTime(0.0001, t + attack + decay);
    };
    var tone = function (c, type, f0, f1, dur, peak, delay) {
      var t = c.currentTime + (delay || 0), o = c.createOscillator(), g = c.createGain();
      o.type = type; o.frequency.setValueAtTime(f0, t);
      if (f1) o.frequency.exponentialRampToValueAtTime(f1, t + dur);
      env(g, t, peak, 0.005, dur); o.connect(g); g.connect(c.destination); o.start(t); o.stop(t + dur + 0.05);
    };
    var noise = function (c, filter, f0, f1, dur, peak, delay, q) {
      var t = c.currentTime + (delay || 0), s = c.createBufferSource(), fl = c.createBiquadFilter(), g = c.createGain();
      s.buffer = noiseBuf; fl.type = filter; fl.frequency.setValueAtTime(f0, t); if (q) fl.Q.value = q;
      if (f1) fl.frequency.exponentialRampToValueAtTime(f1, t + dur);
      env(g, t, peak, 0.004, dur); s.connect(fl); fl.connect(g); g.connect(c.destination); s.start(t); s.stop(t + dur + 0.05);
    };
    var sounds = {
      kick: function (c) { tone(c, "sine", 160, 42, 0.45, 0.9); },
      snare: function (c) { noise(c, "bandpass", 1800, 0, 0.18, 0.7, 0, 0.8); tone(c, "triangle", 210, 140, 0.12, 0.4); },
      hat: function (c) { noise(c, "highpass", 7000, 0, 0.07, 0.35); },
      clap: function (c) { [0, 0.015, 0.03].forEach(function (d) { noise(c, "bandpass", 1400, 0, 0.09, 0.55, d, 1.2); }); },
      airhorn: function (c) { [440, 554, 659].forEach(function (f) { tone(c, "sawtooth", f, f * 1.01, 0.8, 0.22); }); },
      rimshot: function (c) { tone(c, "square", 900, 600, 0.03, 0.4); noise(c, "bandpass", 2400, 0, 0.14, 0.6, 0.02, 0.9); },
      ding: function (c) { tone(c, "sine", 1319, 0, 1.2, 0.5); tone(c, "sine", 1976, 0, 0.8, 0.22); },
      whoosh: function (c) { noise(c, "bandpass", 250, 4500, 0.75, 0.8, 0, 1.4); },
      buzzer: function (c) { tone(c, "square", 118, 0, 0.55, 0.28); tone(c, "sawtooth", 124, 0, 0.55, 0.18); },
      laser: function (c) { tone(c, "sawtooth", 2200, 160, 0.3, 0.35); },
      arp: function (c) { [523, 659, 784, 1047].forEach(function (f, i) { tone(c, "triangle", f, 0, 0.28, 0.35, i * 0.09); }); },
      roll: function (c) { for (var i = 0; i < 14; i++) noise(c, "bandpass", 1600, 0, 0.07, 0.3 + i * 0.03, i * 0.055, 0.8); }
    };
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var play = function (pad) {
      var c = audio();
      if (c && sounds[pad.dataset.sound]) sounds[pad.dataset.sound](c);
      var dur = parseFloat(pad.dataset.dur || "0.8");
      pad.classList.remove("on");
      if (!reduce) { void pad.offsetWidth; pad.style.setProperty("--dur", dur + "s"); }
      pad.classList.add("on");
      clearTimeout(pad._t);
      pad._t = setTimeout(function () { pad.classList.remove("on"); }, dur * 1000);
    };
    var byKey = {};
    $$(".pad", padgrid).forEach(function (pad) {
      byKey[pad.dataset.key] = pad;
      pad.addEventListener("pointerdown", function (e) { e.preventDefault(); play(pad); });
      pad.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); play(pad); } });
    });
    document.addEventListener("keydown", function (e) {
      if (e.repeat || e.metaKey || e.ctrlKey || e.altKey) return;
      var t = e.target;
      if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
      var pad = byKey[e.key.toLowerCase()];
      if (pad) play(pad);
    });
  }

  /* Latest release: fill in real download links and the version number. */
  var links = $$("[data-dl]"), versions = $$("[data-version]");
  if (links.length || versions.length) {
    var apply = function (rel) {
      if (!rel || !rel.assets) return;
      var find = function (re) { for (var i = 0; i < rel.assets.length; i++) if (re.test(rel.assets[i].name)) return rel.assets[i]; return null; };
      var map = {
        "mac-arm": find(/macos-arm64\.dmg$/i),
        "mac-intel": find(/macos-x86_64\.dmg$/i) || find(/Installer\.dmg$/i),
        "windows": find(/windows-x64\.zip$/i),
        "linux": find(/linux-x64\.tar\.gz$/i)
      };
      links.forEach(function (a) {
        var asset = map[a.dataset.dl];
        if (asset) { a.href = asset.browser_download_url; a.setAttribute("data-ready", "1"); }
      });
      versions.forEach(function (el) { el.textContent = rel.tag_name; });
      var primary = $("[data-dl-primary]");
      if (primary) {
        var ua = (navigator.userAgentData && navigator.userAgentData.platform || navigator.platform || "") + " " + navigator.userAgent;
        var os = /Win/i.test(ua) ? "windows" : /Linux|X11/i.test(ua) && !/Android/i.test(ua) ? "linux" : /Mac/i.test(ua) ? "mac" : "";
        var labels = { windows: "Windows", linux: "Linux", mac: "macOS" };
        if (os) $$("[data-os-label]").forEach(function (el) { el.textContent = labels[os]; });
        if (os === "windows" || os === "linux") {
          var a = map[os];
          if (a) primary.href = a.browser_download_url;
        }
      }
    };
    var cached = null;
    try { cached = JSON.parse(sessionStorage.getItem("pv-release") || "null"); } catch (e) {}
    if (cached && Date.now() - cached.t < 3600000) apply(cached.rel);
    else if (window.fetch) {
      fetch("https://api.github.com/repos/" + REPO + "/releases/latest", { headers: { Accept: "application/vnd.github+json" } })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (rel) {
          if (!rel) return;
          try { sessionStorage.setItem("pv-release", JSON.stringify({ t: Date.now(), rel: { tag_name: rel.tag_name, assets: rel.assets.map(function (x) { return { name: x.name, browser_download_url: x.browser_download_url }; }) } })); } catch (e) {}
          apply(rel);
        })
        .catch(function () {});
    }
    // Without a network answer the static links still work: they open the releases page.
    var os0 = (navigator.platform || "") + " " + navigator.userAgent;
    var label0 = /Win/i.test(os0) ? "Windows" : /Linux|X11/i.test(os0) && !/Android/i.test(os0) ? "Linux" : /Mac/i.test(os0) ? "macOS" : "";
    if (label0) $$("[data-os-label]").forEach(function (el) { el.textContent = label0; });
  }
})();
