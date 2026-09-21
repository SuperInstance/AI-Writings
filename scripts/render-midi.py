#!/usr/bin/env python3
"""render-midi.py — MIDI -> WAV via fluidsynth.

Usage:
  render-midi.py INPUT.mid OUTPUT.wav [--gain 0.8] [--sf2 PATH]

Renders a MIDI file to 44.1 kHz 16-bit RIFF WAVE using FluidSynth and the
FluidR3_GM soundfont (falls back to default-GM.sf2). Reverb/chorus on
(defaults) give the room tone; end-of-track tail is whatever the MIDI
itself contains — composers should append a few silent beats for ring-out.
"""
import argparse
import os
import shutil
import subprocess
import sys

SF2_CANDIDATES = [
    "/usr/share/sounds/sf2/FluidR3_GM.sf2",
    "/usr/share/sounds/sf2/default-GM.sf2",
]


def find_sf2(explicit=None):
    for cand in ([explicit] if explicit else SF2_CANDIDATES):
        if cand and os.path.exists(cand):
            return cand
    return None


def render(mid_path, wav_path, gain=0.8, sf2=None):
    sf2 = find_sf2(sf2)
    if not sf2:
        sys.exit("render-midi: no soundfont found (tried %s)" % SF2_CANDIDATES)
    if shutil.which("fluidsynth") is None:
        sys.exit("render-midi: fluidsynth not installed")
    cmd = [
        "fluidsynth", "-ni",
        "-g", str(gain),
        "-r", "44100",
        "-F", wav_path,
        sf2, mid_path,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 or not os.path.exists(wav_path):
        sys.exit("render-midi: fluidsynth failed: %s" % (proc.stderr or proc.stdout)[:800])
    return wav_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mid")
    ap.add_argument("wav")
    ap.add_argument("--gain", type=float, default=0.8)
    ap.add_argument("--sf2", default=None)
    a = ap.parse_args()
    render(a.mid, a.wav, gain=a.gain, sf2=a.sf2)
    print("rendered %s -> %s" % (a.mid, a.wav))


if __name__ == "__main__":
    main()
