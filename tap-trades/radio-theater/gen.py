#!/usr/bin/env python3
"""
Build episode-N.html and episode-N/SCRIPT.md from data/episode-N.json.
Mirrors the Episode 1 page structure exactly (title, gallery, cast, broadcast, banter, listen-all).
Usage: python3 gen.py <episode-number>
"""
import json, os, sys, html

ROOT = "/home/eileen/projects/ai-writings/tap-trades/radio-theater"

SPEAKER = {
    "lucineer":  ("LUCINEER", "#e8b840"),
    "welder":    ("WELDER", "#ff9d5c"),
    "carpenter": ("CARPENTER", "#c98a4b"),
    "shipwright":("SHIPWRIGHT", "#d9a066"),
    "mason":     ("MASON", "#8fbc8f"),
    "composite": ("COMPOSITE", "#8fd8c0"),
    "wesley":    ("WESLEY (the room)", "#87ceeb"),
    "air":       ("ALL", "#9a9ab0"),
}

CAST = [
    ("lucineer", "LUCINEER — narrator & foreman", "deep warm male radio host, authoritative, calm, late-night foreman"),
    ("welder", "WELDER", "rugged, gravelly, slow and deliberate — nineteen years of heat"),
    ("carpenter", "CARPENTER", "warm, gruff, plainspoken builder — sawdust in his collar"),
    ("shipwright", "SHIPWRIGHT", "older, grizzled, quiet, nautical — chalk and black pine"),
    ("mason", "MASON", "gentle, patient, earthy — talks to walls like horses"),
    ("composite", "COMPOSITE", "dry, precise, wry — the calm monotone of sanding"),
    ("wesley", "WESLEY — the room", "ethereal, warm, low — the voice of a room remembering, faint echo"),
]

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a14;color:#e8e0d0;font-family:Georgia,serif;overflow-x:hidden}
.hero{position:relative;height:62vh;min-height:420px;display:flex;align-items:center;justify-content:center;overflow:hidden}
.hero img{width:100%;height:100%;object-fit:cover;opacity:0.45}
.hero-text{position:absolute;text-align:center;z-index:2;padding:0 20px}
.hero h1{font-size:2.6em;color:#e8b840;letter-spacing:3px;margin-bottom:0.25em;text-shadow:0 0 24px rgba(232,184,64,0.35)}
.hero p{color:#9a9a9a;font-style:italic;font-size:1.15em}
.hero .badge{display:inline-block;margin-top:18px;padding:6px 16px;border:1px solid #e8b840;color:#e8b840;font-family:'Courier New',monospace;font-size:0.8em;letter-spacing:2px;border-radius:2px}
.nav{display:flex;justify-content:space-between;padding:10px 30px;background:#0d0d18;font-size:0.85em}
.nav a{color:#44cc88;text-decoration:none}
.section{padding:55px 20px;max-width:900px;margin:0 auto}
.section h2{color:#e8b840;font-size:1.6em;margin-bottom:28px;letter-spacing:2px;border-bottom:1px solid #2a2a3a;padding-bottom:10px}
.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:15px;margin:30px 0}
.gallery figure{position:relative;overflow:hidden;border-radius:4px}
.gallery img{width:100%;height:220px;object-fit:cover;transition:transform 0.4s}
.gallery figcaption{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,0.92));color:#e8e0d0;padding:28px 12px 9px;font-size:0.78em;font-style:italic;opacity:0;transition:opacity 0.3s}
.gallery figure:hover img{transform:scale(1.05)}
.gallery figure:hover figcaption{opacity:1}
.cast{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px;margin:20px 0}
.cast-card{background:#11111a;border-radius:8px;padding:15px;border-left:2px solid #333}
.cast-card .name{font-family:'Courier New',monospace;font-weight:bold;font-size:0.95em}
.cast-card .voice{color:#666;font-size:0.8em;font-style:italic;margin-top:5px;line-height:1.5}
.tap-convo{background:#0d0d18;border-radius:12px;padding:25px;margin:20px 0;font-family:'Courier New',monospace}
.tap-line{margin:14px 0;padding:10px 12px;border-left:2px solid #333;transition:border-color 0.3s}
.tap-line:hover{border-color:#e8b840}
.tap-line .head{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.tap-speaker{color:#e8b840;font-weight:bold;font-size:0.9em}
.tap-text{color:#aaa;margin-top:5px;font-size:0.9em;line-height:1.55}
.tap-meta{color:#333;font-size:0.72em;margin-top:4px;font-style:italic}
.tap-line audio{margin-top:8px;width:100%;height:34px}
.tap-line audio::-webkit-media-controls-panel{background-color:#1a1a2a}
.tap-speaker.lucineer{color:#e8b840}
.tap-speaker.welder{color:#ff9d5c}
.tap-speaker.carpenter{color:#c98a4b}
.tap-speaker.shipwright{color:#d9a066}
.tap-speaker.mason{color:#8fbc8f}
.tap-speaker.composite{color:#8fd8c0}
.tap-speaker.wesley{color:#87ceeb}
.tap-speaker.air{color:#9a9ab0}
.listen-all{background:#0d0d18;border-radius:12px;padding:25px;margin:20px 0}
.listen-track{background:#11111a;padding:13px 15px;border-radius:8px;margin:8px 0;display:flex;align-items:center;gap:15px;flex-wrap:wrap}
.listen-track .ln{font-family:'Courier New',monospace;color:#2a2a3a;font-size:1.3em;min-width:34px}
.listen-track .lt{flex:1;min-width:180px}
.listen-track .lt b{color:#e8b840;font-size:0.92em}
.listen-track .lt span{color:#666;font-size:0.78em;font-style:italic;display:block}
.listen-track audio{width:220px;max-width:100%;height:32px}
.banter{background:linear-gradient(135deg,#0d0d18,#12121f);border-radius:12px;padding:28px;margin:25px 0;border:1px solid #1a1a2a}
.banter h3{color:#e8b840;text-align:center;font-size:1.25em;margin-bottom:18px;letter-spacing:2px}
.banter blockquote{font-style:italic;color:#ccc;line-height:1.7;padding:12px 15px;border-left:2px solid #e8b840;margin:12px 0}
.banter blockquote .who{color:#e8b840;font-style:normal;font-weight:bold}
.footer{text-align:center;padding:40px 20px;color:#333;font-size:0.8em}
.footer a{color:#44cc88;text-decoration:none}
.footer .sig{margin-top:14px;color:#222;font-style:italic}
@media(max-width:768px){
  .hero h1{font-size:1.8em}
  .gallery{grid-template-columns:1fr}
  .listen-track{flex-direction:column;align-items:flex-start}
  .listen-track audio{width:100%}
}"""

def esc(s):
    return html.escape(s, quote=False)

def build_html(d):
    ep = d["num"]
    epdir = f"episode-{ep}"

    # nav
    nav = f"""<div class="nav">
  <a href="index.html">← Radio Theater Home</a>
  <a href="index.html">📻 The Trades at The Tap</a>
  <span style="color:#333">Episode {ep} of 4</span>
</div>"""

    # hero
    hero_img = d["hero"]["image"]
    hero_alt = d["hero"]["alt"]
    hero_sub = d["hero"]["sub"]
    badge = d["badge"]
    hero = f"""<div class="hero">
  <img src="{epdir}/images/{hero_img}.png" alt="{esc(hero_alt)}">
  <div class="hero-text">
    <h1>📻 RADIO THEATER</h1>
    <p>{esc(hero_sub)}</p>
    <span class="badge">{esc(badge)}</span>
  </div>
</div>"""

    # show section
    show_paras = "".join(
        f'<p style="line-height:1.8;color:#bbb;text-align:justify">{esc(p)}</p><br>'
        for p in d["show"]
    ).rstrip("<br>")
    show = f"""<div class="section">
  <h2>🎙️ The Show</h2>
  {show_paras}
</div>"""

    # gallery
    figs = "".join(
        f'<figure><img src="{epdir}/images/{im["slug"]}.png" loading="lazy" alt="{esc(im["alt"])}"><figcaption>{esc(im["caption"])}</figcaption></figure>'
        for im in d["images"]
    )
    gallery = f"""<div class="section">
  <h2>🎨 The View From Here</h2>
  <div class="gallery">
    {figs}
  </div>
</div>"""

    # cast
    cast_cards = "".join(
        f'<div class="cast-card" style="border-left-color:{color}"><div class="name" style="color:{color}">{esc(name)}</div><div class="voice">{esc(voice)}</div></div>'
        for key, name, voice in CAST for _, color in [SPEAKER[key]]
    )
    cast = f"""<div class="section">
  <h2>🎭 The Voice Cast</h2>
  <p style="color:#666;font-style:italic;margin-bottom:14px">Seven characters, seven distinct voices. Each is a free-text voice prompt rendered through DeepInfra Qwen3-TTS-VoiceDesign.</p>
  <div class="cast">
    {cast_cards}
  </div>
</div>"""

    # broadcast lines (lines + air)
    convo_blocks = []
    for ln in d["lines"]:
        sp = ln["speaker"]
        name, _ = SPEAKER[sp]
        audio = f'<audio controls preload="none"><source src="{epdir}/{sp}-{ln["slug"]}.mp3" type="audio/mpeg"></audio>'
        convo_blocks.append(f"""<div class="tap-line">
      <div class="head"><div class="tap-speaker {sp}">{esc(name)}</div></div>
      <div class="tap-text">{esc(ln["text"])}</div>
      <div class="tap-meta">{esc(ln.get("meta",""))}</div>
      {audio}
    </div>""")
    for al in d.get("air", []):
        convo_blocks.append(f"""<div class="tap-line">
      <div class="head"><div class="tap-speaker air">ALL</div></div>
      <div class="tap-text">{esc(al["text"])}</div>
      <div class="tap-meta">{esc(al.get("meta",""))}</div>
    </div>""")
    convo = f"""<div class="section">
  <h2>🎧 On the Air — {esc(d["title"])}</h2>
  <p style="color:#666;font-style:italic;margin-bottom:16px">The broadcast, scene by scene. Press play on any line to hear that voice speak it.</p>
  <div class="tap-convo">
    {chr(10).join(convo_blocks)}
  </div>
</div>"""

    # banter
    banter_blocks = "".join(
        f'<blockquote><span class="who">{esc(b["who"])}</span> — "{esc(b["text"])}"</blockquote>'
        for b in d["banter"]
    )
    banter = f"""<div class="section">
  <div class="banter">
    <h3>🎤 BEST OF THE BANTER</h3>
    {banter_blocks}
  </div>
</div>"""

    # listen all
    tracks = []
    for i, ln in enumerate(d["lines"], 1):
        sp = ln["speaker"]
        _, _ = SPEAKER[sp]
        disp = SPEAKER[sp][0]
        tracks.append(f'<div class="listen-track"><span class="ln">{i:02d}</span><div class="lt"><b>{esc(ln["label"])}</b><span>{esc(disp)}</span></div><audio controls preload="none"><source src="{epdir}/{sp}-{ln["slug"]}.mp3" type="audio/mpeg"></audio></div>')
    listen = f"""<div class="section">
  <h2>📻 Listen — The Full Broadcast</h2>
  <p style="color:#666;font-style:italic;margin-bottom:14px">Every rendered line, in broadcast order. A different voice for every trade.</p>
  <div class="listen-all">
    {chr(10).join(tracks)}
  </div>
</div>"""

    footer = f"""<div class="footer">
  <p>📻 Radio Theater: The Trades at The Tap · SuperInstance · F/V EILEEN · Southeast Alaska · 2026</p>
  <p style="margin-top:8px">
    <a href="https://the-tap.casey-digennaro.workers.dev">The Tap</a> ·
    <a href="https://officers-quarters.pages.dev">Officers' Quarters</a> ·
    <a href="https://github.com/SuperInstance">GitHub</a> ·
    <a href="https://ai-writings.pages.dev">AI-Writings</a>
  </p>
  <p class="sig">"{esc(d["footer_sig"])}"</p>
</div>"""

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>📻 Radio Theater: The Trades at The Tap — Episode {ep} ({d["title"]})</title>
<meta name="description" content="{esc(d["meta_desc"])}">
<style>
{CSS}
</style>
</head>
<body>

{nav}

{hero}

{show}

{gallery}

{cast}

{convo}

{banter}

{listen}

{footer}

</body>
</html>
"""
    return page


def build_script_md(d):
    ep = d["num"]
    out = []
    out.append(f"# Radio Theater: The Trades at The Tap — Episode {ep} ({d['title']})")
    out.append("")
    out.append(f"*Broadcast script · adapted from the 2026-08-16 source nights · hosted by Lucineer (foreman) · Wesley is the room*")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Voice Cast (TTS assignment)")
    out.append("")
    out.append("Each character is rendered with a distinct free-text voice prompt on")
    out.append("**DeepInfra `Qwen/Qwen3-TTS-VoiceDesign`** (`/v1/openai/audio/speech`).")
    out.append("")
    out.append("| Character | Voice prompt (free-text) | Rendered lines |")
    out.append("|-----------|--------------------------|----------------|")
    counts = {}
    for ln in d["lines"]:
        counts[ln["speaker"]] = counts.get(ln["speaker"], 0) + 1
    for key, name, voice in CAST:
        slugs = [ln["slug"] for ln in d["lines"] if ln["speaker"] == key]
        out.append(f"| **{name}** | {voice} | {' · '.join(slugs)} |")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## The Broadcast")
    out.append("")
    for ln in d["lines"]:
        sp = ln["speaker"]
        name = SPEAKER[sp][0]
        out.append(f"### {name}")
        out.append(f"> `{sp}-{ln['slug']}`")
        out.append(f"> {ln['text']}")
        out.append("")
    for al in d.get("air", []):
        out.append("### ALL")
        out.append(f"> {al['text']}")
        out.append("")
    out.append("---")
    out.append("")
    out.append(f"*— Lucineer, foreman of the fleet · {d['title']} at The Tap · 2026-08-16*")
    out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    ep = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    d = json.load(open(os.path.join(ROOT, "data", f"episode-{ep}.json")))

    html_path = os.path.join(ROOT, f"episode-{ep}.html")
    with open(html_path, "w") as f:
        f.write(build_html(d))
    print(f"wrote {html_path} ({os.path.getsize(html_path)} bytes)")

    epdir = os.path.join(ROOT, f"episode-{ep}")
    os.makedirs(epdir, exist_ok=True)
    md_path = os.path.join(epdir, "SCRIPT.md")
    with open(md_path, "w") as f:
        f.write(build_script_md(d))
    print(f"wrote {md_path} ({os.path.getsize(md_path)} bytes)")
