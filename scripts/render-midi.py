#!/usr/bin/env python3
"""Render MIDI files to WAV.

Discovers MIDI files under fleet-radio/jam-session-*/ and renders each to a
sibling .wav file. Uses fluidsynth when available together with a SoundFont,
otherwise falls back to a pure-numpy additive synthesizer.

Usage:
    render-midi.py              # render all discovered .mid files
    render-midi.py some.mid     # render a single .mid file
"""

from __future__ import annotations

import glob
import os
import shutil
import subprocess
import sys
import tempfile
import wave
from bisect import bisect_right
from pathlib import Path

import mido
import numpy as np

SAMPLE_RATE = 44100
DEFAULT_TEMPO = 500000  # microseconds per beat
DEFAULT_TPQ = 480

ATTACK_S = 0.008
RELEASE_S = 0.06
SUSTAIN_LEVEL = 0.6
TAIL_S = max(RELEASE_S, 0.5)

DRUM_DECAY_S = 0.15
DRUM_LOW_HZ = 150.0
DRUM_HIGH_HZ = 8000.0

TARGET_PEAK = 10.0 ** (-1.0 / 20.0)  # -1 dBFS


# ----------------------------------------------------------------- tempo map

def build_tempo_map(mf):
    """Return (segments, tpqn) where segments is a sorted list of
    (start_tick, seconds_at_start_tick, tempo_from_start_tick)."""
    tpqn = mf.ticks_per_beat or DEFAULT_TPQ
    events = []
    for track in mf.tracks:
        tick = 0
        for msg in track:
            tick += msg.time
            if msg.type == "set_tempo":
                events.append((tick, msg.tempo))
    events.sort()
    segments = [(0, 0.0, DEFAULT_TEMPO)]
    for tick, tempo in events:
        start_tick, start_sec, cur_tempo = segments[-1]
        sec = start_sec + (tick - start_tick) * cur_tempo / 1e6 / tpqn
        if tick == start_tick:
            segments[-1] = (tick, sec, tempo)
        else:
            segments.append((tick, sec, tempo))
    return segments, tpqn


def tick_to_seconds(segments, starts, tpqn, tick):
    """Convert an absolute tick to seconds via linear interpolation
    between tempo changes."""
    idx = bisect_right(starts, tick) - 1
    start_tick, start_sec, tempo = segments[idx]
    return start_sec + (tick - start_tick) * tempo / 1e6 / tpqn


# ------------------------------------------------------------ note extraction

def extract_events(mf):
    """Return (notes, drums, last_time).

    notes: [(start_s, end_s, midi_note, velocity)] for non-drum channels
    drums: [(start_s, midi_note, velocity)] for channel 9 note-ons
    """
    segments, tpqn = build_tempo_map(mf)
    starts = [s[0] for s in segments]
    notes = []
    drums = []
    active = {}  # (channel, note) -> (start_s, velocity)
    tick = 0
    last_t = 0.0
    for msg in mido.merge_tracks(mf.tracks):
        tick += msg.time
        t = tick_to_seconds(segments, starts, tpqn, tick)
        last_t = t
        if not hasattr(msg, "channel"):
            continue
        if msg.type not in ("note_on", "note_off"):
            continue  # control/program/pitchwheel have no .note
        if msg.channel == 9:
            if msg.type == "note_on" and msg.velocity > 0:
                drums.append((t, msg.note, msg.velocity))
            continue
        key = (msg.channel, msg.note)
        if msg.type == "note_on" and msg.velocity > 0:
            if key in active:
                prev_start, prev_vel = active.pop(key)
                notes.append((prev_start, t, msg.note, prev_vel))
            active[key] = (t, msg.velocity)
        elif msg.type in ("note_off", "note_on"):  # note_on vel==0 ends a note
            if key in active:
                start, vel = active.pop(key)
                notes.append((start, t, msg.note, vel))
    # Close any hanging notes at the last event time.
    for (_channel, note), (start, vel) in active.items():
        notes.append((start, max(start + 0.25, last_t), note, vel))
    return notes, drums, last_t


# ------------------------------------------------------------------ synthesis

def _additive_tone(freq, t):
    return (np.sin(2.0 * np.pi * freq * t)
            + 0.4 * np.sin(4.0 * np.pi * freq * t)
            + 0.15 * np.sin(6.0 * np.pi * freq * t))


def render_note(buf, start, end, note, velocity):
    sr = SAMPLE_RATE
    freq = 440.0 * 2.0 ** ((note - 69) / 12.0)
    amp = velocity / 127.0
    i0 = max(0, int(round(start * sr)))
    i1 = min(len(buf), int(round(end * sr)))
    i2 = min(len(buf), i1 + int(RELEASE_S * sr))
    if i0 >= len(buf):
        return
    env_end = amp * SUSTAIN_LEVEL
    if i1 > i0:
        t = np.arange(i0, i1) / sr - start
        dur = max(end - start, 1e-3)
        env = np.empty(i1 - i0)
        n_attack = min(int(ATTACK_S * sr), len(env))
        if n_attack:
            env[:n_attack] = np.linspace(0.0, 1.0, n_attack, endpoint=False)
        if len(env) > n_attack:
            td = np.arange(len(env) - n_attack) / sr
            tau = max((dur - ATTACK_S) / 3.0, 0.02)
            env[n_attack:] = SUSTAIN_LEVEL + (1.0 - SUSTAIN_LEVEL) * np.exp(-td / tau)
        buf[i0:i1] += amp * env * _additive_tone(freq, t)
        env_end = amp * env[-1]
    if i2 > i1:
        t = np.arange(i1, i2) / sr - start
        # release ramp relative to note-off (FIXED: was absolute buffer time)
        rel = 1.0 - (np.arange(i1, i2) - i1) / sr / RELEASE_S
        buf[i1:i2] += env_end * rel * _additive_tone(freq, t)


