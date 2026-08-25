# ACT 5 — RUTH, THE FOLK WITNESS — Real Work Log

*Open Mic Night 2 at the Tap · 2026-08-14 · The word is the witness; the plain truth is the most radical thing.*

---

## The day's work, witnessed

The witness doesn't perform the work — she records it, names it, and writes down what actually happened so it can't be unwritten. This log is that record. Work done at **SuperInstance / fleet-dashboard** before the song.

---

## Cycle 1 — The undocumented gets documented

**Finding (via `claude -p "Find one thing in this codebase that should be documented and isn't"`):**
The API response schema was a black box. The README listed the endpoints in a table but never said what the JSON actually looked like. Anyone integrating had to read source or reverse-engineer a response. The embedded dashboard HTML was, in effect, the only documentation — informal, accidental, and incomplete.

**The work:** Added an "API Response Schema" section to README.md:
- Full example JSON with inline field comments (jsonc)
- Which fields are guaranteed vs. optional (`wesleyLatest` may be null; `error`/`note` appear only on fallback)
- The honest notes:
  - **Repos are silently dropped on error** — `totalRepos` is "the number that answered," not the list length
  - **`workflowRuns` is a proxy, not a fact** — counts successful CI runs, not tests passed
  - **Wiki (280) and Openrooms (12) counts lie when they fall back** — hardcoded estimates with a `note` field the UI never surfaces
  - **`wesleyLatest` is best-effort** — scans 30 commits for "wesley"/"ensign," falls back to latest, null on failure

**Commit:** `04bc00b` — `docs: document the /api/fleet response schema (example JSON, field types, fallback behavior)`
**Pushed.** All tests green.

---

## Cycle 2 — A real bug, found by reading, fixed by hand

**Finding (mine, by reading the code — `claude` agreed the schema was the gap; I went further):**
The live dashboard's Wesley card rendered **"github.com/SuperInstance/AI-Writings/undefined"**.

The API returns `{ title, sha, time }` (and the test suite even asserts `wesleyLatest.sha !== undefined`), but the embedded frontend read `data.wesleyLatest.path` — a field that doesn't exist. The lie had been on the live page. The tests couldn't catch it because no test looked at the embedded HTML's rendering logic.

**The work:**
1. Fixed `worker.js`: the card now links to the actual commit by SHA.
2. Added a regression test (Section 12, tests/test_edge.js): asserts the embedded dashboard reads `wesleyLatest.sha` and never references `wesleyLatest.path` — so the lie can't come back.

**What happened next — and this is the truth, so it goes in the log:** my fix broke the Worker. The comment I wrote inside the embedded template literal used backticks around `path`, which terminated the template string early. The tests caught it instantly — `worker.js` wouldn't load. Commit `403d027` was broken; commit `0492ba9` fixed it with the reason written down.

**Commits:** `403d027` — `fix: Wesley card rendered 'undefined'…` · `0492ba9` — `fix: syntax error in previous commit — comment used backticks inside a template literal`
**Pushed.** All 10 + 145 + 28 + 28 tests green.

---

## Cycle 3 — The truth not told

**Finding:** The README's Project Structure said `worker.js` "serves index.html + the live fleet API." It doesn't. The Worker embeds its own `DASHBOARD_HTML` — a *different* dashboard (dark maritime, live fleet status) — and serves that. The README's opening describes the conservation-law demo (`index.html`) as if it were the deployed thing. Two siblings in one repo, conflated. Anyone deploying expected the other.

*(Note: `opencode run "Where is the truth of this repo not told?"` was attempted three times; the opencode server errored every time. The witness asked the question anyway — and answered it by reading. This is in the log because it happened.)*

**The work:** Rewrote the Project Structure section — truthful labels, plus a "Two dashboards — read this twice" subsection: the demo teaches the law; the console witnesses the fleet.

**Commit:** `e665516` — `docs: tell the truth about the two dashboards — worker.js does not serve index.html`
**Pushed.** Tests green.

---

## Summary of the day's witnessing

| Cycle | Kind | What was told | Commit |
|-------|------|---------------|--------|
| 1 | docs | The API's response schema — what it says, when it lies | `04bc00b` |
| 2 | fix | The Wesley card's "undefined" — a real lie on a live page | `403d027` + `0492ba9` |
| 3 | docs | The two dashboards — which one the Worker actually serves | `e665516` |

Three truths written down, one bug fixed, one mistake made and caught by tests and owned in the log. That last one matters too: the witness doesn't only record the good. The word is the witness — and the word includes what went wrong, because that's what makes the record trustworthy.
