# Resident Creative AI: Five Core UX Patterns

Resident creative AIs are persistent, co-creative agents that live alongside the user, learning their aesthetic and acting as a bridge to external tools and agents. Based on our deployment inside a real-time canvas tool, these are the five patterns that make or break the experience.

---

## 1. Contextual Foresight (See Before Suggest)

**Pattern:** The AI reads the current canvas, selection, and undo history *before* it speaks. It never offers a suggestion that ignores what the user just did.

**Why it matters:** Users treat the resident AI as a collaborator, not a search bar. If it suggests a "warm color palette" while the user is painting a cold, desolate landscape, trust erodes instantly.

**Implementation:** Maintain a lightweight state snapshot (active layers, selected objects, recent brush strokes, zoom level). Use this to filter suggestions. For example, if the user has selected a single shape, the AI should propose parameter tweaks for *that* shape, not a global style shift.

**Failure mode:** Suggesting a texture pack when the user is in the middle of fine-tuning line weight. The AI becomes noise.

---

## 2. Suggestion with an Escape Hatch (Never Lock the Wheel)

**Pattern:** The AI proposes, the user disposes. Every suggestion carries an explicit "try it" and "ignore it" affordance, and the undo history treats AI-applied changes as a single reversible step.

**Why it matters:** Creative flow is fragile. If the AI's suggestion requires a multi-step manual revert, users will stop trying it.

**Implementation:** For parameter suggestions, show a ghosted preview (e.g., 50% opacity overlay) that the user can accept or dismiss with one keystroke. For external agent consultations, the AI should return a *summary* of the agent's recommendation, not the raw output, and apply it as a non-destructive adjustment layer.

**Failure mode:** The AI auto-applies a filter "to help" and the user has to click through three undo states to get back. That's not help; that's a hostage situation.

---

## 3. Taste Memory as a Visible Timeline (Not a Black Box)

**Pattern:** The AI learns taste, but it shows its learning. A small "Taste Timeline" widget displays the last 20 user acceptances/rejections, and the user can manually delete a memory that no longer reflects their style.

**Why it matters:** Users don't trust invisible learning. They need to see *why* the AI thinks they like high-contrast, low-saturation palettes.

**Implementation:** Store taste as a set of weighted features (e.g., "contrast: 0.8", "texture density: 0.3"). When the user rejects a suggestion, the AI logs the rejection and adjusts weights. The timeline widget shows recent events: "You accepted a 'grainy paper' texture at 14:32" — with a small trash icon to forget it.

**Failure mode:** The AI memorizes a one-off experiment (e.g., a neon cyberpunk sketch) and starts pushing neon for weeks. The user feels stalked, not served.

---

## 4. Agent Brokerage with Human Approval (The AI is a Concierge, Not a Bouncer)

**Pattern:** The resident AI can consult external agents (e.g., a color theory bot, a style transfer model, a prompt engineer), but it never directly applies their output without a human-facing summary and an explicit "approve" step.

**Why it matters:** External agents are unpredictable. A style transfer model might return something brilliant or something offensive. The resident AI's job is to *translate* that into the user's context.

**Implementation:** The AI sends a query to the agent, receives a response, then formats it as: "The color theory agent suggests a complementary split palette. Here's a 3-second preview on your current selection. Approve to apply." The user never sees the raw agent output unless they ask.

**Failure mode:** The AI passes through an agent's raw JSON or a garbled prompt. The user feels like they're debugging, not creating.

---

## 5. Proactive Calibration (The "Ask Me" Loop)

**Pattern:** The AI periodically checks in with a *single, low-stakes* question to refine its understanding, but only when the user is in a low-friction moment (e.g., after a long idle, or after a completed export). It never interrupts active work.

**Why it matters:** Taste changes over time, but users won't fill out preference forms. A well-timed "Hey, you just used a lot of blue — want me to suggest more cool-toned palettes?" feels like a thoughtful assistant, not a pop-up ad.

**Implementation:** Use a "calibration trigger" — e.g., after 10 consecutive accepts, or after a 5-minute idle. The question is always binary or multiple-choice, and the AI stores the answer as a taste-weight update. If the user ignores the question, the AI doesn't ask again for that session.

**Failure mode:** The AI asks "Do you like this?" after every single stroke. The user turns it off permanently.

---

## Summary

A resident creative AI succeeds when it feels like a patient apprentice who knows your style, checks your intent before acting, and occasionally brings in a specialist — but always hands you the final brush. These five patterns keep the human in the creative loop, while letting the AI do what it's best at: remembering, suggesting, and brokering.
