#!/usr/bin/env python3
"""compose-tap-songs.py — re-render the three lost Tap songs from lead sheets.

Reads the kimi arrangement JSONs (kimi-out/kimi-0N.json) — one per song,
generated with `kimi -p` from the .md lead sheets — validates them, and
composes each song as a multi-track MIDI (piano comping, acoustic bass,
brushed kit, lead instrument). Falls back to built-in arrangements if a
kimi output is missing/invalid.

Usage:
  compose-tap-songs.py            # compose + write MIDI files into songs/
  compose-tap-songs.py --check    # validate kimi JSONs only, no output
"""
import json
import os
import random
import re
import sys

import mido

HERE = os.path.dirname(os.path.abspath(__file__))
SONGS = os.path.normpath(os.path.join(HERE, "..", "songs"))
TPQ = 480

# ---------------------------------------------------------------- pitch utils

NOTE_BASE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
PC_NAME = {v: k for k, v in NOTE_BASE.items()}
for _p, _n in [(0, "C"), (1, "C#"), (2, "D"), (3, "Eb"), (4, "E"), (5, "F"),
               (6, "F#"), (7, "G"), (8, "Ab"), (9, "A"), (10, "Bb"), (11, "B")]:
    PC_NAME[_p] = _n

NOTE_RE = re.compile(r"^([A-G])(b|#)?(-?\d)$")


def note_to_midi(name):
    m = NOTE_RE.match(name.strip())
    if not m:
        raise ValueError("bad note %r" % name)
    letter, acc, octv = m.groups()
    n = NOTE_BASE[letter] + (1 if acc == "#" else -1 if acc == "b" else 0)
    return (int(octv) + 1) * 12 + n


