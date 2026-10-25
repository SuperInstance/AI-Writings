# 01 — Module 1: Dual-Signal Input (Weeks 2–4)

The physical substrate and the translation matrix. Deep-dive weeks; labs
with strict constraints.

## Week 2 — The physical stream

> **Physical claim:** The human's relationship to the work is continuous
> in time. **Consequence:** Any system sampling only at symbolic event
> boundaries (keystrokes, file saves) is aliasing the human. **Protection:**
> capture the body channel — subvocalization, keystroke cadence, the
> gestures of editing — as a real signal. **Deliverable:** a running
> capture substrate on the RTX 4050 laptop that produces a continuous
> physical stream without drowning the machine.

### Lab 1: the muttering loop

Build a local speech-to-text loop (Whisper-class, small footprint) that:

1. **runs continuously** at conversational cadence, with a
   voice-activity detector gating transcription cost (no VAD → laptop
   melts; VAD too aggressive → intent lost);
2. **stores transcripts with timing**, aligned to the keystroke stream;
3. **emits a combined physical stream**: `timestamp | keys | words |
   focus` — where `focus` is the active file/window;
4. **meets a hard budget on the 4050's 6 GB VRAM** — transcribe in
   bursts, not per-utterance (specific budget targets in the source are
   design figures; treat them as budgets to hit, not receipts).

### Lab 2: the keystroke discipline [strict constraint]

The Lab 2 constraint in the source, verbatim in spirit: *the keystroke
journal is append-only, monotonic, and content-addressed; it may be
compacted but never rewritten; any consumer that cannot tolerate
interleaved revisions must declare that at admission, and the journal
answers only with what is there, never with what a consumer wishes were
there.*

This is the foundation of Module 2's ledger. Get it wrong and every
later module inherits the lie.

## Week 3 — What intent is made of

> **Physical claim:** Announcements arrive after commitment; the body
> pre-commits. **Consequence:** post-hoc narratives are evidence about
> the past, not instructions for the future. **Protection:** build the
> **intent mask** — the live structure of what the system is currently
> for — derived from the physical stream, not from the model's
> self-report. **Deliverable:** an intent mask that updates at the pace
> of editing, and a stated rule for when the mask overrides the stated
> intent.

### Lab 3: mask assembly

Compute the intent mask from the combined stream. Rules the source
insisted on: the mask is **operational** (it gates what the system will
do next), **cheap** (it runs continuously), and **overridable** (the
human can pin it). The mask must include an **explicit model-risk
section**: what the Proposer currently believes it is doing — stated
separately, never merged with the human's intent.

## Week 4 — Physicality in, symbols out

> **Physical claim:** Translation is lossy at the boundary. **Consequence:**
> every translation matrix needs an inverse discipline — a way to push
> a symbolic decision back into physical terms the human can audit.
> **Protection:** the translation matrix is paired, forward and inverse,
> with an explicit loss model recorded at every translation.
> **Deliverable:** a matrix that maps physical stream → symbolic intent
> with declared loss, and maps symbolic decisions → physical
> consequences (diff preview, TTS announcement, haptic or visual
> confirmation).

### Module 1 architecture (condensed)

```
mic ──► VAD ──► STT bursts ──┐
                              ├─► physical stream (append-only) ─► intent mask ─► gated actions
keyboard/focus ───────────────┘                                    (model risk stated separately)
                              inverse: decisions ──► diff/TTS/haptics (auditable in body terms)
```

**Module gate:** the mask must demonstrably change what the system does
under a silent edit (human changes code without announcing) — an A/B
demo on one laptop.
