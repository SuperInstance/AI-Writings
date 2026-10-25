#!/usr/bin/env python3
"""
SongForge: Audio Feature Analysis
Extracts spectral and temporal features from all MMX tracks.
Produces a CSV and summary statistics.
"""
import os
import sys
import json
import csv
import librosa
import numpy as np
from pathlib import Path

MUSIC_ROOT = Path("/home/eileen/projects/ai-writings/music")
OUTPUT_DIR = Path("/home/eileen/projects/ai-writings/music/analysis")
OUTPUT_DIR.mkdir(exist_ok=True)

def analyze_track(filepath):
    """Extract audio features from a track."""
    try:
        y, sr = librosa.load(str(filepath), sr=22050, mono=True)
    except Exception as e:
        return {"error": str(e)}

    duration = len(y) / sr
    
    # Spectral features
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y)[0]
    rms = librosa.feature.rms(y=y)[0]
    
    # Tempo and beat
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    
    # Chroma
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)
    
    # Spectral contrast
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    contrast_mean = contrast.mean(axis=1)
    
    # MFCCs (first 13)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_means = mfccs.mean(axis=1)
    
    # Spectral flatness (measure of noise-like vs tonal)
    flatness = librosa.feature.spectral_flatness(y=y)[0]
    
    return {
        "duration_sec": round(duration, 2),
        "sample_rate": sr,
        "tempo_bpm": round(float(tempo), 1) if not isinstance(tempo, np.ndarray) else round(float(tempo[0]), 1),
        "spectral_centroid_mean": round(float(np.mean(spectral_centroids)), 1),
        "spectral_centroid_std": round(float(np.std(spectral_centroids)), 1),
        "spectral_rolloff_mean": round(float(np.mean(spectral_rolloff)), 1),
        "spectral_bandwidth_mean": round(float(np.mean(spectral_bandwidth)), 1),
        "zero_crossing_rate_mean": round(float(np.mean(zero_crossing_rate)), 4),
        "rms_mean": round(float(np.mean(rms)), 4),
        "rms_std": round(float(np.std(rms)), 4),
        "spectral_flatness_mean": round(float(np.mean(flatness)), 4),
        "dynamic_range": round(float(np.percentile(rms, 95) - np.percentile(rms, 5)), 4),
        "chroma_means": [round(float(x), 3) for x in chroma_mean],
        "contrast_means": [round(float(x), 3) for x in contrast_mean],
        "mfcc_means": [round(float(x), 2) for x in mfcc_means],
    }