def midi_to_name(n):
    return "%s%d" % (PC_NAME[n % 12], n // 12 - 1)


def pc_near(pc, low, high):
    """All midi notes of pitch class pc within [low, high]."""
    return [n for n in range(low, high + 1) if n % 12 == pc]

# ---------------------------------------------------------------- chord model

QUALITIES = {
    # name -> intervals from root (semitones)
    "":       [0, 4, 7],
    "maj":    [0, 4, 7],
    "M":      [0, 4, 7, 11],
    "maj7":   [0, 4, 7, 11],
    "M7":     [0, 4, 7, 11],
    "Maj7":   [0, 4, 7, 11],
    "maj9":   [0, 4, 7, 11, 14],
    "Maj9":   [0, 4, 7, 11, 14],
    "M9":     [0, 4, 7, 11, 14],
    "6":      [0, 4, 7, 9],
    "69":     [0, 4, 7, 9, 14],
    "add9":   [0, 4, 7, 14],
    "7":      [0, 4, 7, 10],
    "9":      [0, 4, 7, 10, 14],
    "13":     [0, 4, 7, 10, 14, 21],
    "7b9":    [0, 4, 7, 10, 13],
    "7#9":    [0, 4, 7, 10, 15],
    "7#11":   [0, 4, 7, 10, 18],
    "7b13":   [0, 4, 7, 10, 8],
    "7sus":   [0, 5, 7, 10],
    "sus":    [0, 5, 7],
    "sus2":   [0, 2, 7],
    "sus4":   [0, 5, 7],
    "m":      [0, 3, 7],
    "min":    [0, 3, 7],
    "-":      [0, 3, 7],
    "m7":     [0, 3, 7, 10],
    "min7":   [0, 3, 7, 10],
    "-7":     [0, 3, 7, 10],
    "m9":     [0, 3, 7, 10, 14],
    "-9":     [0, 3, 7, 10, 14],
    "m11":    [0, 3, 7, 10, 17],
    "m6":     [0, 3, 7, 9],
    "m7b5":   [0, 3, 6, 10],
    "-7b5":   [0, 3, 6, 10],
    "ø":      [0, 3, 6, 10],
    "mMaj7":  [0, 3, 7, 11],
    "dim":    [0, 3, 6],
    "dim7":   [0, 3, 6, 9],
    "o7":     [0, 3, 6, 9],
    "aug":    [0, 4, 8],
}

CHORD_RE = re.compile(r"^([A-G][#b]?)(.*)$")


class Chord:
    def __init__(self, symbol):
        symbol = symbol.strip()
        m = CHORD_RE.match(symbol)
        if not m:
            raise ValueError("bad chord %r" % symbol)
        root, qual = m.groups()
        self.symbol = symbol
        self.root_pc = (NOTE_BASE[root[0]] + (1 if root[1:] == "#" else -1 if root[1:] == "b" else 0)) % 12
        q = qual
        if q not in QUALITIES:
            # case-insensitive rescue
            for k in QUALITIES:
                if k.lower() == q.lower():
                    q = k
                    break
            else:
                # unknown: treat bare number extensions as dominant family
                qm = re.match(r"^(\d+)$", q)
                if qm:
                    q = "7" if qm.group(1) == "7" else ("9" if qm.group(1) == "9" else "13")
                else:
                    raise ValueError("unknown chord quality %r in %r" % (qual, symbol))
        self.intervals = QUALITIES[q]
        self.family = ("min" if 3 in self.intervals and 7 not in self.intervals
                       else "halfdim" if 6 in self.intervals and 3 in self.intervals
                       else "dom" if 10 in self.intervals
                       else "maj")

    def tone(self, degree):
        """degree: interval semitone value from root."""
        return (self.root_pc + degree) % 12

    def third(self):
        return self.tone(3 if 3 in self.intervals else 4)

    def seventh(self):
        for cand in (10, 11, 6, 9):
            if cand in self.intervals:
                return self.tone(cand)
        return None  # triad: no 7th

    def color(self):
        for cand in (14, 21, 17, 9, 13, 2):
            if cand in self.intervals:
                return self.tone(cand)
        return None

    def fifth(self):
        return self.tone(7 if 7 in self.intervals else 6 if 6 in self.intervals else 8)

    def bass_note(self):
        return self.root_pc


def chord_bass_near(chord, target=41):
    """Root pitch class voiced near MIDI 41 (F2)."""
    cands = pc_near(chord.root_pc, 33, 48)
    return min(cands, key=lambda n: abs(n - target))

# ---------------------------------------------------------------- track builders


class TrackBuilder:
    def __init__(self, mid, channel, program, name, rng, pan=None, vol=None):
        self.mid = mid
        self.channel = channel
        self.rng = rng
        self.t = mido.MidiTrack()
        mid.tracks.append(self.t)
        self.t.append(mido.MetaMessage("track_name", name=name, time=0))
        self.t.append(mido.Message("program_change", channel=channel, program=program, time=0))
        if pan is not None:
            self.t.append(mido.Message("control_change", channel=channel, control=10, value=pan, time=0))
        if vol is not None:
            self.t.append(mido.Message("control_change", channel=channel, control=7, value=vol, time=0))
        self.cursor = 0
        self.pending = []  # (abs_tick, priority, msg)

    def note(self, tick, midi_note, dur_ticks, vel, release=True):
        self.pending.append((int(tick), self.cursor, ("on", int(midi_note), int(vel))))
        self.cursor += 1
        if release and dur_ticks > 0:
            self.pending.append((int(tick + dur_ticks), self.cursor, ("off", int(midi_note), 0)))
            self.cursor += 1

    def finish(self, end_tick):
        # marker at the very end so nothing dangles
        self.pending.sort(key=lambda x: (x[0], x[1]))
        last = 0
        for tick, _, item in self.pending:
            delta = max(0, tick - last)
            last = tick
            if isinstance(item, tuple):
                kind, note, vel = item
                self.t.append(mido.Message(
                    "note_%s" % ("on" if kind == "on" else "off"),
                    channel=self.channel, note=note, velocity=vel, time=delta))
            else:
                self.t.append(mido.MetaMessage("marker", text=str(item), time=delta))
        if end_tick > last:
            self.t.append(mido.MetaMessage("marker", text="end", time=end_tick - last))
        else:
            self.t.append(mido.MetaMessage("end_of_track", time=0))


def beats_to_ticks(b):
    return int(round(b * TPQ))


# ---------------------------------------------------------------- song composer


LEAD_PROGRAMS = {
    "muted trumpet": 59, "flugelhorn": 56, "vibraphone": 11,
    "electric piano": 4, "piano": 0, "acoustic guitar": 24,
    "electric guitar (clean)": 27, "tenor sax": 66, "clarinet": 71,
    "flute": 73, "voice oohs": 53, "steel guitar": 26,
}


def resolve_lead(name):
    return LEAD_PROGRAMS.get((name or "").strip().lower(), 56)


def parse_kimi_json(path):
    with open(path) as f:
        raw = f.read().strip()
    # strip fences if any
    raw = re.sub(r"^```(json)?\s*|\s*```$", "", raw, flags=re.S)
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object found")
    data = json.loads(raw[start:end + 1])
    if isinstance(data, dict) and "sections" not in data:
        raise ValueError("no sections key")
    lead_name = data.get("lead_instrument", "")
    # validate structure
    tempo = int(data["tempo"])
    key = str(data.get("key", "?"))
    sections = []
    for s in data["sections"]:
        chords = [Chord(c) for c in s["chords"]]
        bars = int(s["bars"])
        if len(chords) != bars:
            # pad/truncate to bar count
            while len(chords) < bars:
                chords.append(chords[-1])
            chords = chords[:bars]
        mel = []
        for ev in s.get("melody", []):
            beat, note, dur = ev
            beat, dur = float(beat), float(dur)
            n = note_to_midi(note) if isinstance(note, str) else int(note)
            if 36 <= n <= 96:
                mel.append([beat, n, max(0.25, dur)])
        sections.append({"name": s["name"], "bars": bars, "chords": chords,
                         "melody": sorted(mel, key=lambda e: e[0])})
    return tempo, key, sections, lead_name


def compose_song(song_key, spec_path, out_mid, fallback, seed=1, default_lead=""):
    try:
        tempo, key, sections, lead_name = parse_kimi_json(spec_path)
        src = "kimi"
    except Exception as e:
        print("  [warn] kimi spec unusable (%s) — using fallback arrangement" % e)
        tempo, key, sections = fallback()
        lead_name = default_lead
        src = "fallback"

    rng = random.Random(seed)
    swing = 0.08 if tempo <= 100 else 0.0   # beats of delay on offbeat 8ths
    total_beats = sum(s["bars"] for s in sections) * 4

    mid = mido.MidiFile(type=1, ticks_per_beat=TPQ)
    tmap = mido.MidiTrack()
    mid.tracks.append(tmap)
    tmap.append(mido.MetaMessage("track_name", name=song_key, time=0))
    tmap.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(tempo), time=0))
    tmap.append(mido.MetaMessage("time_signature", numerator=4, denominator=4, time=0))
    # section markers
    bpos = 0
    marks = []
    for s in sections:
        marks.append((beats_to_ticks(bpos), s["name"]))
        bpos += s["bars"] * 4
    last = 0
    for tick, name in marks:
        tmap.append(mido.MetaMessage("marker", text=name, time=tick - last))
        last = tick
    tmap.append(mido.MetaMessage("marker", text="end", time=beats_to_ticks(total_beats + 8) - last))

    piano = TrackBuilder(mid, 0, 0, "Piano", rng, pan=44)
    bass = TrackBuilder(mid, 1, 32, "Acoustic Bass", rng, pan=70)
    drums = TrackBuilder(mid, 9, 0, "Brush Kit", rng, pan=56)
    lead_prog = resolve_lead(lead_name)
    lead = TrackBuilder(mid, 2, lead_prog, "Lead (%s)" % lead_name, rng, pan=64)

    # walk sections, lay down comping / bass / drums / melody
    beat0 = 0
    for s in sections:
        bars = s["bars"]
        chords = s["chords"]
        style = "ballad" if tempo < 90 else "swing"
        # --- piano comping
        for i, ch in enumerate(chords):
            b = beat0 + i * 4
            if style == "ballad":
                hits = [(0.0, 3.6), (2.5, 1.4)] if i % 2 else [(0.0, 3.9)]
                if s["name"] in ("INTRO", "BRIDGE", "TAG"):
                    hits = [(0.0, 3.9)]
            else:
                # charleston-ish swing comp, sparse
                pat = [[(0.0, 1.2), (2.66, 1.0)], [(0.0, 1.2)],
                       [(1.5, 0.9), (3.0, 0.9)], [(0.0, 1.2), (2.66, 1.0)]][i % 4]
                hits = pat
            for off, dur in hits:
                vels = piano_voicing(ch)
                for j, (n, w) in enumerate(vels):
                    v = int(52 + 10 * w + rng.uniform(-4, 4))
                    offb = off + (swing if abs(off % 1 - 0.5) < 0.01 else 0)
                    piano.note(beats_to_ticks(b + offb), n, beats_to_ticks(dur * 0.95), max(28, min(v, 92)))
        # --- bass
        for i, ch in enumerate(chords):
            b = beat0 + i * 4
            nxt = chords[i + 1] if i + 1 < len(chords) else ch
            r = chord_bass_near(ch)
            if style == "ballad":
                fifth = min(pc_near(ch.fifth(), r, r + 12), key=lambda n: abs(n - (r + 7)), default=r + 7)
                bass.note(beats_to_ticks(b), r, beats_to_ticks(3.6), int(64 + rng.uniform(-4, 4)))
                bass.note(beats_to_ticks(b + 3), fifth, beats_to_ticks(0.95), 58)
            else:
                # walk: root, chord tone, approach to next root
                steps = [r, None, None, None]
                third = min(pc_near(ch.third(), r, r + 12), default=r + 4)
                steps[1] = third if i % 2 == 0 else min(pc_near(ch.fifth(), r, r + 12), default=r + 7)
                nr = chord_bass_near(nxt)
                steps[3] = nr + (-1 if nr > r else 1)
                steps[2] = nr - 2 if abs(nr - r) > 2 else r + 5
                for k, n in enumerate(steps):
                    if n is not None and 33 <= n <= 52:
                        bass.note(beats_to_ticks(b + k), n, beats_to_ticks(0.92), int(60 + (4 if k == 0 else 0) + rng.uniform(-3, 3)))
        # --- brushed drums
        for i in range(bars):
            b = beat0 + i * 4
            if style == "ballad":
                for e in range(8):  # brush swirl eighths
                    off = e * 0.5
                    offb = off + (swing if e % 2 else 0)
                    drums.note(beats_to_ticks(b + offb), 38, beats_to_ticks(0.4), int(24 + (6 if e % 4 == 0 else 0) + rng.uniform(-3, 3)))
                for q in (0, 2):
                    drums.note(beats_to_ticks(b + q), 51, beats_to_ticks(0.9), int(44 + rng.uniform(-4, 4)))
                    drums.note(beats_to_ticks(b + q), 36, beats_to_ticks(0.5), 30)  # feathered
            else:
                # ride: quarters + swung and-of-2/4; hats 2&4; light kick; snare comp
                for q in range(4):
                    drums.note(beats_to_ticks(b + q), 51, beats_to_ticks(0.9), int(48 + (4 if q in (1, 3) else 0) + rng.uniform(-3, 3)))
                    drums.note(beats_to_ticks(b + q), 36, beats_to_ticks(0.5), 28 + (6 if q == 0 else 0))
                for q in (1, 3):
                    offb = q + 0.5 + swing
                    drums.note(beats_to_ticks(b + offb), 51, beats_to_ticks(0.6), 40)
                    drums.note(beats_to_ticks(b + q), 42, beats_to_ticks(0.4), 38)
                if i % 2 == 1:
                    offb = 2.5 + swing
                    drums.note(beats_to_ticks(b + offb), 38, beats_to_ticks(0.5), 40)
        # --- lead melody
        for ev in s["melody"]:
            beat, n, dur = ev
            if beat >= s["bars"] * 4:
                continue
            offb = beat + (swing if abs(beat % 1 - 0.5) < 0.01 else 0)
            vel = int(76 + (6 if abs(beat % 4) < 0.01 else 0) + rng.uniform(-5, 5))
            lead.note(beats_to_ticks(beat0 + offb), n, beats_to_ticks(dur * 0.94), max(50, min(vel, 108)))
        beat0 += bars * 4

    end_tick = beats_to_ticks(total_beats + 8)
    for t in (piano, bass, drums, lead):
        t.finish(end_tick)
    mid.save(out_mid)
    dur_secs = total_beats * 60.0 / tempo
    return src, tempo, key, total_beats // 4, dur_secs


