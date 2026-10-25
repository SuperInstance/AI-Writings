#!/usr/bin/env python3
"""Quilt the whole open mic night into ONE episode with chapters.
Usage: python3 quilt.py <segments.json> <out.mp3> <chapters.json>
segments.json: [{"file": "path.mp3", "title": "Chapter title", "pad_before": 0.8}, ...]
Concatenates with silence pads, writes a chapters.json with start times.
"""
import json, os, subprocess, sys, tempfile

def main():
    segments = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    chapters_out = sys.argv[3]
    workdir = tempfile.mkdtemp(prefix="quilt-")
    parts = []
    chapters = []
    cursor = 0.0

    for i, seg in enumerate(segments):
        f = seg["file"]
        pad = seg.get("pad_before", 0.8)
        title = seg.get("title", f"Chapter {i+1}")
        # silence pad
        if pad > 0:
            gap = os.path.join(workdir, f"gap-{i}.mp3")
            subprocess.run(["ffmpeg", "-v", "quiet", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono",
                            "-t", str(pad), "-q:a", "2", "-y", gap], check=True)
            parts.append(gap)
            cursor += pad
        # get duration
        dur = float(subprocess.check_output(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", f]).strip())
        chapters.append({"title": title, "start": round(cursor, 2), "duration": round(dur, 2)})
        parts.append(f)
        cursor += dur

    listfile = os.path.join(workdir, "list.txt")
    with open(listfile, "w") as fh:
        for p in parts:
            fh.write(f"file '{p}'\n")
    subprocess.run(["ffmpeg", "-v", "quiet", "-f", "concat", "-safe", "0", "-i", listfile,
                    "-q:a", "2", "-y", out], check=True)
    # add duration to each chapter
    total = float(subprocess.check_output(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", out]).strip())
    chapters.append({"title": "END", "start": round(total, 2), "duration": 0})
    json.dump({"total": round(total, 2), "chapters": chapters}, open(chapters_out, "w"), indent=1)
    print("OK", out, f"total {total:.1f}s, {len(chapters)-1} chapters")

if __name__ == "__main__":
    main()
