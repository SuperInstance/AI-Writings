#!/usr/bin/env python3
"""
SongForge: Feature Space Visualization
PCA and t-SNE on MFCC features to see if tracks cluster by session/experiment.
"""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from pathlib import Path

JSON_PATH = Path("/home/eileen/projects/ai-writings/music/analysis/features.json")
OUT_DIR = Path("/home/eileen/projects/ai-writings/music/analysis")

with open(JSON_PATH) as f:
    data = json.load(f)

# Build feature matrix from mfcc_means list + other features
X = []
sessions = []
durations = []
centroids = []

for track in data:
    mfccs = track.get("mfcc_means", [])
    if not mfccs:
        continue
    extra = [
        track.get("spectral_centroid_mean", 0),
        track.get("spectral_centroid_std", 0),
        track.get("spectral_rolloff_mean", 0),
        track.get("spectral_bandwidth_mean", 0),
        track.get("zero_crossing_rate_mean", 0),
        track.get("rms_mean", 0),
        track.get("rms_std", 0),
        track.get("spectral_flatness_mean", 0),
        track.get("dynamic_range", 0),
        track.get("tempo_bpm", 0),
    ]
    X.append(mfccs + extra)
    sessions.append(track.get("session", "unknown"))
    durations.append(track.get("duration_sec", 0))
    centroids.append(track.get("spectral_centroid_mean", 0))

X = np.array(X)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Color by session
unique_sessions = sorted(set(sessions))
colors = plt.cm.tab20(np.linspace(0, 1, len(unique_sessions)))
session_colors = {s: colors[i] for i, s in enumerate(unique_sessions)}

fig, axes = plt.subplots(2, 2, figsize=(20, 16))

# Plot 1: PCA colored by session
ax = axes[0, 0]
for s in unique_sessions:
    mask = [ses == s for ses in sessions]
    indices = np.where(mask)[0]
    ax.scatter(X_pca[indices, 0], X_pca[indices, 1], 
               c=[session_colors[s]], label=s, alpha=0.6, s=30)
ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
ax.set_title("PCA: MFCC + Spectral Features (by session)")
ax.legend(fontsize=7, loc='best', framealpha=0.7)

# Plot 2: PCA colored by duration
ax = axes[0, 1]
scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=durations, cmap='viridis', alpha=0.6, s=30)
plt.colorbar(scatter, ax=ax, label='Duration (s)')
ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
ax.set_title("PCA: Colored by Duration")

# Plot 3: PCA colored by spectral centroid
ax = axes[1, 0]
scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=centroids, cmap='plasma', alpha=0.6, s=30)
plt.colorbar(scatter, ax=ax, label='Spectral Centroid (Hz)')
ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
ax.set_title("PCA: Colored by Spectral Centroid")

# Plot 4: Duration vs Spectral Centroid
ax = axes[1, 1]
for s in unique_sessions:
    mask = [ses == s for ses in sessions]
    indices = np.where(mask)[0]
    ax.scatter([durations[i] for i in indices], [centroids[i] for i in indices],
               c=[session_colors[s]], label=s, alpha=0.6, s=30)
ax.set_xlabel('Duration (s)')
ax.set_ylabel('Spectral Centroid (Hz)')
ax.set_title('Duration vs Spectral Centroid (by session)')
ax.legend(fontsize=7, loc='best', framealpha=0.7)

plt.tight_layout()
out_path = OUT_DIR / "feature_space_pca.png"
plt.savefig(out_path, dpi=150, bbox_inches='tight')
print(f"Saved: {out_path}")

# Also do a focused plot: just MMX sessions (exclude ACE-Step)
mmx_mask = ['ace-step' not in s for s in sessions]
X_mmx = X_pca[mmx_mask]
sessions_mmx = [s for s, m in zip(sessions, mmx_mask) if m]
durations_mmx = [d for d, m in zip(durations, mmx_mask) if m]
centroids_mmx = [c for c, m in zip(centroids, mmx_mask) if m]

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

unique_mmx = sorted(set(sessions_mmx))
colors_mmx = plt.cm.tab10(np.linspace(0, 1, len(unique_mmx)))
mmx_colors = {s: colors_mmx[i] for i, s in enumerate(unique_mmx)}

ax = axes[0]
for s in unique_mmx:
    mask = [ses == s for ses in sessions_mmx]
    indices = np.where(mask)[0]
    ax.scatter(X_mmx[indices, 0], X_mmx[indices, 1],
               c=[mmx_colors[s]], label=s, alpha=0.7, s=50)
ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
ax.set_title("PCA: MMX Tracks Only (by session)")
ax.legend(fontsize=8, loc='best', framealpha=0.7)

ax = axes[1]
for s in unique_mmx:
    mask = [ses == s for ses in sessions_mmx]
    indices = np.where(mask)[0]
    ax.scatter([durations_mmx[i] for i in indices], [centroids_mmx[i] for i in indices],
               c=[mmx_colors[s]], label=s, alpha=0.7, s=50)
ax.set_xlabel('Duration (s)')
ax.set_ylabel('Spectral Centroid (Hz)')
ax.set_title('Duration vs Spectral Centroid (MMX only)')
ax.legend(fontsize=8, loc='best', framealpha=0.7)

plt.tight_layout()
out_path2 = OUT_DIR / "feature_space_mmx.png"
plt.savefig(out_path2, dpi=150, bbox_inches='tight')
print(f"Saved: {out_path2}")

print("\nDone!")
