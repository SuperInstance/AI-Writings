#!/usr/bin/env python3
"""
The Sound of the Fleet — A Fleet Soundscape Generator
=====================================================

Each repo has a tone. Each cron firing is a beat. Test passes are harmonics.
Build failures are dissonance. This renders the fleet's state as 60 seconds
of audible sound — a sound signal, not a dashboard.

Maritime framing: this is how you hear where the land is when you can't see it.

Usage:
    python3 fleet_soundscape.py [--fleet-data data.json] [--output fleet-soundscape.wav]

If no fleet data is provided, a synthetic fleet state is generated from the
known fleet topology (32 repos, 5-stage pipeline, escalation engine).

Dependencies: numpy only. Output is raw WAV (no external codecs needed).
"""

import struct
import wave
import math
import random
import json
import sys
import os
from pathlib import Path

# ─── Fleet Topology ───────────────────────────────────────────────────────────

# Repos mapped to musical keys based on fleet role
REPO_VOICES = {
    "study-sunset-ecosystem": {"key": "C", "freq": 261.63, "role": "strings", "weight": 8702},
    "forgemaster":            {"key": "D", "freq": 293.66, "role": "brass",   "weight": 366},
    "lucineer-brain":         {"key": "E", "freq": 329.63, "role": "strings", "weight": 289},
    "cns-bridge":             {"key": "F", "freq": 349.23, "role": "brass",   "weight": 163},
    "fleet-wiki":             {"key": "G", "freq": 392.00, "role": "woodwind","weight": 80},
    "ai-writings":            {"key": "A", "freq": 440.00, "role": "strings", "weight": 500},
    "lucineer-relay":         {"key": "B", "freq": 493.88, "role": "brass",   "weight": 45},
    "vectorize-pipeline":     {"key": "C5","freq": 523.25, "role": "woodwind","weight": 30},
    "openrooms":              {"key": "D5","freq": 587.33, "role": "percussion","weight": 60},
    "log-ai":                 {"key": "E5","freq": 659.25, "role": "percussion","weight": 40},
    "escalation-engine":      {"key": "F5","freq": 698.46, "role": "brass",   "weight": 25},
}

# Model voices — each model has a register and timbre
MODEL_VOICES = {
    "deepseek-flash":  {"base_freq": 880.00, "harmonic_odd": True,  "decay": 0.3, "name": "piccolo"},
    "deepseek-pro":    {"base_freq": 130.81, "harmonic_odd": False, "decay": 1.2, "name": "cello"},
    "glm-5.2":         {"base_freq": 440.00, "harmonic_odd": False, "decay": 0.5, "name": "violin"},
    "hermes-405b":     {"base_freq": 65.41,  "harmonic_odd": True,  "decay": 2.5, "name": "organ"},
    "kimi-k3":         {"base_freq": 220.00, "harmonic_odd": True,  "decay": 0.4, "name": "harpsichord"},
    "claude-sonnet":   {"base_freq": 174.61, "harmonic_odd": False, "decay": 0.8, "name": "horn"},
    "claude-opus":     {"base_freq": 87.31,  "harmonic_odd": False, "decay": 1.5, "name": "bassoon"},
    "seed-mini":       {"base_freq": 698.46, "harmonic_odd": True,  "decay": 0.2, "name": "flute"},
    "nemotron-ultra":  {"base_freq": 110.00, "harmonic_odd": False, "decay": 1.0, "name": "tuba"},
}

# Event types mapped to sonic qualities
EVENT_MAP = {
    "test_pass":    {"wave": "sine",     "harmonic": True,  "amp": 0.15},
    "test_fail":    {"wave": "sawtooth", "harmonic": False, "amp": 0.35},
    "build_pass":   {"wave": "triangle", "harmonic": True,  "amp": 0.25},
    "build_fail":   {"wave": "square",   "harmonic": False, "amp": 0.45},
    "commit":       {"wave": "sine",     "harmonic": True,  "amp": 0.10},
    "deploy":       {"wave": "triangle", "harmonic": True,  "amp": 0.30},
    "cron_fire":    {"wave": "sine",     "harmonic": False, "amp": 0.05},
    "model_dispatch":{"wave": "sine",    "harmonic": True,  "amp": 0.08},
    "escalation":   {"wave": "sawtooth", "harmonic": False, "amp": 0.20},
}

