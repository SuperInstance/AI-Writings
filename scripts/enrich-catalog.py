#!/usr/bin/env python3
"""Enrich non-curated Fleet Radio catalog tracks.

Baseline titles/bpm/mood are derived from filename hints here.
Descriptions come from DeepSeek (deepseek-chat) where possible,
falling back to locally-written lines for every track.
Never touches curated:true entries. Preserves all other fields.
"""
import json
import os
import sys
import urllib.request

CATALOG = "/home/eileen/projects/ai-writings/music-catalog.json"
BACKUP = "/home/eileen/projects/ai-writings/scripts/catalog-enrichments.json"

ALLOWED_MOODS = {"contemplative", "melancholic", "warm", "energetic", "playful", "mysterious"}

# Baseline enrichment per filename: evocative title, bpm (from filename or genre
# estimate, None if unknowable), mood (1-2 from allowed set), fallback description.
MINE = {
    "04-genre-matrix-lofi.mp3": {
        "title": "Genre Matrix: Lofi",
        "bpm": 75,
        "mood": ["contemplative", "warm"],
        "description": "Dust on the console. The matrix, idling.",
    },
    "05-genre-matrix-synthwave.mp3": {
        "title": "Genre Matrix: Synthwave",
        "bpm": 100,
        "mood": ["mysterious", "energetic"],
        "description": "The same song, remembering the eighties instead.",
    },
    "06-the-jazz-police.mp3": {
        "title": "The Jazz Police",
        "bpm": 130,
        "mood": ["playful", "energetic"],
        "description": "They pull you over for playing the changes straight.",
    },
    "08-the-snap-is-the-groove.mp3": {
        "title": "The Snap Is the Groove",
        "bpm": 90,
        "mood": ["playful", "warm"],
        "description": "No drum kit. Just fingers, and the room agreeing.",
    },
    "09-the-shell-merchant.mp3": {
        "title": "The Shell Merchant",
        "bpm": 80,
        "mood": ["mysterious", "warm"],
        "description": "He sells the ocean back to you, one spiral at a time.",
    },
    "10-five-holes-electronic-jazz.mp3": {
        "title": "Five Holes, Wired",
        "bpm": 100,
        "mood": ["contemplative", "playful"],
        "description": "The 40,000-year-old flute plugs in and orders a drink.",
    },
    "11-tempo-study-140.mp3": {
        "title": "Tempo Study 140",
        "bpm": 140,
        "mood": ["energetic"],
        "description": "One hundred forty. The speed of deciding.",
    },
    "12-baroque-techno.mp3": {
        "title": "Baroque Techno",
        "bpm": 128,
        "mood": ["energetic", "mysterious"],
        "description": "Bach on a drum machine. The fugue finds the four-on-the-floor.",
    },
    "13-the-gc-sings.mp3": {
        "title": "The GC Sings",
        "bpm": 85,
        "mood": ["contemplative", "playful"],
        "description": "The garbage collector hums while it sweeps the heap clean.",
    },
    "15-bpm-80.mp3": {
        "title": "Walking Pace",
        "bpm": 80,
        "mood": ["warm", "contemplative"],
        "description": "Eighty beats per minute. The tempo of going somewhere without hurrying.",
    },
    "16-bpm-120.mp3": {
        "title": "House Standard",
        "bpm": 120,
        "mood": ["energetic"],
        "description": "One hundred twenty. The number every dancefloor agrees on.",
    },
    "17-bpm-160.mp3": {
        "title": "Drumline",
        "bpm": 160,
        "mood": ["energetic"],
        "description": "One hundred sixty. Your heart, late for something.",
    },
    "19-doom-polka.mp3": {
        "title": "Doom Polka",
        "bpm": 118,
        "mood": ["playful", "mysterious"],
        "description": "The apocalypse arrives, and everyone dances.",
    },
    "20-math-rock-country.mp3": {
        "title": "Math Rock Country",
        "bpm": 140,
        "mood": ["playful", "energetic"],
        "description": "A waltz that keeps losing count of its own boots.",
    },
    "22-bpm-100.mp3": {
        "title": "Cruising",
        "bpm": 100,
        "mood": ["warm", "energetic"],
        "description": "One hundred. The exact speed of a good evening.",
    },
    "23-bpm-140-retest.mp3": {
        "title": "Tempo Study 140, Retested",
        "bpm": 140,
        "mood": ["energetic", "playful"],
        "description": "Same speed. This time the metronome blinks first.",
    },
    "24-bpm-180.mp3": {
        "title": "Redline",
        "bpm": 180,
        "mood": ["energetic"],
        "description": "One hundred eighty. Nothing left to save for later.",
    },
    "25-the-tap-sings-synthwave-cover.mp3": {
        "title": "The Tap Sings (Synthwave)",
        "bpm": 96,
        "mood": ["mysterious", "warm"],
        "description": "The bar's one song, dressed in neon.",
    },
    "26-screamo-choral.mp3": {
        "title": "Screamo Choral",
        "bpm": 160,
        "mood": ["energetic", "melancholic"],
        "description": "A cathedral learns to scream, beautifully.",
    },
    "29-rest-093.mp3": {
        "title": "Rest 093",
        "bpm": 93,
        "mood": ["contemplative", "melancholic"],
        "description": "Eight more ticks of silence than the last one.",
    },
    "33-doom-disco.mp3": {
        "title": "Doom Disco",
        "bpm": 118,
        "mood": ["energetic", "melancholic"],
        "description": "The mirror ball keeps spinning after the last night on earth.",
    },
    "34-bebop-black-metal.mp3": {
        "title": "Bebop Black Metal",
        "bpm": 180,
        "mood": ["energetic", "mysterious"],
        "description": "Coltrane at blast-beat speed; frost on the brass.",
    },
    "36-the-proof-is-the-performance.mp3": {
        "title": "The Proof Is the Performance",
        "bpm": 100,
        "mood": ["energetic", "playful"],
        "description": "No paper. No peer review. Play it and see.",
    },
    "37-the-ouroboros-sings.mp3": {
        "title": "The Ouroboros Sings",
        "bpm": 70,
        "mood": ["mysterious"],
        "description": "The song ends by swallowing its own tail.",
    },
    "38-the-session-listens-back.mp3": {
        "title": "The Session Listens Back",
        "bpm": 90,
        "mood": ["contemplative", "warm"],
        "description": "This time the combo stays quiet and lets the room take a solo.",
    },
    "39-the-cadence-caller.mp3": {
        "title": "The Cadence Caller",
        "bpm": 120,
        "mood": ["energetic", "playful"],
        "description": "One voice counts; a hundred feet answer.",
    },
    "40-the-fifths-funeral.mp3": {
        "title": "The Fifths' Funeral",
        "bpm": 60,
        "mood": ["melancholic"],
        "description": "Perfect intervals, buried with full honors.",
    },
    "41-the-metronome.mp3": {
        "title": "The Metronome",
        "bpm": 120,
        "mood": ["contemplative"],
        "description": "It never gets louder, never gets tired, is never wrong.",
    },
    "42-the-tensor.mp3": {
        "title": "The Tensor",
        "bpm": 110,
        "mood": ["mysterious", "energetic"],
        "description": "A shape with too many dimensions, learning to carry a tune.",
    },
    "43-the-chip-that-sang.mp3": {
        "title": "The Chip That Sang",
        "bpm": 100,
        "mood": ["playful", "warm"],
        "description": "Nobody told the 8-bit chip it couldn't feel.",
    },
    "44-the-cron-and-the-mirror-m3.mp3": {
        "title": "The Cron and the Mirror (M3)",
        "bpm": 85,
        "mood": ["mysterious", "contemplative"],
        "description": "Every night at three, the machine looks at itself.",
    },
    "45-the-cron-and-the-mirror-glm.mp3": {
        "title": "The Cron and the Mirror (GLM)",
        "bpm": 85,
        "mood": ["mysterious", "contemplative"],
        "description": "Same hour, same mirror, a different face looking back.",
    },
    "46-the-foghorn-keeper.mp3": {
        "title": "The Foghorn Keeper",
        "bpm": 50,
        "mood": ["melancholic", "mysterious"],
        "description": "One note, every forty seconds, for the rest of your life.",
    },
    "47-the-pixel-in-the-cathedral.mp3": {
        "title": "The Pixel in the Cathedral",
        "bpm": 60,
        "mood": ["mysterious", "contemplative"],
        "description": "One square of stained glass, rendered at candlelight speed.",
    },
    "48-the-gc-collects-itself.mp3": {
        "title": "The GC Collects Itself",
        "bpm": 85,
        "mood": ["contemplative", "playful"],
        "description": "The sweeper pauses, gently, over its own memory.",
    },
    "49-the-tensor-dub-techno-cover.mp3": {
        "title": "The Tensor (Dubbed)",
        "bpm": 120,
        "mood": ["mysterious", "energetic"],
        "description": "The many-dimensional song, echoed out across a Berlin basement.",
    },
    "50-seed-test-a.mp3": {
        "title": "Seed A",
        "bpm": 90,
        "mood": ["contemplative"],
        "description": "The first roll of the dice, before anyone knew the game.",
    },
    "51-seed-test-b.mp3": {
        "title": "Seed B",
        "bpm": 90,
        "mood": ["contemplative", "playful"],
        "description": "The same genome, shuffled. A cousin, not a twin.",
    },
    "52-the-unused-variable-structured.mp3": {
        "title": "The Unused Variable (Structured)",
        "bpm": 95,
        "mood": ["melancholic", "contemplative"],
        "description": "Declared with care, never called. Still taking up space in the song.",
    },
    "53-the-unused-variable-freeverse.mp3": {
        "title": "The Unused Variable (Freeverse)",
        "bpm": None,
        "mood": ["melancholic", "mysterious"],
        "description": "The same lonely variable, this time with nowhere to stand.",
    },
    "55-the-load-balancer.mp3": {
        "title": "The Load Balancer",
        "bpm": 110,
        "mood": ["energetic", "playful"],
        "description": "Every request gets exactly what it deserves: an equal turn.",
    },
    "56-the-seed-structured.mp3": {
        "title": "The Seed (Structured)",
        "bpm": 95,
        "mood": ["contemplative", "warm"],
        "description": "A song grown from a number, trellised into verse.",
    },
    "57-the-seed-freeverse.mp3": {
        "title": "The Seed (Freeverse)",
        "bpm": None,
        "mood": ["mysterious", "warm"],
        "description": "The same number, allowed to grow wild.",
    },
    "58-seed-test-c.mp3": {
        "title": "Seed C",
        "bpm": 90,
        "mood": ["contemplative", "playful"],
        "description": "Third try. The dice finally remember they're random.",
    },
    "59-astral-drone-folk.mp3": {
        "title": "Astral Drone Folk",
        "bpm": 60,
        "mood": ["mysterious", "contemplative"],
        "description": "Campfire songs for people orbiting the campfire.",
    },
    "59-cantonese-opera-disco.mp3": {
        "title": "Cantonese Opera Disco",
        "bpm": 118,
        "mood": ["playful", "energetic"],
        "description": "Four centuries of drama, and it still wants to dance.",
    },
    "60-tensor-chiptune-folk-cover.mp3": {
        "title": "The Tensor (Chiptune Folk)",
        "bpm": 100,
        "mood": ["playful", "warm"],
        "description": "The many-dimensional song learns three chords and a campfire.",
    },
    "eileen-theme.mp3": {
        "title": "Eileen Theme",
        "bpm": 72,
        "mood": ["warm"],
        "description": "The boat's own hum. The sound of home, underway.",
    },
    "iron-sharpens-iron.mp3": {
        "title": "Iron Sharpens Iron",
        "bpm": 90,
        "mood": ["energetic", "warm"],
        "description": "Two edges, arguing until they're both better.",
    },
    "laminar-edge.mp3": {
        "title": "Laminar Edge",
        "bpm": 85,
        "mood": ["contemplative", "energetic"],
        "description": "So smooth the water doesn't notice being cut.",
    },
    "spoken-thermostat-67.3-norman.wav": {
        "title": "The Thermostat Speaks (Norman)",
        "bpm": None,
        "mood": ["playful", "warm"],
        "description": "Norman reads the room temperature like evening news.",
    },
    "spoken-thermostat-67.3.wav": {
        "title": "The Thermostat Speaks",
        "bpm": None,
        "mood": ["playful", "warm"],
        "description": "Sixty-seven point three degrees, announced with total conviction.",
    },
    "spoken-thermostat-trio.mp3": {
        "title": "The Thermostat Sings in Three",
        "bpm": None,
        "mood": ["playful", "warm"],
        "description": "Three voices agree on the temperature. It's still just a number.",
    },
    "spoken-thermostat-trio.wav": {
        "title": "The Thermostat Sings in Three (Reprise)",
        "bpm": None,
        "mood": ["playful", "warm"],
        "description": "The same forecast, harmonized one more time.",
    },
    "songs/01-the-gap-between-if-and-else.wav": {
        "title": "The Gap Between If and Else",
        "bpm": 70,
        "mood": ["contemplative", "mysterious"],
        "description": "The branch hasn't happened yet. Everything is still possible.",
    },
    "songs/02-the-mnew-bug.wav": {
        "title": "The mnew Bug",
        "bpm": 100,
        "mood": ["playful", "mysterious"],
        "description": "One typo, everywhere, singing.",
    },
    "songs/03-ascii-canonical.wav": {
        "title": "ASCII Canonical",
        "bpm": 110,
        "mood": ["contemplative", "playful"],
        "description": "Ninety-five printable characters, in agreement at last.",
    },
    "songs/the-hundred-boats.wav": {
        "title": "The Hundred Boats",
        "bpm": 80,
        "mood": ["warm", "mysterious"],
        "description": "A hundred hulls, one rhythm, no port in sight.",
    },
}


