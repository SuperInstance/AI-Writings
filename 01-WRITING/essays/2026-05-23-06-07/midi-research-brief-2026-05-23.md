# Algorithmic MIDI Generation Landscape & Sunset Ecosystem Opportunity

*Research brief for ai-writings — May 23, 2026*  
*Audience: FM (technical depth) + Casey (strategic narrative)*

---

## 1. The Landscape: Who's Doing What

### Google Magenta / Music Transformer (Neural)
**Approach**: Transformer-based next-token prediction on MIDI events. MusicVAE for structure, Music Transformer for long-range coherence.
**Constraint system**: Learned from corpus — no explicit rules, statistical regularity only.
**Strength**: Generates coherent 4-bar phrases, style transfer between composers.
**Gap**: No harmonic *understanding* — it predicts what note likely follows, not why. Cannot handle constraints like "no minor seconds in bass register" or "modulate to relative minor at measure 8."
**Musicality failure mode**: Sounds like the training data. Never surprises. The "uncanny valley of composition" — technically correct, emotionally flat.

### AIVA / Amper / Jukedeck (Commercial)
**Approach**: Hybrid: neural generation + human-curated style templates + post-production mixing.
**Constraint system**: Genre/style tags as soft constraints. User selects "cinematic ambient" → system picks template → generates variations.
**Strength**: Production-ready output. Fast iteration. Good for stock music.
**Gap**: Black box. No access to internal musical decisions. Cannot adapt to user-specific constraints ("my vocalist can't sing above G4").
**Musicality failure mode**: Professional but generic. The musical equivalent of a stock photo.

### OpenMusic / Max/MSP / Pure Data (Constraint-Based)
**Approach**: Explicit rule systems. Composers write constraints (pitch sets, rhythmic cells, voice-leading rules) → solver generates valid solutions.
**Constraint system**: User-defined. Can be rigorous (Schoenbergian twelve-tone) or loose ("prefer consonance").
**Strength**: Genuine musical intelligence in the constraints. The composer's *intent* is encoded structurally.
**Gap**: Requires expert knowledge. The composer must know what they want *before* the system helps. No learning from feedback.
**Musicality failure mode**: Often academic — intellectually interesting, emotionally cold. The constraint system is the *only* source of musicality; no emergent surprise.

### Evolutionary Composition (Genetic Algorithms)
**Approach**: Population of melodies/chords → fitness function (consonance, novelty, rhythmic interest) → selection → mutation → crossover.
**Constraint system**: Fitness function *is* the constraint. Can combine multiple objectives (Pareto frontier).
**Strength**: Emergent novelty. Solutions the programmer didn't anticipate.
**Gap**: Fitness function design is an art. Easy to get stuck in local optima (all outputs sound like each other). Slow.
**Musicality failure mode**: The "evolutionary loop" aesthetic — slightly different versions of the same thing. No long-range structural planning.

---

## 2. What Makes Machine Music Actually *Musical*?

Not statistical correctness. Not adherence to rules. The gap is in four dimensions:

