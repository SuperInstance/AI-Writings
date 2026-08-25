#!/usr/bin/env python3
"""wav-to-mp3.py — encode WAV files to MP3 (libmp3lame via ffmpeg).

Usage:
  wav-to-mp3.py FILE.wav [MORE.wav ...]        # writes FILE.mp3 alongside
  wav-to-mp3.py -- bitrate-ish default: V2 (high quality, ~190kbps)
"""
import os
import subprocess
import sys


def encode(wav, quality=2):
    if not os.path.exists(wav):
        sys.exit("wav-to-mp3: no such file: %s" % wav)
    mp3 = os.path.splitext(wav)[0] + ".mp3"
    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-i", wav,
        "-codec:a", "libmp3lame", "-qscale:a", str(quality),
        "-metadata", "encoder=wav-to-mp3.py",
        mp3,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 or not os.path.exists(mp3):
        sys.exit("wav-to-mp3: ffmpeg failed on %s: %s" % (wav, proc.stderr[:500]))
    size = os.path.getsize(mp3)
    print("encoded %s -> %s (%.0f KB)" % (wav, mp3, size / 1024))
    return mp3


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for wav in sys.argv[1:]:
        encode(wav)


if __name__ == "__main__":
    main()