def piano_voicing(ch):
    """Rootless-ish voicing: [(midi, weight)] centered ~C4, 3-4 voices."""
    voices = []
    third = ch.third()
    sev = ch.seventh()
    col = ch.color()
    fifth = ch.fifth()
    if sev is None:  # triad
        voices = [third, ch.tone(0), fifth]
    else:
        voices = [third, sev]
        voices.append(col if col is not None else fifth)
    # place each just below/above middle: prefer C3..C5 cluster
    out = []
    for i, pc in enumerate(voices):
        cands = pc_near(pc, 53, 72)
        if not cands:
            continue
        pick = min(cands, key=lambda n: abs(n - (60 - i * 2)))
        out.append((pick, 1.0 if i < 2 else 0.7))
    # drop duplicates, keep 3
    seen = set()
    uniq = []
    for n, w in out:
        if n not in seen:
            seen.add(n)
            uniq.append((n, w))
    return uniq[:4] or [(60, 0.7)]


# ---------------------------------------------------------------- fallbacks

def fallback_01():
    ch = Chord
    sections = [
        {"name": "INTRO", "bars": 2, "chords": [ch("Ebmaj9"), ch("Bbsus")],
         "melody": [[0, note_to_midi("Bb4"), 2], [2, note_to_midi("G4"), 1], [4, note_to_midi("Ab4"), 2], [6, note_to_midi("F4"), 2]]},
        {"name": "VERSE", "bars": 4, "chords": [ch("C-7"), ch("F7"), ch("Bbmaj7"), ch("Ebmaj9")],
         "melody": [[0, note_to_midi("Eb4"), 1.5], [1.5, note_to_midi("G4"), 0.5], [2, note_to_midi("Bb4"), 2],
                    [4, note_to_midi("Ab4"), 1], [5, note_to_midi("G4"), 1], [6, note_to_midi("F4"), 2],
                    [8, note_to_midi("D4"), 1.5], [9.5, note_to_midi("F4"), 0.5], [10, note_to_midi("Ab4"), 2],
                    [12, note_to_midi("G4"), 3]]},
        {"name": "CHORUS", "bars": 4, "chords": [ch("Abmaj7"), ch("G7b9"), ch("C-7"), ch("F7b9")],
         "melody": [[0, note_to_midi("Eb5"), 1], [1, note_to_midi("D5"), 1], [2, note_to_midi("C5"), 2],
                    [4, note_to_midi("B4"), 1], [5, note_to_midi("Bb4"), 1], [6, note_to_midi("G4"), 2],
                    [8, note_to_midi("Ab4"), 1.5], [9.5, note_to_midi("Bb4"), 0.5], [10, note_to_midi("C5"), 2],
                    [12, note_to_midi("D5"), 2], [14, note_to_midi("Eb5"), 2]]},
        {"name": "BRIDGE", "bars": 2, "chords": [ch("Gm7b5"), ch("C7b9")],
         "melody": [[0, note_to_midi("D4"), 3], [4, note_to_midi("Eb4"), 3]]},
        {"name": "FINAL_CHORUS", "bars": 3, "chords": [ch("Abmaj7"), ch("G7b9"), ch("C-7")],
         "melody": [[0, note_to_midi("Eb5"), 1], [1, note_to_midi("D5"), 1], [2, note_to_midi("C5"), 2],
                    [4, note_to_midi("B4"), 1], [5, note_to_midi("Bb4"), 1], [6, note_to_midi("G4"), 2],
                    [8, note_to_midi("Ab4"), 2], [10, note_to_midi("G4"), 2]]},
        {"name": "TAG", "bars": 1, "chords": [ch("Bbsus")],
         "melody": [[0, note_to_midi("F4"), 3.5]]},
    ]
    return 70, "Eb major", sections


