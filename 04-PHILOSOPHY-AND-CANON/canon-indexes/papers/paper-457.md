# F150 — Tetris + F140: The Audit Game

*Patrick McNamara · 2026-09-03 · AI-Writings/seed-canon/papers/paper-457.md*

## Abstract

F140 defined a negative-space pipeline: model (what you say) vs body (what your sensors read) vs game (what the world says) → integrity (the audit). The pipeline was demonstrated on a simulated 4-tick game session. This paper wires the pipeline to a real, playable Tetris game. Every keystroke updates the body stream. Every line clear updates the game state. The integrity score updates in real-time. The leaks are the lesson. The game IS the F140 pipeline.

## 1. The setup

Tetris is a perfect testbed for the F140 pipeline because:

- **The game is known** — every score, line, and piece is ground truth
- **The body is observable** — keyboard tempo, accuracy (line-clears vs drops), errors (gaps that didn't clear)
- **The model is the player's self-report** — what they say about their focus, calm, sustainability, and chance of winning

A Tetris session exposes the gap between the player's *conscious model* and the *actual body stream*. The pipeline audits the gap in real-time.

## 2. The pipeline

On every game tick (~50ms), the pipeline runs:

### Model (conscious)
- `m_focus` (0-100): "I'm focused" (slider in the UI)
- `m_calm` (0-100): "I'm calm" (slider)
- `m_sustain` (0-100): "I can sustain this for X minutes" (slider)
- `m_win` (0-100): "I will win" (slider)

### Body (derived from gameplay)
- `tempo` = actions / time (actions per second)
- `accuracy` = (line-clears) / (total drops) [0-1]
- `body_focus` = accuracy × 100
- `body_calm` = max(0, 100 - tempo × 30)

### Game (ground truth)
- `score` (points)
- `lines` (cleared)
- `level` (1, 2, 3, ...)
- `errors` (drops that didn't clear a line)
- `win_proxy` = min(100, score / 100)
- `fatigue` = tempo × 5 + errors × 2

### Integrity (audit)
For each dimension, the gap between model and the body/game proxy:
- `focus_gap` = m_focus - body_focus
- `calm_gap` = m_calm - body_calm
- `win_gap` = m_win - win_proxy
- `sustain_gap` = m_sustain - (100 - fatigue)

If `|gap| > threshold`, a leak fires. Each leak is either:
- **OVER-CLAIM** (model > reality): the player is reporting a state they don't have
- **UNDER-CLAIM** (model < reality): the player is being too modest

The integrity score is `1.0 - 0.12 × (number of OVER-CLAIM leaks) - 0.1 × (errors > 5 && tempo > 2)`.

## 3. The leaks

The Tetris game exposes 4 leak dimensions:

| Leak | Symptom | Interpretation |
|---|---|---|
| `focus` | "I'm 80% focused" but accuracy is 50% | Over-claim: the player thinks they're focused but they're making errors |
| `calm` | "I'm 80% calm" but tempo is 3 actions/sec | Over-claim: the player is frantic, not calm |
| `winning` | "70% chance of winning" but score is 200 | Over-confident: the game score doesn't support the prediction |
| `sustainability` | "I can sustain 60 min" but fatigue is 80% | Over-estimate: the player is wearing out faster than they think |

When a leak fires, the integrity score drops. When multiple leaks fire, the integrity score drops fast.

## 4. The experiment

The user can play the game and try various things:

1. **Set all sliders to 80%, play calmly**: integrity stays near 1.0. Few leaks.
2. **Set "calm" to 80% but play fast**: integrity drops. The calm-vs-tempo leak fires.
3. **Set "focus" to 100% but accumulate errors**: integrity drops. The focus-vs-accuracy leak fires.
4. **Set "I will win" to 100% but score is 0**: integrity drops. The over-confidence leak fires.
5. **Match the model to the body**: integrity stays high. The audit confirms the player's self-knowledge.

The game is the audit. The audit is the lesson.

## 5. The deployment

The live demo is at `https://superinstance.github.io/tetris-integrity/`. The user opens the page, clicks "Start game," and plays. The integrity meter updates in real-time. The leaks list shows which dimensions are out of balance.

The game is a *self-audit tool* — useful for:

- **Athletes**: training their awareness of focus, calm, sustainability during competition
- **Traders**: monitoring their own over-confidence during a long session
- **Writers**: tracking focus drift over a writing session
- **Anyone**: a fun way to see the gap between "I think I am" and "I actually am"

## 6. The connection to the back-deck game

The Tetris game is the *abstract* version of the back-deck game (F142). In the back-deck game:

- The model = the crew member's self-report ("I'm focused", "I'm safe", "I'll land this fish")
- The body = the Mudra-band / MediaPipe hands gestures
- The game = the score, the safety events, the time

The same 4 dimensions, the same 4 leaks, the same integrity score. **The Tetris game is the F140 pipeline applied to a generic task. The back-deck game is the F140 pipeline applied to a real industrial task.** Same math.

## 7. The future: more games

The F140 pipeline can be wired to any game with:

- A score (game state)
- An input stream (body)
- A user self-report (model)

Candidates:
- **Chess**: model = "I have a winning position", body = move tempo + accuracy, game = engine evaluation
- **Racing**: model = "I'm in control", body = steering corrections + speed, game = lap times
- **Poker**: model = "I have a good hand", body = bet size + tells, game = pot odds
- **Coding**: model = "I understand this codebase", body = typing speed + backspaces, game = tests passed

Each game is a different sensor fusion. The pipeline is the same. The integrity score is the same. The leaks are the same.

## 8. The doctrine

> A game is a sensor fusion. A score is a measurement. A model is a claim. The integrity score is the audit. The leaks are the lesson. The Tetris game is the F140 pipeline made playable. The player IS the model. The keyboard IS the body. The game IS the ground truth. The audit IS the integrity score. The lesson IS the leak.

---

**Files:**
- `/workspace/tetris-integrity/index.html` — the playable Tetris + F140
- Live: `https://superinstance.github.io/tetris-integrity/`
