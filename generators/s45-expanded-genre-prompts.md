# Session 45 — 9 New Genre Prompts for MMX (Llama 3.2 Refined)
## Combined with S44's 8 original prompts = 17-genre batch for Aug 17

## Prompt 9: Future Ambient Blues
```
Slow blues at 68 BPM in A minor. Electric guitar with warm overdrive playing 
pentatonic licks over synth pad drones. Crystal chimes accenting phrase endings. 
Deep emotive male vocal, bluesy phrasing with long sustained notes. Subtle 
delay and reverb creating atmospheric depth. Reference: Gary Clark Jr meets 
Brian Eno's Music for Airports.
```

## Prompt 10: Aquatic Ambiance
```
Ambient at 72 BPM in D minor. Waterphone providing eerie metallic tones, 
theremin sweeping in long arcs, alto flute carrying melody. Breathy female 
vocal mimicking water droplet rhythms. Ocean-like white noise swell in 
background. Reference: Max Richter's Sleep meets coastal field recordings.
```

## Prompt 11: Neo-Jazz Funk
```
Neo-jazz funk at 98 BPM in E-flat major. Fender Rhodes with tremolo, 
Hammond B3 organ with Leslie speaker, tenor saxophone with breathy tone. 
Syncopated drum pattern with ghost notes on snare. Female vocal with 
Erykah Badu-style phrasing, conversational and warm. Walking bass line. 
Reference: Erykah Badu's Mama's Gun meets Robert Glasper.
```

## Prompt 12: Synthwave Groove
```
Synthwave at 128 BPM in G minor. Roland TR-808 drum pattern, Moog 
Sub Phatty bassline with filter sweeps, Juno-106 synth pads. Digitized 
vocals with vocoder processing. Arpeggiated synth melody in upper 
register. Reference: Carpenter Brut meets Kavinsky's Nightcall.
```

## Prompt 13: Solar Pop Groove
```
Pop at 105 BPM in B major. Guitar synthesizer with bright envelope 
filter, nature percussion (thunder rumble, rain-on-leaf shaker pattern). 
Ethereal female vocal in high register, soaring and warm. Lush dreamy 
textures with delay throws on vocals. Reference: Beach House meets 
Bjork's Biophilia.
```

## Prompt 14: Neo-Classical Fusion Beats
```
Neo-classical at 135 BPM in C minor. Grand piano with close miking, 
viola da gamba with extended vibrato techniques. Electronic drum machine 
with metallic bell timbres. Soft-spoken male vocal using baroque phrasing 
and archaic vocabulary. String quartet building to crescendo. 
Reference: Olafur Arnalds meets Clerk Petersen.
```

## Prompt 15: Vaporwave Symphonic Dreamscape
```
Symphonic vaporwave at 82 BPM in F# minor. String quartet with analog 
distortion pedals, vintage vinyl crackle throughout. Electric bass 
emulating ocean wave patterns. Female lead in warm baritone with male 
falsetto harmonies. Eerie, nostalgic atmosphere with reversed string 
samples. Reference: William Basinski's Disintegration Loops meets 
Slowdive's Souvlaki.
```

## Prompt 16: Harmonious Fusion
```
Warm fusion at 100 BPM in D major. Synthesizer pads, electric guitar 
with clean tone, acoustic piano, lush string section. Smooth falsetto 
male vocal with soulful belts in chorus. Syncopated but gentle drum 
pattern. Bass guitar melodic and conversational. Reference: Thundercat 
meets Steely Dan's Aja.
```

## Prompt 17: Techno-Organic
```
Techno-organic at 144 BPM in E minor. Hard-hitting drum machine with 
TR-909 kick, distorted electric guitar stabs, synthetic and organic 
percussion layered. Aggressive chopped rap vocal samples, gritty and 
compressed. Sub-bass sine wave on downbeats. Industrial textures. 
Reference: Flume meets Death Grips meets Gesaffelstein.
```

## Batch Execution Plan (Aug 17)

| # | Genre | Distance | Tempo | Key | Vocal |
|---|-------|----------|-------|-----|-------|
| 1 | Neo-soul | NEAR | 82 | Eb | Female alto |
| 2 | Welsh choir post-rock | MOD | 68 | Bm | Male choir |
| 3 | Ghettotech | FAR | 138 | Gm | MC style |
| 4 | Bulgarian wedding | FAR | 140 | D modal | Diaphonic |
| 5 | Koto ambient | V.FAR | 60 | Dm | Japanese-contour |
| 6 | Black metal ambient | V.FAR | 90 | Em | Screamed/clean |
| 7 | Desert blues | MOD | 95 | Am | Tamashek-style |
| 8 | Baltimore club | FAR | 130 | F | Percussive female |
| 9 | Future Ambient Blues | FAR | 68 | Am | Blues male |
| 10 | Aquatic Ambiance | V.FAR | 72 | Dm | Breathy female |
| 11 | Neo-Jazz Funk | NEAR | 98 | Eb | Neo-soul female |
| 12 | Synthwave Groove | MOD | 128 | Gm | Vocoder |
| 13 | Solar Pop Groove | V.FAR | 105 | B | Ethereal female |
| 14 | Neo-Classical Fusion | V.FAR | 135 | Cm | Baroque male |
| 15 | Vaporwave Symphonic | FAR | 82 | F#m | Warm baritone F |
| 16 | Harmonious Fusion | NEAR | 100 | D | Falsetto male |
| 17 | Techno-Organic | FAR | 144 | Em | Aggressive rap |

### Quota Considerations
- MMX music generation: ~1 track per quota call
- Weekly quota resets Aug 17
- Previous batches: max 8-12 tracks per session
- 17 tracks may exceed a single session's quota — prioritize by tier:
  - **Priority 1 (must run):** #1, #7, #9, #10, #11, #16
  - **Priority 2 (should run):** #2, #5, #6, #15
  - **Priority 3 (nice to have):** #3, #4, #8, #12, #13, #14, #17