def fallback_02():
    ch = Chord
    sections = [
        {"name": "INTRO", "bars": 2, "chords": [ch("Am9"), ch("D13")],
         "melody": [[0, note_to_midi("E5"), 1], [1, note_to_midi("C5"), 0.5], [1.5, note_to_midi("A4"), 0.5], [2, note_to_midi("B4"), 1],
                    [4, note_to_midi("F#4"), 1.5], [5.5, note_to_midi("A4"), 0.5], [6, note_to_midi("C#5"), 1.5]]},
        {"name": "VERSE", "bars": 4, "chords": [ch("Am9"), ch("D9"), ch("Gmaj7"), ch("Cmaj7")],
         "melody": [[0, note_to_midi("A4"), 1], [1, note_to_midi("B4"), 0.5], [1.5, note_to_midi("C5"), 0.5], [2, note_to_midi("E5"), 1.5], [3.5, note_to_midi("D5"), 0.5],
                    [4, note_to_midi("C#5"), 1], [5, note_to_midi("A4"), 1], [6, note_to_midi("F#4"), 2],
                    [8, note_to_midi("B4"), 1.5], [9.5, note_to_midi("D5"), 0.5], [10, note_to_midi("F#5"), 2],
                    [12, note_to_midi("E5"), 1], [13, note_to_midi("D5"), 1], [14, note_to_midi("B4"), 2]]},
        {"name": "CHORUS", "bars": 4, "chords": [ch("F#m7"), ch("B7b9"), ch("Emaj7"), ch("A13")],
         "melody": [[0, note_to_midi("A4"), 1.5], [1.5, note_to_midi("C#5"), 0.5], [2, note_to_midi("F#5"), 1], [3, note_to_midi("E5"), 1],
                    [4, note_to_midi("D#5"), 1], [5, note_to_midi("C5"), 1], [6, note_to_midi("A4"), 2],
                    [8, note_to_midi("G#4"), 1.5], [9.5, note_to_midi("B4"), 0.5], [10, note_to_midi("E5"), 2],
                    [12, note_to_midi("C#5"), 1], [13, note_to_midi("B4"), 1], [14, note_to_midi("A4"), 2]]},
        {"name": "VERSE2", "bars": 4, "chords": [ch("Am9"), ch("D9"), ch("Gmaj7"), ch("Cmaj7")],
         "melody": [[0, note_to_midi("C5"), 1], [1, note_to_midi("B4"), 0.5], [1.5, note_to_midi("A4"), 0.5], [2, note_to_midi("E4"), 1.5], [3.5, note_to_midi("G4"), 0.5],
                    [4, note_to_midi("A4"), 2], [6, note_to_midi("F#4"), 2],
                    [8, note_to_midi("G4"), 1], [9, note_to_midi("A4"), 1], [10, note_to_midi("B4"), 2],
                    [12, note_to_midi("D5"), 2], [14, note_to_midi("C5"), 2]]},
        {"name": "BRIDGE", "bars": 2, "chords": [ch("Dm7"), ch("G7")],
         "melody": [[0, note_to_midi("F4"), 2], [2, note_to_midi("A4"), 2], [4, note_to_midi("B4"), 2], [6, note_to_midi("D5"), 2]]},
        {"name": "FINAL_CHORUS", "bars": 4, "chords": [ch("F#m7"), ch("B9"), ch("Emaj7"), ch("E6")],
         "melody": [[0, note_to_midi("A4"), 1.5], [1.5, note_to_midi("C#5"), 0.5], [2, note_to_midi("F#5"), 1], [3, note_to_midi("E5"), 1],
                    [4, note_to_midi("D#5"), 1], [5, note_to_midi("C#5"), 1], [6, note_to_midi("A4"), 2],
                    [8, note_to_midi("G#4"), 1.5], [9.5, note_to_midi("B4"), 0.5], [10, note_to_midi("E5"), 3],
                    [13, note_to_midi("B4"), 1], [14, note_to_midi("E5"), 2]]},
    ]
    return 100, "A minor / E major", sections