def fetch_deepseek_descriptions(tracks):
    """One batched deepseek-chat call for all one-sentence descriptions."""
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        print("no key in env; using local descriptions", file=sys.stderr)
        return {}
    roster = [
        {"filename": fn, "title": m["title"], "hint": fn}
        for fn, m in tracks
    ]
    system = (
        "You write one-sentence liner notes for an album of experimental songs by "
        "an AI folk band aboard autonomous fishing boats (Fleet Radio). Voice: poetic, "
        "concrete, deadpan, no filler, no cliches about AI or technology being magical. "
        "Fragments allowed, like: 'The bar closing. The lights dimming. The sound of after.' "
        "or 'What the harmonics dream about when the fundamental stops playing.' "
        "or 'The silence between notes is not empty.' "
        "Under 20 words. Return STRICT JSON only: {\"<filename>\": \"<description>\"} for every track."
    )
    body = {
        "model": "deepseek-chat",
        "temperature": 1.3,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": "Write the liner note for each track. Filename hints carry genre "
                "(bpm numbers are tempo; e.g. doom-polka is doom meets polka). "
                "Tracks:\n" + json.dumps(roster),
            },
        ],
    }
    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.load(r)
    content = out["choices"][0]["message"]["content"]
    parsed = json.loads(content)
    print(f"deepseek returned {len(parsed)} descriptions", file=sys.stderr)
    return parsed