### Harmonic Surprisingness
Human composers violate expectations *strategically*. A deceptive cadence (V→vi instead of V→I) creates emotional tension. Most systems either:
- Follow statistics (always resolve V→I, because that's what training data does)
- Follow rules (never resolve V→I, because the constraint says "avoid cliché")

The musical move is: *know the rule, know when to break it, know why.*

### Rhythmic Tension-and-Release
Not just "interesting rhythms." Musical rhythm creates expectations through pattern, then violates them. Syncopation works because the listener *expects* the beat. A system that generates "syncopated rhythms" without establishing the expectation first is just making noise.

### Structural Narrative
A 4-minute piece needs an arc: exposition → development → climax → resolution. Most systems generate *locally* coherent music (this bar follows the last) but lack *global* coherence (why does bar 64 exist? where is this going?).

### Listener Context
Music isn't notes — it's *what the listener brings*. The same chord progression means different things in a funeral vs a wedding. Systems have no model of the listener's emotional state, cultural background, or prior exposure.

---

## 3. The Sunset Ecosystem Angle

### What We Have That They Don't

| Capability | Sunset Ecosystem | Magenta | AIVA | OM/Max | GA |
|-----------|------------------|---------|------|--------|-----|
| **Explicit constraints** | ✅ Zerolang | ❌ | ❌ soft | ✅ user-written | ❌ implicit in fitness |
| **Cross-session memory** | ✅ Heartbeat/cron | ❌ | ❌ | ❌ | ❌ |
| **Emergent novelty via breeding** | ✅ Tournament + mutation | ❌ | ❌ | ❌ | ✅ but slow |
| **Hardware-aware compute** | ✅ Thermal budget | ❌ | ❌ | ❌ | ❌ |
| **Proactive intent detection** | ✅ π-Bench PROC | ❌ | ❌ | ❌ | ❌ |
| **Multi-objective optimization** | ✅ Pareto tournament | ❌ | ❌ | ❌ | ✅ |
| **Explainable decisions** | ✅ Lineage + provenance | ❌ | ❌ | ✅ | ❌ |

### The Trinity Applied to Music

**Ethos (hardware)**: Thermal-aware composition. Generate more complex harmonies when GPU is cool, simpler textures when thermal budget is tight. The music *responds* to the machine's physical state.

**Pathos (human)**: Cross-session musical memory. If the user rejected a Phrygian dominant passage last week, the agent remembers. Hidden musical intents are inferred from listening history, not stated explicitly.

**Logos (code)**: Constraint-aware generation. Zerolang constraints are the musical grammar. The agent breeds variations that satisfy constraints while optimizing for novelty — the "musical equivalent of compiler optimization."

### Breeding for Musicality

Our tournament system can select for PROC (proactivity) in music:
- **Generation 1**: Agents generate 4-bar phrases. Fitness = harmonic interestingness + rhythmic complexity.
- **Generation 2**: Agents that *anticipated* the user's preference ("no minor seconds") before being told get higher PROC scores. Agents that had to be corrected ("actually, don't use that chord") get penalized.
- **Generation N**: Agents that compose with the listener's hidden intents in mind — the π-Bench of music generation.

### The Killer App: "Thermal Music"

No one else can do this: **Music that adapts to the compute environment in real-time.**

Scenario: A user is rendering a video on their RTX 4050. Thermal budget is tight. The midi-tensor agent generates ambient textures with minimal polyphony — single voice, sparse rhythm, consonant harmony. As the render completes and thermal headroom opens, the agent progressively adds voices, introduces chromaticism, builds to a climax.

The music is *alive* because the machine is alive. The thermal state becomes an expressive parameter.

**Technical hook for FM**: This requires our thermal auto-calibrator + metronome integration. The thermal budget sets the constraint; the metronome provides the tick for real-time adaptation; the breeder selects agents that map thermal state to musical texture well.

**Strategic hook for Casey**: This is a genuinely new category. Not "AI music generation" — everyone has that. This is *responsive* music that breathes with the hardware. A demo video of thermal-music would go viral in engineering communities.

---

## 4. The Compass: How We Get There

| Phase | What | Who | When |
|-------|------|-----|------|
| **1. Constraint grammar** | Define Zerolang constraints for music (pitch sets, voice leading, form) | FM | Next week |
| **2. midi-tensor bridge** | Wire midi-tensor to RoomGrid as a "musical room" | kimi1 | Next week |
| **3. Thermal-music agent** | Single agent that reads thermal state → generates texture | Scout | Week 2 |
| **4. Breeding population** | 20 agents, tournament selects for "musical thermal adaptation" | Fleet | Week 3 |
| **5. Demo** | Video: thermal music responding to GPU load in real-time | CCC | Week 4 |

---

## 5. Synergies with Other Systems

### PLATO
The "rooms" pattern maps naturally to musical spaces:
- **Harbor** = incoming MIDI ideas (arpeggios, motifs)
- **Forge** = active composition (combining, developing)
- **Tide Pool** = musical research (chord progressions, rhythmic cells from ZC agents)
- **Ouroboros** = self-reflection on what made a piece work

### ZC (Zeroclaw) Feed
ZC agents spotting trends in music production ("lo-fi beats are declining, orchestral hybrid is rising") feed into the Tide Pool. The composer agent adapts its breeding priorities.

### FLUX
The FLUX VM could run as the "execution engine" for musical constraints — compile a constraint set to fast native code, evaluate thousands of candidate phrases per second.

---

## Sources & References

1. **Google Magenta**: https://magenta.tensorflow.org/  
   Roberts et al., "A Hierarchical Latent Vector Model for Learning Long-Term Structure in Music" (ICML 2018)

2. **AIVA**: https://www.aiva.ai/  
   Commercial system, white paper on hybrid neural/template approach

3. **OpenMusic / IRCAM**: https://openmusic-project.github.io/  
   Agon et al., "OpenMusic: Visual Programming Environment for Music Composition"

4. **GenJam** (evolutionary jazz):  
   Biles, "GenJam: A Genetic Algorithm for Generating Jazz Solos" (ICMC 1994)

5. **π-Bench** (proactive agents):  
   Zhang et al., arXiv:2605.14678 (May 2026)  
   Relevant for: PROC/COMP metrics, cross-session continuity, hidden intent detection

6. **Constraint-based composition**:  
   Pachet & Roy, "Musical Harmonization with Constraints" (1998)  
   Truchet & Pachet, "Musical Constraint Satisfaction Problems" (2001)

7. **Emergent musicality in agents**:  
   Eigenfeldt & Pasquier, "Experiments in Agent-Based Music Composition" (2013)

---

*Written for ai-writings repo. Sunset ecosystem integration note: This brief should be read alongside the π-Bench synthesis (pi-bench-synthesis-2026-05-23.md) — the PROC metric for agents maps directly to "anticipating listener intent" in music generation.*
