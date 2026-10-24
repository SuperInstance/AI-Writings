#!/usr/bin/env python3
"""
Generate atmospheric music beds using ffmpeg synthesis and mix with narration.
Each episode gets a unique mood via different frequencies, filters, and effects.
"""
import subprocess, os, sys

FFMPEG = __import__("imageio_ffmpeg").get_ffmpeg_exe()
OUT = "/home/eileen/projects/ai-writings/podcasts"

def run(cmd):
    """Run ffmpeg command, return success."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[-500:]}")
        return False
    return True

def get_duration(path):
    """Get duration of audio file in seconds."""
    result = subprocess.run([FFMPEG, "-i", path, "-f", "null", "-"], 
                          capture_output=True, text=True)
    # Parse duration from stderr
    for line in result.stderr.split('\n'):
        if 'Duration:' in line:
            time_str = line.split('Duration:')[1].split(',')[0].strip()
            h, m, s = time_str.split(':')
            return int(h)*3600 + int(m)*60 + float(s)
    return 0

episodes = [
    {
        "prefix": "episode-1-the-hundred-hooks",
        "music_mood": "contemplative",  # Low drone + ocean
        # Layered low-frequency drone with slow tremolo for "pattern emerging" feel
        "music_cmd": [
            "-f", "lavfi", "-i", 
            "sine=frequency=55:duration=180,volume=0.3,tremolo=f=0.3:d=0.5,"
            "aecho=0.8:0.9:1000:0.3,lowpass=f=400",
            "-f", "lavfi", "-i",
            "anoisesrc=d=180:c=pink:a=0.05,lowpass=f=800,highpass=f=100",
            "-f", "lavfi", "-i",
            "sine=frequency=110:duration=180,volume=0.1,tremolo=f=0.2:d=0.3",
            "-filter_complex",
            "[0:a][1:a][2:a]amix=inputs=3:duration=longest:weights=1 0.5 0.7,"
            "afade=t=in:st=0:d=3,afade=t=out:st=175:d=5",
        ],
    },
    {
        "prefix": "episode-2-the-bilge-pump-and-the-substrate",
        "music_mood": "industrial",  # Machinery hum + water
        # Industrial drone with mechanical rhythm
        "music_cmd": [
            "-f", "lavfi", "-i",
            "sine=frequency=60:duration=180,volume=0.25,tremolo=f=2:d=0.4,"
            "aecho=0.7:0.8:500:0.4,lowpass=f=600",
            "-f", "lavfi", "-i",
            "anoisesrc=d=180:c=brown:a=0.08,lowpass=f=500",
            "-f", "lavfi", "-i",
            "sine=frequency=82:duration=180,volume=0.08,tremolo=f=0.5:d=0.2",
            "-filter_complex",
            "[0:a][1:a][2:a]amix=inputs=3:duration=longest:weights=1 0.7 0.5,"
            "afade=t=in:st=0:d=4,afade=t=out:st=175:d=5",
        ],
    },
    {
        "prefix": "episode-3-the-welders-prayer-at-0230",
        "music_mood": "sacred",  # Sparse, holy, 2AM
        # Very sparse high tones like distant church bell + silence
        "music_cmd": [
            "-f", "lavfi", "-i",
            "sine=frequency=220:duration=180,volume=0.08,"
            "aecho=0.9:0.95:3000:0.2,lowpass=f=800",
            "-f", "lavfi", "-i",
            "anoisesrc=d=180:c=pink:a=0.03,lowpass=f=300",
            "-f", "lavfi", "-i",
            "sine=frequency=165:duration=180,volume=0.05,tremolo=f=0.15:d=0.3,"
            "aecho=0.8:0.9:2000:0.3",
            "-filter_complex",
            "[0:a][1:a][2:a]amix=inputs=3:duration=longest:weights=1 0.5 0.8,"
            "afade=t=in:st=0:d=5,afade=t=out:st=175:d=8",
        ],
    },
    {
        "prefix": "episode-4-darmok-at-the-noise-floor",
        "music_mood": "haunting",  # Electronic, failing to connect
        # Haunting electronic undertones, dissonant
        "music_cmd": [
            "-f", "lavfi", "-i",
            "sine=frequency=49:duration=300,volume=0.2,tremolo=f=0.4:d=0.6,"
            "aecho=0.8:0.9:1500:0.35,lowpass=f=500",
            "-f", "lavfi", "-i", 
            "sine=frequency=98:duration=300,volume=0.1,vibrato=f=5:d=0.5,"
            "aecho=0.7:0.85:800:0.3",
            "-f", "lavfi", "-i",
            "anoisesrc=d=300:c=white:a=0.02,lowpass=f=2000,highpass=f=200",
            "-filter_complex",
            "[0:a][1:a][2:a]amix=inputs=3:duration=longest:weights=1 0.6 0.4,"
            "afade=t=in:st=0:d=4,afade=t=out:st=295:d=8",
        ],
    },
]

for ep in episodes:
    prefix = ep["prefix"]
    narration_path = f"{OUT}/{prefix}-narration-full.wav"
    music_path = f"{OUT}/{prefix}-music-bed.wav"
    final_path = f"{OUT}/{prefix}-final.mp3"
    
    print(f"\n=== {prefix} ({ep['music_mood']}) ===")
    
    # Check narration exists
    if not os.path.exists(narration_path):
        print(f"  ❌ Narration not found: {narration_path}")
        continue
    
    nar_duration = get_duration(narration_path)
    print(f"  Narration duration: {nar_duration:.1f}s ({nar_duration/60:.1f} min)")
    
    # Generate music bed
    print(f"  Generating music bed ({ep['music_mood']})...")
    music_cmd = [FFMPEG, "-y"] + ep["music_cmd"] + ["-t", str(int(nar_duration) + 10), music_path]
    if not run(music_cmd):
        print(f"  ⚠️ Music generation failed, trying simpler approach...")
        # Fallback: simple low drone
        run([FFMPEG, "-y", "-f", "lavfi", "-i",
             f"sine=frequency=55:duration={int(nar_duration)+10},volume=0.15,lowpass=f=400",
             music_path])
    
    # Mix narration with music bed
    # Music at 15% volume, ducked under narration
    print(f"  Mixing narration + music bed...")
    mix_cmd = [
        FFMPEG, "-y",
        "-i", narration_path,
        "-i", music_path,
        "-filter_complex",
        # Duck music to 12% volume under narration
        "[1:a]volume=0.12[bg];"
        "[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2,"
        "afade=t=in:st=0:d=2,afade=t=out:st=" + str(int(nar_duration) - 3) + ":d=3",
        "-c:a", "libmp3lame", "-b:a", "128k",
        final_path
    ]
    
    if run(mix_cmd):
        size_mb = os.path.getsize(final_path) / (1024*1024)
        final_duration = get_duration(final_path)
        print(f"  ✅ {os.path.basename(final_path)} ({final_duration:.1f}s, {size_mb:.1f} MB)")
    else:
        print(f"  ❌ Mixing failed")

print("\n=== All episodes mixed ===")