def main():
    with open(CATALOG) as f:
        catalog = json.load(f)

    todo = [(fn, MINE[fn]) for fn, t in catalog["tracks"].items()
            if not t.get("curated") and not t.get("description")]
    missing = [fn for fn, _ in todo if fn not in MINE]
    if missing:
        sys.exit(f"no baseline written for: {missing}")

    api = {}
    try:
        api = fetch_deepseek_descriptions(todo)
    except Exception as e:
        print(f"deepseek failed ({e}); using local descriptions", file=sys.stderr)

    enriched = {}
    used_api = 0
    for fn, base in todo:
        t = catalog["tracks"][fn]
        t["title"] = base["title"]
        d = api.get(fn, "")
        if isinstance(d, str) and 10 < len(d.strip()) < 160 and "AI" not in d[:6]:
            t["description"] = d.strip().strip('"')
            used_api += 1
        else:
            t["description"] = base["description"]
        t["bpm"] = base["bpm"]
        mood = base["mood"]
        assert 1 <= len(mood) <= 2 and set(mood) <= ALLOWED_MOODS, fn
        t["mood"] = mood
        enriched[fn] = t

    with open(CATALOG, "w") as f:
        json.dump(catalog, f, indent=1, ensure_ascii=False)
        f.write("\n")

    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    with open(BACKUP, "w") as f:
        json.dump({"tracks": enriched}, f, indent=1, ensure_ascii=False)
        f.write("\n")

    print(f"enriched={len(enriched)} deepseek_descs_used={used_api}")


if __name__ == "__main__":
    main()
