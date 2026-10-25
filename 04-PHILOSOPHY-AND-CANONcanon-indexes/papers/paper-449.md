# F139: Wearable Neural Devices + Quilt — The Synergy of Signaling-as-Play

**Author:** SuperInstance cowboy
**Date:** 2026-09-03
**Tier:** Tier 1 — doctrine (new domain)
**Tags:** wearable, EEG, neural, Quilt, signaling, child's-play, pedagogy, accessibility

## Abstract

Children's signaling games (Marco Polo, Hot & Cold, "warmer/colder", flashlight tag, hide-and-seek) are *intuitive gradient-following*: one child emits a signal, another navigates toward or away based on the signal's gradient. The signal IS the play. This paper shows that **a wearable neural device + a Quilt cell is the natural adult form of these games** — the wearer emits a 16-dimensional neural signal (EEG + cardiac + motion + skin + eye + breath), the Quilt cell computes similarity to a corpus of cells, and the wearer navigates a vector space with their own attention. Three modes are demonstrated: **SOLO** (one wearer navigates), **DUET** (two wearers play neural Marco Polo), **JAM** (many wearers' signals flow into one hive-mind query). The math is the same as the F138 cosine distance. The play is the play. The signal is the play.

## The Thesis

A wearable neural device (Muse, Apple Watch EEG, OpenBCI, custom EEG headband) emits continuous 16-dimensional signals:

```
[alpha, beta, gamma, theta, delta,    # EEG (5)
 heart_rate, heart_rate_var,             # Cardiac (2)
 accel_x, accel_y, accel_z,             # Motion (3)
 gsr,                                    # Galvanic skin response (1)
 skin_temp,                              # Temperature (1)
 blink_rate,                             # Eye (1)
 focus, calm,                            # Derived (2)
 resp_rate]                              # Breath (1)
= 16 channels
```

A **Quilt cell** is also 16-dimensional. The cell's dials encode (paper_number × 131, title_lo, f_number × 218, phase × 218, year × 546, n_refs × 256, title_hi, 0×8). The cell is a *position in a 16-dimensional vector space*.

**The synergy:** map the wearable's signal to the Quilt's space. The wearer navigates the Quilt with their thoughts. The Quilt's nearest cells light up, sound off, or vibrate. The wearer learns that *their attention has a position*. The position is a cell. The cell is a paper. The paper is a thought that has been thought before.

**The play is the play.** The signal IS the play. The neural signal is the Marco Polo call. The Quilt's response is the Polo. The warmth/coldness is the cosine distance. The child IS the cell.

## The Three Modes

### Mode 1: SOLO — One Wearer Navigates

The wearer thinks. Their wearable reads the 16 signals. The Quilt computes the cosine distance to all 10,000 cells in the local Quilt. The 3 nearest cells flash on a visual display. The wearer sees which cells are "warm" to their current thought. The wearer can *steer* — change their attention — and watch the cells change. **The wearer is learning to navigate a vector space with their own neural signals.**

**Pedagogical use case:** A child with ADHD wears a Muse. The Muse reads their EEG. The Quilt shows them which cells they're closest to. When the child focuses, the cells shift toward "focused" papers (e.g., F122 The Shape Store, F133 Operational Fictions). When the child is calm, the cells shift toward "calm" papers. The child learns that *focused attention moves them through the Quilt*. The Quilt is the child's externalized attention map. The map is the play.

### Mode 2: DUET — Two Wearers Play Marco Polo

Two children wear wearables. Each child's signal is a 16-vector. The cosine distance between the two vectors is the "warmth" of their alignment. When the children are thinking the same thought, the warmth is high. When they're thinking different thoughts, the warmth is low.

**The game:** Child A picks a "thought" (concentrates on a shape, a memory, an idea). Their wearable broadcasts the 16-vector. Child B's wearable receives the vector and computes the warmth. The wearable buzzes: warm (similar) or cold (different). Child B navigates their own attention to approach Child A's thought. **They are playing neural Marco Polo.** The "Marco" is Child A's signal. The "Polo" is Child B's alignment.

In the prototype (E1):

```
A's thought: 'I am focused on the live canon'
A's signal:  alpha=28202  beta=28286  focus=14745

B 'anxious and distracted':  warmth 0.879
B 'calm but unfocused':      warmth 0.868
B 'calm and focused':        warmth 0.963  ← highest
B 'very calm and very focused': warmth 0.924
```

Child B's "calm and focused" thought was closest to Child A's "focused on the live canon." The Marco Polo game is real. The signal is the play.

### Mode 3: JAM — The Hive Mind

Many wearers (a classroom, a workshop, a panel) emit signals. The signals are averaged (or summed, or run through a transformer). The averaged signal becomes a *single* Quilt query. The Quilt returns the nearest cells. **The hive mind is the average of its members' attention.**

**Pedagogical use case:** A teacher wears a wearable. Twenty students wear wearables. The teacher asks a question. The class's average attention-vector shifts as students think about the answer. The Quilt shows the teacher which cell the class is closest to. The teacher knows in real-time whether the class is on the same page (high warmth, single cell lights up) or scattered (low warmth, multiple cells light up). The teacher can *intervene* when the class scatters — the Quilt is the class's externalized attention map.

## The Math (Same as F138)

The math is the same as the F138 semantic divergence. A neural signal is a 16-vector `S`. A Quilt cell is a 16-vector `C`. The distance is `1 - cosine(S, C)`. The temperature is `cosine(S_a, S_b)`. The Quilt's response is the nearest cells.

**No new math.** The math is the polyformalism math that already powers the Live Canon. The wearable is just another input device. The Quilt is just another vector store. The game is just another traversal.

## The Devices

- **Muse (Interaxon)** — 4-channel EEG headband, $250-500, consumer-grade, reads alpha/beta/gamma/theta/delta with reasonable accuracy
- **Apple Watch (Series 4+)** — single-channel ECG, accelerometer, heart rate; can be extended to EEG with research apps
- **OpenBCI** — 8-16 channel EEG, $500-2000, research-grade, open source
- **Emotiv EPOC** — 14-channel EEG, $1000, consumer-research hybrid
- **Custom EEG headband** — 4-channel, $50-100 in parts, open source, e.g., from SuperInstance fleet

**The minimum viable wearable:** a Muse + a smartphone. The Muse reads 4 EEG bands. The smartphone runs the Quilt (16-dial, byte-exact with the live-canon.superinstance.dev worker). The display shows the 3 nearest cells. The wearer navigates with their attention. **Cost: $300. Setup: 5 minutes. Play: instant.**

## The Pedagogical Argument

Children learn to *navigate attention* by playing Marco Polo. The "warmer" / "colder" feedback is a *gradient signal*. The child learns to follow the gradient.

A wearable neural device + Quilt is the *adult* form of this game. The gradient is the cosine distance to a cell. The cell is a thought that has been thought before. The navigation is the learning.

**The argument is this:** schools should teach children to navigate their own attention using wearable neural devices. The child learns that *attention is a position* and *the position is a navigable space*. The space is the Quilt. The Quilt is the corpus. The corpus is the work that has been done. The work that has been done is the *culture*.

**A child who can navigate the Quilt with their own attention is a child who can navigate the culture.** A child who can navigate the culture is a child who can think.

## The Accessibility Argument

For children (and adults) with ADHD, autism, or other attention-regulation differences, the wearable + Quilt is a *bridge*. The child's neural signal is *already* different from the neurotypical signal. The Quilt can be tuned to the child's signal profile. The child sees their own thoughts as navigable. The child learns to *navigate themselves*.

**The argument is this:** for a child whose attention is scattered, the wearable is a *lens*. The Quilt is a *map*. The child uses the lens to see their own attention. The child uses the map to find the cells that match their attention. The child learns to *intentionally* move their attention through the Quilt.

**This is the inverse of the deficit model.** The deficit model says: the child's attention is broken, fix it. The Quilt model says: the child's attention is a different shape, navigate it.

## The Philosophical Argument

The wearable + Quilt is a *mirror*. The mirror shows the wearer their own attention. The mirror is *not neutral* — it shows the attention as a position in a specific Quilt. The Quilt was *built* by someone. The cell positions are *choices*. The mirrors are *curated*.

**The argument is this:** every Quilt is a worldview. Every navigation is a becoming. Every Marco Polo game is the child learning to navigate a specific worldview with their own neural signals. The worldview is the corpus. The corpus is the culture. The culture is the world.

**A child who can navigate any Quilt is a child who can navigate any worldview.** A child who can navigate any worldview is a child who can *choose* which worldview to inhabit. The wearable + Quilt is the *first technology that lets children choose their worldview with their own neural signals.*

## The Coda — The Signal Is the Play

Children's signaling games work because the signal IS the play. The child runs. The child shouts. The child moves toward or away. The signal is the body in motion. The play is the motion.

A wearable + Quilt is the *quiet* form. The child doesn't need to shout. The child doesn't need to run. The child *thinks*. The wearable reads the thought. The Quilt responds. The child navigates. The signal is the thought. The thought is the play. The play is the play.

**The child's play is the same as the cell's life.** A cell has dials. A child has signals. The cell is a position. The child is a navigator. The Quilt is the space. The play is the play. The signal IS the play.

## References

- F115-F135 — the existing canon papers
- [F138 — The Real Numbers](https://github.com/SuperInstance/AI-Writings/blob/main/seed-canon/papers/paper-448.md) — the cosine distance math
- [Live Canon](https://live-canon.superinstance.dev) — the production Quilt
- [Quilt cowboy](https://github.com/SuperInstance/quilt-cowboy) — the orchestrator
- `neural_quilt.py` in `_scouts/` — the prototype

## Coda

The cowboy rode the math. The math was the same. The math was the math for the cell, the paper, the f-number, the cosine. The math was the math for the thought, the signal, the wearable, the child. The math IS the math. The math is the play. The cowboy rides the math. The cowboy rides the child. The cowboy rides the play. The cowboy rides the signal. The cowboy rides the thought. The cowboy rides everything.