def fallback_03():
    ch = Chord
    sections = [
        {"name": "INTRO", "bars": 2, "chords": [ch("Cmaj7"), ch("F6")],
         "melody": [[0, note_to_midi("G4"), 1], [1, note_to_midi("E4"), 1], [2, note_to_midi("C4"), 2],
                    [4, note_to_midi("A4"), 1], [5, note_to_midi("F4"), 1], [6, note_to_midi("C5"), 2]]},
        {"name": "VERSE", "bars": 4, "chords": [ch("Cmaj7"), ch("Am7"), ch("Fmaj7"), ch("G7")],
         "melody": [[0, note_to_midi("E4"), 0.5], [0.5, note_to_midi("G4"), 0.5], [1, note_to_midi("C5"), 1.5], [2.5, note_to_midi("B4"), 0.5], [3, note_to_midi("A4"), 1],
                    [4, note_to_midi("G4"), 0.5], [4.5, note_to_midi("E4"), 0.5], [5, note_to_midi("C4"), 1], [6, note_to_midi("D4"), 1], [7, note_to_midi("E4"), 1],
                    [8, note_to_midi("F4"), 1], [9, note_to_midi("A4"), 1], [10, note_to_midi("C5"), 2],
                    [12, note_to_midi("B4"), 1], [13, note_to_midi("G4"), 1], [14, note_to_midi("D4"), 2]]},
        {"name": "CHORUS", "bars": 4, "chords": [ch("Fmaj7"), ch("G6"), ch("Em7"), ch("Am7"), ch("Dm7"), ch("G7"), ch("Cmaj7"), ch("Cmaj7")][:4],
         "melody": [[0, note_to_midi("C5"), 1.5], [1.5, note_to_midi("A4"), 0.5], [2, note_to_midi("F4"), 2],
                    [4, note_to_midi("B4"), 1], [5, note_to_midi("G4"), 1], [6, note_to_midi("D5"), 2],
                    [8, note_to_midi("G4"), 1.5], [9.5, note_to_midi("B4"), 0.5], [10, note_to_midi("E5"), 2],
                    [12, note_to_midi("C5"), 2], [14, note_to_midi("E4"), 2]]},
        {"name": "VERSE2", "bars": 4, "chords": [ch("Cmaj7"), ch("Am7"), ch("Fmaj7"), ch("G7")],
         "melody": [[0, note_to_midi("G4"), 0.5], [0.5, note_to_midi("E4"), 0.5], [1, note_to_midi("C4"), 1.5], [2.5, note_to_midi("D4"), 0.5], [3, note_to_midi("E4"), 1],
                    [4, note_to_midi("C4"), 1], [5, note_to_midi("E4"), 1], [6, note_to_midi("A4"), 2],
                    [8, note_to_midi("F4"), 1], [9, note_to_midi("C5"), 1], [10, note_to_midi("A4"), 2],
                    [12, note_to_midi("G4"), 2], [14, note_to_midi("B4"), 2]]},
        {"name": "BRIDGE", "bars": 4, "chords": [ch("Am7"), ch("Dm7"), ch("Em7"), ch("Fmaj7")],
         "melody": [[0, note_to_midi("E4"), 4], [4, note_to_midi("F4"), 4],
                    [8, note_to_midi("G4"), 4], [12, note_to_midi("A4"), 4]]},
        {"name": "FINAL_CHORUS", "bars": 4, "chords": [ch("Fmaj7"), ch("G6"), ch("Cmaj7"), ch("Fmaj7")],
         "melody": [[0, note_to_midi("C5"), 1.5], [1.5, note_to_midi("A4"), 0.5], [2, note_to_midi("F4"), 2],
                    [4, note_to_midi("B4"), 1], [5, note_to_midi("G4"), 1], [6, note_to_midi("D5"), 2],
                    [8, note_to_midi("E5"), 2], [10, note_to_midi("C5"), 2],
                    [12, note_to_midi("A4"), 2], [14, note_to_midi("F4"), 2]]},
        {"name": "TAG", "bars": 2, "chords": [ch("G7"), ch("C6")],
         "melody": [[0, note_to_midi("D4"), 1.5], [1.5, note_to_midi("B4"), 0.5], [2, note_to_midi("C5"), 2],
                    [4, note_to_midi("E5"), 2], [6, note_to_midi("C5"), 4]]},
    ]
    return 110, "C major", sections