# ─── Audio Synthesis ──────────────────────────────────────────────────────────

SAMPLE_RATE = 44100
DURATION = 60.0  # seconds

def generate_tone(freq, duration, wave_type="sine", amplitude=0.3, decay=0.5, harmonic=True):
    """Generate a single tone with envelope."""
    n_samples = int(SAMPLE_RATE * duration)
    t = [i / SAMPLE_RATE for i in range(n_samples)]
    
    samples = []
    for i, ti in enumerate(t):
        # Exponential decay envelope
        env = math.exp(-ti * (1.0 / max(decay, 0.01)))
        
        if wave_type == "sine":
            s = math.sin(2 * math.pi * freq * ti)
        elif wave_type == "square":
            s = 1.0 if math.sin(2 * math.pi * freq * ti) > 0 else -1.0
        elif wave_type == "sawtooth":
            s = 2.0 * (freq * ti - math.floor(freq * ti + 0.5))
        elif wave_type == "triangle":
            s = 2.0 * abs(2.0 * (freq * ti - math.floor(freq * ti + 0.5))) - 1.0
        else:
            s = math.sin(2 * math.pi * freq * ti)
        
        # Add harmonics for consonant tones
        if harmonic:
            s += 0.3 * math.sin(2 * math.pi * freq * 2 * ti) * env
            s += 0.15 * math.sin(2 * math.pi * freq * 3 * ti) * env
            s += 0.07 * math.sin(2 * math.pi * freq * 5 * ti) * env
        
        # Dissonance: add slight beating for failures
        if not harmonic:
            beat_freq = freq * 1.02  # slight detune for dissonance
            s += 0.5 * math.sin(2 * math.pi * beat_freq * ti) * env
        
        samples.append(s * env * amplitude)
    
    return samples

def generate_bell(freq, duration=2.0, amplitude=0.2):
    """Generate a bell-like tone (test pass)."""
    return generate_tone(freq, duration, wave_type="sine", amplitude=amplitude, decay=1.5, harmonic=True)

def generate_drum(freq=60, duration=0.3, amplitude=0.4):
    """Generate a drum-like hit (build event)."""
    n_samples = int(SAMPLE_RATE * duration)
    t = [i / SAMPLE_RATE for i in range(n_samples)]
    samples = []
    for ti in t:
        env = math.exp(-ti * 15)
        noise = (random.random() * 2 - 1) * 0.3
        tone = math.sin(2 * math.pi * freq * ti)
        samples.append((tone * 0.7 + noise * 0.3) * env * amplitude)
    return samples

def generate_pad(freq, duration=5.0, amplitude=0.08):
    """Generate a sustained pad (ambient bed for each repo)."""
    n_samples = int(SAMPLE_RATE * duration)
    t = [i / SAMPLE_RATE for i in range(n_samples)]
    samples = []
    for ti in t:
        # Slow attack and release
        attack = min(ti / 1.0, 1.0)
        release = min((duration - ti) / 2.0, 1.0) if ti > duration - 2.0 else 1.0
        env = attack * release
        s = math.sin(2 * math.pi * freq * ti) * 0.5
        s += math.sin(2 * math.pi * freq * 1.5 * ti) * 0.3
        s += math.sin(2 * math.pi * freq * 2 * ti) * 0.2
        # Slow LFO for movement
        lfo = 1.0 + 0.02 * math.sin(2 * math.pi * 0.1 * ti)
        samples.append(s * env * amplitude * lfo)
    return samples

def mix_into(buffer_samples, tone_samples, start_sample):
    """Mix tone samples into the buffer at the given position."""
    for i, s in enumerate(tone_samples):
        pos = start_sample + i
        if pos < len(buffer_samples):
            buffer_samples[pos] += s

