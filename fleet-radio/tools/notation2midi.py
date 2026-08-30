#!/usr/bin/env python3
"""
notation2midi.py — the oven's missing part.

The jam sessions' playing lives in text notation (r1-sax.txt, transcripts)
but MIDI Studio (localhost:5556) renders flakily (Set 23: 209 bytes).
This renders the notation DIRECTLY — no external service, no deps.

Notation understood (all seen in real jam output):
  "C4 E5 B4 | squall"        notes | annotation   (one line = one bar)
  "B2: C#5 D5 E5 (dishpit)"  labeled bar
  "BAR 1: C5 E5 G5 | sweep"  transcript form
  "rest"                     a silent bar
  "G1x5" / "G1*5"            a note hit 5 times
  "#" after a note           accent (velocity boost)
Chords: bracketed [C4 E4 G4] play together. Sustains: "C4~2" = 2 beats.

Usage: notation2midi.py <out.mid> --track "name=file [file...]" ...
       --bpm 88 --ppq 480 --beats-per-bar 5
Each --track becomes a MIDI track on its own channel.
"""
import argparse
import re
import struct
import sys

NOTE_RE = re.compile(r'([A-Ga-g])([#b]?)(-?\d)(?:~([\d.]+))?')
BAR_RE = re.compile(r'^(?:B(?:AR)?\s*-?\s*(\d+)\s*[:.]?)?\s*(.*)$', re.I)


def note_to_midi(token: str):
    m = NOTE_RE.fullmatch(token.rstrip('#').rstrip('*x0123456789'))
    if not m:
        # forms like G1x5 handled by caller; here strict single notes
        m2 = re.fullmatch(r'([A-Ga-g])([#b]?)(-?\d)', token)
        if not m2:
            return None
        m = m2
    letters = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    name, acc, octv = m.group(1).upper(), m.group(2), int(m.group(3))
    v = letters[name] + (1 if acc == '#' else -1 if acc == 'b' else 0)
    return 12 * (octv + 1) + v


def parse_bar(text: str):
    """Return list of events: ('note', midi, beats, accent) or ('rest',)."""
    text = text.split('|')[0].split('(')[0].strip()  # drop annotations
    if not text or text.lower() in ('rest', 'rests', 'silence', '—', '-'):
        return [('rest',)]
    events = []
    # pull bracketed chords out first so whitespace inside [ ] survives tokenization
    chords = re.findall(r'\[[^\]]+\]', text)
    remainder = re.sub(r'\[[^\]]+\]', ' ', text)
    for tok in re.split(r'[,\s]+', remainder):
        if not tok:
            continue
        accent = tok.endswith('#')
        rep = re.search(r'[x*](\d+)$', tok)
        times = int(rep.group(1)) if rep else 1
        base = re.sub(r'[x*]\d+$', '', tok).rstrip('#').rstrip('.')
        chord = base.startswith('[') and base.endswith(']')
        if chord:
            notes = [note_to_midi(n) for n in base[1:-1].split()]
            notes = [n for n in notes if n is not None]
            for t in range(times):
                events.append(('chord', notes, 1.0, accent))
            continue
        sus = re.search(r'~([\d.]+)$', base)
        beats = float(sus.group(1)) if sus else 1.0
        clean = re.sub(r'~[\d.]+$', '', base)
        n = note_to_midi(clean)
        if n is None:
            continue
        for t in range(times):
            events.append(('note', n, beats, accent))
    for base in chords:
        accent = base.endswith(']#')
        notes = [note_to_midi(n) for n in base[1:-1].split()]
        notes = [n for n in notes if n is not None]
        if notes:
            events.append(('chord', notes, 1.0, accent))
    return events or [('rest',)]


def parse_file(path: str):
    """Yield bars (list of events) from one notation file."""
    bars = []
    for line in open(path, encoding='utf-8', errors='replace'):
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('---'):
            continue
        m = re.match(r'^(?:B(?:AR)?\s*-?\s*\d+\s*[:.]?)\s*(.*)$', line, re.I)
        body = m.group(1) if m else line
        # markdown transcript lines: "BAR 1: notes | anno"
        if re.match(r'^\*?\*?BAR', body, re.I):
            continue
        bars.append(parse_bar(body))
    return bars


