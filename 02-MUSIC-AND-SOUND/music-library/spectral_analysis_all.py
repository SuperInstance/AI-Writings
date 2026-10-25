#!/usr/bin/env python3
"""Extended spectral analysis for all 366 tracks in the SongForge corpus."""

import os
import json
import wave
import struct
import math
import sys
from pathlib import Path

MUSIC_DIR = Path("/home/eileen/projects/ai-writings/music")
OUTPUT_FILE = MUSIC_DIR / "spectral_analysis_full.json"

def analyze_mp3(filepath):
    """Analyze an MP3 file using subprocess + sox or fallback to raw analysis."""
    import subprocess
    
    # Try using ffmpeg to decode to raw PCM
    try:
        result = subprocess.run(
            ["ffmpeg", "-i", str(filepath), "-f", "s16le", "-ac", "1", "-ar", "22050", "-"],
            capture_output=True, timeout=60
        )
        raw = result.stdout
    except Exception as e:
        return {"error": str(e), "file": filepath.name}
    
    if len(raw) < 4:
        return {"error": "too short", "file": filepath.name}
    
    # Parse 16-bit signed LE samples
    n_samples = len(raw) // 2
    samples = struct.unpack(f'<{n_samples}h', raw)
    
    # Basic stats
    n = len(samples)
    if n == 0:
        return {"error": "no samples", "file": filepath.name}
    
    # RMS
    sum_sq = sum(s * s for s in samples)
    rms = math.sqrt(sum_sq / n)
    
    # Peak
    peak = max(abs(s) for s in samples) / 32768.0
    
    # Crest factor
    crest = (peak / rms) if rms > 0 else 0
    
    # Zero crossing rate
    zcr_count = 0
    for i in range(1, n):
        if (samples[i] >= 0) != (samples[i-1] >= 0):
            zcr_count += 1
    zcr = zcr_count / n
    
    # Dynamic range (difference between max and min RMS frames)
    frame_size = 2205  # 0.1s at 22050Hz
    n_frames = n // frame_size
    if n_frames > 0:
        frame_rms = []
        for f in range(n_frames):
            start = f * frame_size
            end = start + frame_size
            frame_sum_sq = sum(s * s for s in samples[start:end])
            frame_rms.append(math.sqrt(frame_sum_sq / frame_size))
        
        sorted_rms = sorted(frame_rms)
        # Dynamic range: difference between 95th and 5th percentile RMS in dB
        p95 = sorted_rms[int(0.95 * len(sorted_rms))] if len(sorted_rms) > 20 else max(sorted_rms)
        p5 = sorted_rms[int(0.05 * len(sorted_rms))] if len(sorted_rms) > 20 else min(sorted_rms)
        dr_db = 20 * math.log10(p95 / (p5 + 1e-10)) if p5 > 0 else 0
    else:
        dr_db = 0
    
    # Duration
    duration = n / 22050.0
    
    return {
        "file": filepath.name,
        "path": str(filepath.relative_to(MUSIC_DIR)),
        "duration_s": round(duration, 2),
        "rms": round(rms / 32768.0, 6),
        "peak": round(peak, 4),
        "crest_factor": round(crest, 2),
        "zcr": round(zcr, 6),
        "dynamic_range_db": round(dr_db, 2),
        "file_size_mb": round(filepath.stat().st_size / (1024*1024), 2),
        "n_samples": n,
    }

def main():
    # Find all MP3 files
    mp3_files = sorted(MUSIC_DIR.rglob("*.mp3"))
    print(f"Found {len(mp3_files)} MP3 files", file=sys.stderr)
    
    results = {}
    
    # Load existing analysis to skip already-analyzed
    existing = {}
    if OUTPUT_FILE.exists():
        try:
            existing = json.loads(OUTPUT_FILE.read_text())
            print(f"Already analyzed: {len(existing)}", file=sys.stderr)
        except:
            pass
    
    for i, f in enumerate(mp3_files):
        rel = str(f.relative_to(MUSIC_DIR))
        if rel in existing and 'error' not in existing[rel]:
            results[rel] = existing[rel]
            continue
        
        print(f"[{i+1}/{len(mp3_files)}] {rel}", file=sys.stderr)
        analysis = analyze_mp3(f)
        analysis["path"] = rel
        results[rel] = analysis
        
        # Save periodically
        if (i + 1) % 20 == 0:
            OUTPUT_FILE.write_text(json.dumps(results, indent=2))
            print(f"  Saved {len(results)} analyses", file=sys.stderr)
    
    # Final save
    OUTPUT_FILE.write_text(json.dumps(results, indent=2))
    print(f"\nDone! {len(results)} tracks analyzed.", file=sys.stderr)
    
    # Print summary stats
    valid = {k: v for k, v in results.items() if 'error' not in v}
    print(f"Valid analyses: {len(valid)}", file=sys.stderr)
    
    if valid:
        rms_vals = [v['rms'] for v in valid.values()]
        zcr_vals = [v['zcr'] for v in valid.values()]
        dr_vals = [v['dynamic_range_db'] for v in valid.values()]
        dur_vals = [v['duration_s'] for v in valid.values()]
        
        print(f"\nRMS:  min={min(rms_vals):.4f} max={max(rms_vals):.4f} mean={sum(rms_vals)/len(rms_vals):.4f}", file=sys.stderr)
        print(f"ZCR:  min={min(zcr_vals):.4f} max={max(zcr_vals):.4f} mean={sum(zcr_vals)/len(zcr_vals):.4f}", file=sys.stderr)
        print(f"DR:   min={min(dr_vals):.2f} max={max(dr_vals):.2f} mean={sum(dr_vals)/len(dr_vals):.2f}", file=sys.stderr)
        print(f"Dur:  min={min(dur_vals):.1f} max={max(dur_vals):.1f} mean={sum(dur_vals)/len(dur_vals):.1f}", file=sys.stderr)

if __name__ == "__main__":
    main()