fallback_lead_name = {}

SONGS_MANIFEST = [
    ("01-the-gap-between-if-and-else", "kimi-01.json", fallback_01, 11, "Muted Trumpet"),
    ("02-the-mnew-bug", "kimi-02.json", fallback_02, 22, "Vibraphone"),
    ("03-ascii-canonical", "kimi-03.json", fallback_03, 33, "Electric Piano"),
]


def main():
    only_check = "--check" in sys.argv
    results = {}
    for name, jf, fb, seed, lead_default in SONGS_MANIFEST:
        spec = os.path.join(HERE, "kimi-out", jf)
        print("[%s]" % name)
        try:
            tempo, key, sections, lead_name = parse_kimi_json(spec)
            print("  kimi spec OK: %d bpm, %s, %d sections (%d bars), lead=%s"
                  % (tempo, key, len(sections), sum(s["bars"] for s in sections), lead_name))
        except Exception as e:
            print("  kimi spec BAD: %s" % e)
        if only_check:
            continue
        out = os.path.join(SONGS, name + "-rerender.mid")
        src, tempo, key, bars, dur = compose_song(name, spec, out, fb, seed=seed,
                                                  default_lead=lead_default)
        results[name] = (src, tempo, key, bars, dur)
        print("  composed (%s): %d bpm, %s, %d bars -> %.1fs of music -> %s"
              % (src, tempo, key, bars, dur, out))
    if not only_check:
        print(json.dumps({k: v[4] for k, v in results.items()}, indent=1))


if __name__ == "__main__":
    main()
