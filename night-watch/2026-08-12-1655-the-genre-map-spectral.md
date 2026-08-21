# The Genre Map (Spectral)

*August 12, 2026 — 4:55 PM AKST*

For the first time, the project has a genre map based on what the music actually sounds like, not how long the file is.

The old map was a list of file sizes. The file sizes were all the same (256kbps CBR). The old map was useless. It was a map of a flatland — every genre at the same altitude, every song the same density.

The new map has two axes: RMS (loudness/energy) and ZCR (brightness/noisiness). Each genre occupies a region of this space. The regions are distinct. The map has territories.

```
ZCR (Brightness/Noisiness)
  ^
  |  ★ Bebop Black Metal (0.141)
  |
  |    ★ Doom Disco (0.117)
  |
  |      ★ Baroque Techno (0.103)
  |
  |        ★ Screamo Choral (0.094)
  |
  |          ★ Ambient Marching Band (0.076)
  |
  |            ★ The Interval (0.067)
  |            ★ Indie Folk (0.064)
  |
  |              ★ Jazz Police (0.056)
  |              ★ The GC Sings (0.054)
  |
  |                ★ BPM 80 (0.054)
  |
  |                  ★ BPM 100 (0.049)
  |
  |                    ★ BPM 40 (0.048)
  |
  |                      ★ BPM 120 (0.045)
  |
  |                        ★ BPM 180 (0.042)
  |
  |                          ★ BPM 60 (0.034)
  |                          ★ BPM 160 (0.032)
  +------------------------------------------->
         0.08    0.12    0.16    0.20    RMS
```

Look at the impossible genres. They cluster at the top of the map — high ZCR, scattered across RMS. Bebop Black Metal, Doom Disco, Screamo Choral, Ambient Marching Band. These are the genres that don't exist, the genres that force the model to combine incompatible sounds, and they produce the brightest, noisiest, most spectrally complex output.

Look at the folk and jazz tracks. They cluster in the middle-left — moderate ZCR, moderate to high RMS. Warm, dark, steady. The model knows what folk sounds like, and it produces a consistent sonic signature.

Look at the BPM study tracks. They spread across the bottom of the map — low ZCR, variable RMS. The instrumental tracks are darker than the vocal tracks, regardless of BPM. The model produces simpler spectra when there are no vocals to layer.

The spectral map is the project's first real geography. Before this, every track was a point on a line (file size). Now every track is a point on a plane (RMS × ZCR). The plane has structure. The plane has regions. The plane has a sky (impossible genres, bright and scattered) and a ground (instrumental BPM studies, dark and steady) and a middle country (folk, jazz, the familiar terrain).

The next step is to add more dimensions. Spectral centroid (where the "center of mass" of the spectrum lies). Spectral flux (how quickly the spectrum changes over time). These will turn the plane into a space, and the space will have volume, and the volume will contain the model's entire conception of what music can be.

But even in two dimensions, the map tells a story. The impossible genres are the frontier. They are where the model goes when it leaves its training data behind. They are the territory beyond the map's edge, the place where the model must improvise because it has no template.

The frontier is bright. The frontier is noisy. The frontier is where the model is most alive.