def render_drum(buf, start, note, velocity, rng):
    """Band-limited white-noise burst with exponential decay."""
    sr = SAMPLE_RATE
    i0 = int(round(start * sr))
    if i0 >= len(buf):
        return
    n = min(len(buf) - i0, int(DRUM_DECAY_S * 4.0 * sr))
    if n <= 0:
        return
    noise = rng.standard_normal(n)
    spec = np.fft.rfft(noise)
    freqs = np.fft.rfftfreq(n, 1.0 / sr)
    lo = DRUM_LOW_HZ * 2.0 ** ((note - 38) / 24.0)  # lower drums = darker band
    lo = min(max(lo, 60.0), 2000.0)
    spec[(freqs < lo) | (freqs > DRUM_HIGH_HZ)] = 0.0
    noise = np.fft.irfft(spec, n)
    peak = float(np.max(np.abs(noise)))
    if peak > 0.0:
        noise /= peak
    t = np.arange(n) / sr
    buf[i0:i0 + n] += (velocity / 127.0) * np.exp(-t / DRUM_DECAY_S) * noise


def synthesize(mid_path):
    mf = mido.MidiFile(str(mid_path))
    notes, drums, last_t = extract_events(mf)
    last_end = last_t
    for start, end, _note, _vel in notes:
        last_end = max(last_end, end)
    for start, _note, _vel in drums:
        last_end = max(last_end, start + DRUM_DECAY_S * 4.0)
    total = last_end + TAIL_S
    n = max(1, int(round(total * SAMPLE_RATE)))
    buf = np.zeros(n, dtype=np.float64)
    rng = np.random.default_rng(0xC0FFEE)
    for start, end, note, vel in notes:
        if end > start:
            render_note(buf, start, end, note, vel)
    for start, note, vel in drums:
        render_drum(buf, start, note, vel, rng)
    return buf


# ----------------------------------------------------------------- fluidsynth

def find_soundfont():
    candidates = sorted(glob.glob("/usr/share/sounds/sf2/**/*.sf2", recursive=True))
    return candidates[0] if candidates else None


def render_with_fluidsynth(mid_path):
    """Render via fluidsynth to mono float64 at SAMPLE_RATE; None on failure."""
    sf2 = find_soundfont()
    if not sf2:
        return None
    fd, raw_path = tempfile.mkstemp(suffix=".raw")
    os.close(fd)
    try:
        subprocess.run(
            ["fluidsynth", "-ni", "-T", "raw", "-F", raw_path,
             "-r", str(SAMPLE_RATE), "-g", "1.0", sf2, str(mid_path)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        data = np.fromfile(raw_path, dtype="<i2")
        if data.size == 0:
            return None
        if data.size % 2:
            data = data[:-1]
        stereo = data.reshape(-1, 2).astype(np.float64)
        return stereo.mean(axis=1) / 32768.0
    except (subprocess.CalledProcessError, OSError):
        return None
    finally:
        try:
            os.unlink(raw_path)
        except OSError:
            pass


# --------------------------------------------------------------------- output

def finalize(buf):
    """Normalize to -1 dBFS peak; return (buffer, peak_dBFS)."""
    peak = float(np.max(np.abs(buf))) if buf.size else 0.0
    if peak <= 0.0:
        buf = np.zeros(SAMPLE_RATE, dtype=np.float64)  # 1s of silence
    else:
        buf = buf * (TARGET_PEAK / peak)
    out_peak = float(np.max(np.abs(buf))) if buf.size else 0.0
    dbfs = 20.0 * np.log10(out_peak) if out_peak > 0.0 else float("-inf")
    return buf, dbfs


def write_wav(buf, wav_path):
    """Write mono 16-bit little-endian WAV at SAMPLE_RATE."""
    pcm = (np.clip(buf, -1.0, 1.0) * 32767.0).astype("<i2")
    with wave.open(str(wav_path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm.tobytes())


def is_valid_wav(path):
    try:
        with open(path, "rb") as f:
            head = f.read(12)
    except OSError:
        return False
    return len(head) >= 12 and head[:4] == b"RIFF" and head[8:12] == b"WAVE"


# ----------------------------------------------------------------------- main

def render(mid_path):
    buf = None
    if shutil.which("fluidsynth"):
        buf = render_with_fluidsynth(mid_path)
    if buf is None:
        buf = synthesize(mid_path)
    return finalize(buf)


def main():
    repo = Path(__file__).resolve().parent.parent
    if len(sys.argv) > 1 and sys.argv[1].endswith(".mid"):
        midi_paths = [Path(sys.argv[1])]
    else:
        midi_paths = sorted(repo.glob("fleet-radio/jam-session-*/*.mid"))
    for mid_path in midi_paths:
        wav_path = mid_path.with_suffix(".wav")
        if is_valid_wav(wav_path):
            print(f"SKIP {mid_path}")
            continue
        try:
            buf, dbfs = render(mid_path)
        except Exception as exc:  # noqa: BLE001 - keep the batch alive
            print(f"WARN {mid_path}: {exc}")
            continue
        write_wav(buf, wav_path)
        duration = len(buf) / SAMPLE_RATE
        dbfs_str = f"{dbfs:.1f}" if np.isfinite(dbfs) else "-inf"
        print(f"RENDER {mid_path} -> {wav_path} ({duration:.2f}s, peak dBFS {dbfs_str})")


if __name__ == "__main__":
    main()