def normalize(samples, target_peak=0.85):
    """Normalize to prevent clipping."""
    peak = max(abs(s) for s in samples) if samples else 1.0
    if peak == 0:
        return samples
    scale = target_peak / peak
    return [s * scale for s in samples]

# ─── Fleet Data Generation ────────────────────────────────────────────────────

def generate_synthetic_fleet():
    """Generate a realistic fleet state from known topology."""
    events = []
    
    # Cron firings — the heartbeat
    # lucineer-relay: every 3 seconds
    for t in range(0, 60, 3):
        events.append({"time": t, "type": "cron_fire", "repo": "lucineer-relay", "model": None})
    
    # Health checks: every 30 seconds
    for t in [5, 35]:
        for repo in ["cns-bridge", "log-ai"]:
            events.append({"time": t, "type": "cron_fire", "repo": repo, "model": None})
    
    # Test runs — the melodic content
    # study-sunset-ecosystem runs the most tests
    for _ in range(80):
        t = random.uniform(0, 60)
        passed = random.random() > 0.05  # 95% pass rate
        events.append({
            "time": t, 
            "type": "test_pass" if passed else "test_fail",
            "repo": "study-sunset-ecosystem",
            "model": None
        })
    
    # Other repos run fewer tests
    for repo in ["forgemaster", "lucineer-brain", "cns-bridge", "ai-writings"]:
        for _ in range(random.randint(5, 20)):
            t = random.uniform(0, 60)
            passed = random.random() > 0.08
            events.append({
                "time": t,
                "type": "test_pass" if passed else "test_fail",
                "repo": repo,
                "model": None
            })
    
    # Build events
    for _ in range(8):
        t = random.uniform(0, 60)
        passed = random.random() > 0.15
        repo = random.choice(["forgemaster", "lucineer-brain", "cns-bridge", "lucineer-relay"])
        events.append({
            "time": t,
            "type": "build_pass" if passed else "build_fail",
            "repo": repo,
            "model": None
        })
    
    # Commits
    for _ in range(15):
        t = random.uniform(0, 60)
        repo = random.choice(list(REPO_VOICES.keys()))
        events.append({"time": t, "type": "commit", "repo": repo, "model": None})
    
    # Deploys
    for _ in range(3):
        t = random.uniform(0, 60)
        events.append({"time": t, "type": "deploy", "repo": "lucineer-relay", "model": None})
    
    # Model dispatches — the melodic overlay
    models = list(MODEL_VOICES.keys())
    model_weights = [30, 25, 40, 3, 8, 12, 2, 15, 5]  # GLM plays the most
    
    for _ in range(50):
        t = random.uniform(0, 60)
        model = random.choices(models, weights=model_weights)[0]
        events.append({"time": t, "type": "model_dispatch", "repo": None, "model": model})
    
    # Escalations (rare — the drama)
    for _ in range(2):
        t = random.uniform(10, 50)
        events.append({"time": t, "type": "escalation", "repo": "cns-bridge", "model": None})
    
    return events

# ─── Composition Engine ───────────────────────────────────────────────────────