def main():
    # Find all MP3 files
    mp3_files = sorted(MUSIC_ROOT.rglob("*.mp3"))
    print(f"Found {len(mp3_files)} MP3 files")
    
    results = []
    
    for i, filepath in enumerate(mp3_files):
        rel_path = filepath.relative_to(MUSIC_ROOT)
        session = filepath.parent.name
        filename = filepath.name
        filesize_mb = filepath.stat().st_size / (1024 * 1024)
        
        print(f"[{i+1}/{len(mp3_files)}] {rel_path} ({filesize_mb:.2f} MB)...", end=" ", flush=True)
        
        features = analyze_track(filepath)
        
        if "error" in features:
            print(f"ERROR: {features['error']}")
            continue
        
        row = {
            "session": session,
            "filename": filename,
            "filesize_mb": round(filesize_mb, 2),
            **features,
        }
        results.append(row)
        print(f"✓ {features['duration_sec']}s, {features['tempo_bpm']} BPM, centroid {features['spectral_centroid_mean']}Hz")
    
    # Write CSV
    csv_path = OUTPUT_DIR / "features.csv"
    if results:
        # Flatten nested lists for CSV
        flat_results = []
        for r in results:
            flat = {}
            for k, v in r.items():
                if isinstance(v, list):
                    for j, item in enumerate(v):
                        flat[f"{k}_{j}"] = item
                else:
                    flat[k] = v
            flat_results.append(flat)
        
        fieldnames = sorted(set().union(*(r.keys() for r in flat_results)))
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(flat_results)
        
        print(f"\nCSV written to {csv_path}")
    
    # Write JSON
    json_path = OUTPUT_DIR / "features.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"JSON written to {json_path}")
    
    # Summary statistics
    if results:
        durations = [r["duration_sec"] for r in results]
        tempos = [r["tempo_bpm"] for r in results]
        centroids = [r["spectral_centroid_mean"] for r in results]
        flatnesses = [r["spectral_flatness_mean"] for r in results]
        dynamic_ranges = [r["dynamic_range"] for r in results]
        
        print("\n" + "="*60)
        print("SUMMARY STATISTICS")
        print("="*60)
        print(f"Tracks analyzed: {len(results)}")
        print(f"\nDuration: mean={np.mean(durations):.1f}s, min={np.min(durations):.1f}s, max={np.max(durations):.1f}s")
        print(f"Tempo: mean={np.mean(tempos):.1f}, min={np.min(tempos):.1f}, max={np.max(tempos):.1f}")
        print(f"Spectral Centroid: mean={np.mean(centroids):.0f}Hz, min={np.min(centroids):.0f}Hz, max={np.max(centroids):.0f}Hz")
        print(f"Spectral Flatness: mean={np.mean(flatnesses):.4f}, min={np.min(flatnesses):.4f}, max={np.max(flatnesses):.4f}")
        print(f"Dynamic Range: mean={np.mean(dynamic_ranges):.4f}, min={np.min(dynamic_ranges):.4f}, max={np.max(dynamic_ranges):.4f}")
        
        # Top 5 longest tracks
        print("\nTop 5 Longest Tracks:")
        by_duration = sorted(results, key=lambda x: x["duration_sec"], reverse=True)
        for r in by_duration[:5]:
            print(f"  {r['session']}/{r['filename']}: {r['duration_sec']}s ({r['filesize_mb']} MB)")
        
        # Top 5 by spectral centroid (brightest)
        print("\nTop 5 Brightest Tracks (highest spectral centroid):")
        by_centroid = sorted(results, key=lambda x: x["spectral_centroid_mean"], reverse=True)
        for r in by_centroid[:5]:
            print(f"  {r['session']}/{r['filename']}: {r['spectral_centroid_mean']}Hz")
        
        # Top 5 by flatness (most noise-like)
        print("\nTop 5 Most Noise-like Tracks (highest flatness):")
        by_flat = sorted(results, key=lambda x: x["spectral_flatness_mean"], reverse=True)
        for r in by_flat[:5]:
            print(f"  {r['session']}/{r['filename']}: {r['spectral_flatness_mean']:.4f}")
        
        # Correlation: filesize vs duration
        sizes = [r["filesize_mb"] for r in results]
        corr_size_dur = np.corrcoef(sizes, durations)[0, 1]
        print(f"\nCorrelation (filesize ↔ duration): r={corr_size_dur:.4f}")
        
        # Correlation: duration vs spectral centroid
        corr_dur_cent = np.corrcoef(durations, centroids)[0, 1]
        print(f"Correlation (duration ↔ centroid): r={corr_dur_cent:.4f}")
        
        # Correlation: duration vs flatness
        corr_dur_flat = np.corrcoef(durations, flatnesses)[0, 1]
        print(f"Correlation (duration ↔ flatness): r={corr_dur_flat:.4f}")
        
        # Per-session summary
        print("\n" + "="*60)
        print("PER-SESSION SUMMARY")
        print("="*60)
        sessions = sorted(set(r["session"] for r in results))
        for sess in sessions:
            sess_results = [r for r in results if r["session"] == sess]
            sess_durations = [r["duration_sec"] for r in sess_results]
            sess_centroids = [r["spectral_centroid_mean"] for r in sess_results]
            sess_flat = [r["spectral_flatness_mean"] for r in sess_results]
            print(f"\n{sess} ({len(sess_results)} tracks):")
            print(f"  Duration: mean={np.mean(sess_durations):.1f}s, range={np.min(sess_durations):.1f}-{np.max(sess_durations):.1f}s")
            print(f"  Centroid: mean={np.mean(sess_centroids):.0f}Hz")
            print(f"  Flatness: mean={np.mean(sess_flat):.4f}")
            print(f"  Tempo: mean={np.mean([r['tempo_bpm'] for r in sess_results]):.1f}")

if __name__ == "__main__":
    main()