# ── minimal MIDI writer (SMF format 1) ─────────────────────────────

def vlq(n: int) -> bytes:
    out = bytearray([n & 0x7F])
    n >>= 7
    while n:
        out.insert(0, 0x80 | (n & 0x7F))
        n >>= 7
    return bytes(out)


def track_bytes(events, channel=0, program=0, velocity=84):
    """events: list of (start_tick, kind, midi, dur_ticks, vel)"""
    ev = bytearray()
    ev += b'\x00' + bytes([0xC0 | channel, program])  # program change at t=0
    seq = sorted(events, key=lambda e: e[0])
    last = 0
    for start, kind, midi, dur, vel in seq:
        if kind == 'on':
            msg = (0x90 | channel, midi, vel)
        else:
            msg = (0x80 | channel, midi, 0x40)
        delta = start - last
        if delta < 0:
            continue
        ev += vlq(delta) + bytes(msg)
        last = start
    ev += vlq(0) + b'\xff\x2f\x00'  # end of track
    return b'MTrk' + struct.pack('>I', len(ev)) + bytes(ev)


def build(paths, names=None, bpm=88, ppq=480, bpb=5):
    header = b'MThd' + struct.pack('>IHHH', 6, 1, len(paths) + 1, ppq)
    tempo = int(60_000_000 / bpm)
    t0 = (vlq(0) + b'\xff\x51\x03' + struct.pack('>I', tempo)[1:]
          + vlq(0) + b'\xff\x58\x04' + bytes([bpb, 2, 24, 8]) + vlq(0) + b'\xff\x2f\x00')
    meta = b'MTrk' + struct.pack('>I', len(t0)) + t0
    out = [header, meta]
    for i, p in enumerate(paths):
        channel = i % 16
        if channel == 9:
            channel = 10  # keep off the drum channel unless intended
        events = []
        tick = 0
        names_i = names[i] if names and i < len(names) else f'tr{i}'
        prog = {'sax': 66, 'trumpet': 56, 'piano': 0, 'steam': 91,
                'griddle': 30, 'dishpit': 11, 'piano/waitress': 0}.get(
            names_i.lower(), 0)
        for bar in parse_file(p):
            beat = 0.0
            for kind, *rest in bar:
                if kind == 'rest':
                    beat += bpb
                    continue
                if kind == 'chord':
                    notes, beats, accent = rest
                    st = tick + int(beat * ppq)
                    d = int(beats * ppq * 0.9)
                    for n in notes:
                        events.append((st, 'on', n, d, 84))
                        events.append((st + d, 'off', n, 0, 0))
                    beat += beats
                    continue
                n, beats, accent = rest
                st = tick + int(beat * ppq)
                d = int(beats * ppq * 0.85)
                vel = 110 if accent else 84
                events.append((st, 'on', n, d, vel))
                events.append((st + d, 'off', n, 0, 0))
                beat += beats
            tick += bpb * ppq
        out.append(track_bytes(events, channel=channel, program=prog))
    return b''.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--track', action='append', required=True,
                    help='name=file[,file2...] (multiple files concatenate)')
    ap.add_argument('--bpm', type=float, default=88)
    ap.add_argument('--ppq', type=int, default=480)
    ap.add_argument('--beats-per-bar', type=int, default=5)
    a = ap.parse_args()
    paths, names = [], []
    for t in a.track:
        name, files = t.split('=', 1)
        for f in files.split(','):
            paths.append(f)
            names.append(name)
    data = build(paths, names, a.bpm, a.ppq, a.beats_per_bar)
    open(a.out, 'wb').write(data)
    print(f'wrote {a.out}: {len(data)} bytes, {len(paths)} tracks, '
          f'{a.bpm} BPM, {a.beats_per_bar}/4 meter')


if __name__ == '__main__':
    main()