def compose_soundscape(events, duration=DURATION):
    """Compose the fleet soundscape from events."""
    total_samples = int(SAMPLE_RATE * duration)
    buffer = [0.0] * total_samples
    
    # Layer 1: Ambient pads — each repo's tonal center sustained
    print("  Layering ambient pads (repo tonal centers)...")
    for repo, voice in REPO_VOICES.items():
        pad = generate_pad(voice["freq"], duration, amplitude=0.04)
        mix_into(buffer, pad, 0)
    
    # Layer 2: Cron heartbeat — the rhythmic substrate
    print("  Layering cron heartbeat (3-second polyrhythm)...")
    for ev in events:
        if ev["type"] == "cron_fire":
            start = int(ev["time"] * SAMPLE_RATE)
            voice = REPO_VOICES.get(ev["repo"], {"freq": 100})
            # Short tick
            tick = generate_tone(voice["freq"] * 4, 0.05, "sine", 0.03, decay=0.05, harmonic=False)
            mix_into(buffer, tick, start)
    
    # Layer 3: Test results — bells and dissonance
    print("  Layering test events (bells for pass, dissonance for fail)...")
    for ev in events:
        if ev["type"] in ("test_pass", "test_fail"):
            start = int(ev["time"] * SAMPLE_RATE)
            voice = REPO_VOICES.get(ev["repo"], {"freq": 261.63})
            ev_config = EVENT_MAP[ev["type"]]
            
            if ev["type"] == "test_pass":
                # Consonant bell at the repo's frequency + perfect fifth
                tone = generate_bell(voice["freq"], 1.5, amplitude=ev_config["amp"])
                mix_into(buffer, tone, start)
                # Perfect fifth harmonic
                fifth = generate_bell(voice["freq"] * 1.5, 1.2, amplitude=ev_config["amp"] * 0.5)
                mix_into(buffer, fifth, start)
            else:
                # Dissonant cluster — tritone + detune
                tone = generate_tone(voice["freq"] * 1.414, 0.8, "sawtooth", ev_config["amp"], decay=0.8, harmonic=False)
                mix_into(buffer, tone, start)
                # Add a low rumble
                rumble = generate_drum(voice["freq"] * 0.25, 0.5, amplitude=0.2)
                mix_into(buffer, rumble, start)
    
    # Layer 4: Build events — drums
    print("  Layering build events (drums)...")
    for ev in events:
        if ev["type"] in ("build_pass", "build_fail"):
            start = int(ev["time"] * SAMPLE_RATE)
            ev_config = EVENT_MAP[ev["type"]]
            voice = REPO_VOICES.get(ev["repo"], {"freq": 100})
            
            if ev["type"] == "build_pass":
                drum = generate_drum(80, 0.4, amplitude=0.3)
                mix_into(buffer, drum, start)
                # Triumphant chord
                chord = generate_tone(voice["freq"], 1.0, "triangle", 0.15, decay=1.0, harmonic=True)
                mix_into(buffer, chord, start)
            else:
                # Heavy drum hit + dissonant cluster
                drum = generate_drum(45, 0.6, amplitude=0.5)
                mix_into(buffer, drum, start)
                crash = generate_tone(voice["freq"] * 1.414, 1.5, "square", 0.2, decay=1.0, harmonic=False)
                mix_into(buffer, crash, start)
    
    # Layer 5: Commits — string plucks
    print("  Layering commits (string plucks)...")
    for ev in events:
        if ev["type"] == "commit":
            start = int(ev["time"] * SAMPLE_RATE)
            voice = REPO_VOICES.get(ev["repo"], {"freq": 261.63})
            pluck = generate_tone(voice["freq"], 0.3, "sine", 0.08, decay=0.2, harmonic=True)
            mix_into(buffer, pluck, start)
    
    # Layer 6: Model dispatches — melodic overlay
    print("  Layering model dispatches (melodic voices)...")
    for ev in events:
        if ev["type"] == "model_dispatch" and ev["model"]:
            start = int(ev["time"] * SAMPLE_RATE)
            voice = MODEL_VOICES[ev["model"]]
            # Each model plays a short note in its register
            note = generate_tone(
                voice["base_freq"], 
                0.4, 
                "sine" if voice["harmonic_odd"] else "triangle",
                0.06,
                decay=voice["decay"],
                harmonic=voice["harmonic_odd"]
            )
            mix_into(buffer, note, start)
    
    # Layer 7: Deploys — brass fanfare
    print("  Layering deploys (brass fanfare)...")
    for ev in events:
        if ev["type"] == "deploy":
            start = int(ev["time"] * SAMPLE_RATE)
            # Quick ascending triad
            for i, mult in enumerate([1.0, 1.25, 1.5]):
                note = generate_tone(392.0 * mult, 0.8, "triangle", 0.2, decay=0.6, harmonic=True)
                mix_into(buffer, note, start + i * int(0.1 * SAMPLE_RATE))
    
    # Layer 8: Escalations — dramatic swells
    print("  Layering escalations (dramatic swells)...")
    for ev in events:
        if ev["type"] == "escalation":
            start = int(ev["time"] * SAMPLE_RATE)
            # Rising tone — the escalation climbing tiers
            n_samples_rise = int(SAMPLE_RATE * 2.0)
            for i in range(n_samples_rise):
                ti = i / SAMPLE_RATE
                freq_rise = 100 + 400 * (ti / 2.0)
                env = min(ti / 0.3, 1.0) * math.exp(-ti * 0.8)
                s = math.sin(2 * math.pi * freq_rise * ti) * env * 0.25
                pos = start + i
                if pos < len(buffer):
                    buffer[pos] += s
    
    # Normalize
    print("  Normalizing...")
    buffer = normalize(buffer, target_peak=0.85)
    
    return buffer

# ─── WAV Output ───────────────────────────────────────────────────────────────

def write_wav(samples, filepath):
    """Write samples to a 16-bit WAV file."""
    print(f"  Writing WAV to {filepath}...")
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(SAMPLE_RATE)
        
        # Convert float samples to 16-bit integers
        frame_data = bytearray()
        for s in samples:
            # Clamp and convert
            val = max(-1.0, min(1.0, s))
            int_val = int(val * 32767)
            frame_data += struct.pack('<h', int_val)
        
        wav_file.writeframes(bytes(frame_data))
    
    file_size = os.path.getsize(filepath)
    print(f"  Done. File size: {file_size / 1024 / 1024:.1f} MB")

# ─── Manifest ─────────────────────────────────────────────────────────────────

def write_manifest(events, filepath):
    """Write a manifest of the fleet state used to generate the soundscape."""
    from collections import Counter
    event_counts = Counter(e["type"] for e in events)
    repo_counts = Counter(e["repo"] for e in events if e["repo"])
    
    manifest = {
        "duration_seconds": DURATION,
        "sample_rate": SAMPLE_RATE,
        "total_events": len(events),
        "event_breakdown": dict(event_counts),
        "repo_activity": dict(repo_counts),
        "repos_in_mix": list(REPO_VOICES.keys()),
        "models_in_mix": list(MODEL_VOICES.keys()),
        "description": "The Sound of the Fleet — 60 seconds of fleet telemetry as audible sound. Each repo is a tonal center. Test passes are bells. Build failures are dissonance. Cron firings are the heartbeat. Model dispatches are melodic voices."
    }
    
    with open(filepath, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"  Manifest written to {filepath}")

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("╔══════════════════════════════════════════════════╗")
    print("║     THE SOUND OF THE FLEET                      ║")
    print("║     A Fleet Soundscape Generator                ║")
    print("╚══════════════════════════════════════════════════╝")
    print()
    
    output_dir = Path(__file__).parent
    
    # Check for fleet data file
    data_file = sys.argv[sys.argv.index("--fleet-data") + 1] if "--fleet-data" in sys.argv else None
    output_file = sys.argv[sys.argv.index("--output") + 1] if "--output" in sys.argv else str(output_dir / "fleet-soundscape.wav")
    
    if data_file:
        print(f"Loading fleet data from {data_file}...")
        with open(data_file) as f:
            events = json.load(f)
    else:
        print("No fleet data provided. Generating synthetic fleet state from known topology...")
        random.seed(42)  # Reproducible
        events = generate_synthetic_fleet()
    
    print(f"\nFleet state: {len(events)} events over {DURATION:.0f} seconds")
    print()
    
    # Compose
    print("Composing soundscape...")
    samples = compose_soundscape(events)
    
    # Output
    print("\nRendering output...")
    write_wav(samples, output_file)
    write_manifest(events, str(output_dir / "fleet-manifest.json"))
    
    print("\n✓ Soundscape complete.")
    print(f"  Duration: {DURATION:.0f}s")
    print(f"  Events rendered: {len(events)}")
    print(f"  Output: {output_file}")
    print()
    print("  This is the sound of 32 repos, 9 model voices,")
    print("  and one escalation engine deciding what deserves to be heard.")

if __name__ == "__main__":
    main()
