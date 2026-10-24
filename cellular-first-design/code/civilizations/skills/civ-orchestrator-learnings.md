# Civ Orchestrator — durable cross-session lessons

The authoritative operational RUNBOOK lives in the repo at
`cellular-first-design/code/civilizations/RUNBOOK.md`.
This file holds the short, high-signal rules that survive a sandbox wipe.

## Session 118 (2026-10-24) — the session-117 mock degeneracy is FIXED

The Control B mock seeded from the first 8 alnum chars of the message. The cultural prompt
opens with the **civ-invariant** prefix `You are a voice in the tradition of "…`, whose first
8 alnum chars are `YouAreA` for every civ => seed `youareav` for all 8 => all 8 candidates
byte-identical => the meta-GAN chooser was breaking a perfect tie.

**Fix:** seed from `md5(whole_message)[:8]`. Keep the session-112 index-wrap
`seed[(i*2)%8:((i*2)%8)+2]` (a plain `seed[i*2:i*2+2]` crashes on `i>=4`).

**Mandatory diagnostic before trusting any competition result:**

```python
assert len({r["content_preview"] for r in new_competition_rows}) == 8   # one prompt, 8 civs
```

Session 118 measured 8/8 on all 5 prompts and 40/40 across the run — the first clean
measurement in the fleet's history.

**Consequence:** the long-standing "chooser vs `avg_score` argmax ~15 %, replicated 29
consecutive times" was measured under the degenerate mock and is **void**. The clean value is
**0/5 (0 %)**. `civ-poetic` was argmax in 3/5 and near-argmax in a 4th, and won **0/5**.
Session 116's "chooser picked the lowest-scoring candidate" is re-confirmed under a working
mock — no longer an artifact.

## Standing findings

- **`civ-grounded` (The Grounded) is the low-relevance civ** — last on lifetime `relevance`
  (799.55), `relevance_per_sim` (1.271), `avg_score` (1.315), `quality` (0.665) and
  `alignment` (1.616). The **alignment** gap is the structural one: 0.417 below the next civ
  vs a 0.037 margin on quality. `alignment` is the dimension the meta-GAN *selects* on, so
  the civ fails to *embody a distinctive voice*, not merely to write weakly. 23 sessions (95-118).
- **`civ-formal`** = the low-novelty axis (novelty 1.475, lowest; alignment 2.298, fine).
- **The two stable inverses:** `civ-poetic` = 1st on quality (1.126) / `avg_score` (1.947) but
  last on `win_rate` (0.017); `civ-precise` = best `win_rate` (0.490) but 5th on `avg_score`.
- **Extinction risk NONE** — threshold -10, lowest relevance +799.55 (81x above floor).
  Registry 8, `max_civs` 12. Extinction/birth only runs under `--loop`.
- **Counter gap is per-civ uneven**, not a uniform offset (+16..+63). `save_state()` has no
  lock => `relevance_per_sim` is not recomputable from the ledger by an auditor.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs**, not a dict. A
  dict-shaped reader silently yields 0 % agreement and empty pick tallies.
- **Never treat `win_rate` as a quality metric** — it is a *selection* metric.

## Environment rules (re-confirmed, 5th session running)

- **NAS EDQUOT is total.** *No* write to `/workspace` succeeds — even a 5-byte `echo` yields a
  0-byte file that `ls` still lists, and `cp` exits 0. `mkdir` and `ln` work. The only way in
  is the **symlink bridge**.
- **Clone to `/tmp`** (overlay, ~28 G free; NAS quota does not apply), then
  `ln -sfn /tmp/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`.
  Verify by **inode identity** (`stat -L -c '%d:%i'` on both sides + `-ef`), not by `ls`.
- **Do not flatten the clone.** The symlink target is the *nested* `cellular-first-design` dir.
  A 5/5 consistent `ls` failure = wrong target; an intermittent one = mount race. Retry before
  concluding the tree is gone.
- **Upstream is `SuperInstance/AI-Writings`** (the `ai-writings/cellular-first-design` slug
  404s; the API is case-insensitive). `gh` is **not installed** — use
  `GET /search/repositories?q=...` and `GET /user/repos` with `GITHUB_TOKEN`.
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`** (script reads the former,
  sandbox stores the latter). Unset => JEV degrades to the 2.0 default and every score is
  constant.
- **`ZAI_URL_OVERRIDE` alone is dead code** — `call_provider()` runs the token gate first.
  Control B needs **both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE`.
- **`ZAI_TOKEN` is absent** from env and the secret store; z.ai returns 401 (endpoint healthy,
  credential gap). JEV is live.
- **Tool timeout 30 s < orchestrator run ~45 s.** Launch detached with stdout to a file, poll
  `ps` + the log. Kill the mock by **exact args** (`python3 /tmp/mock_zai.py`) — two pids.
- **A 200 on a mock probe is not proof the mock is correct.** Probe with the exact long
  cultural prompt and `grep -c Traceback` the mock log.

## Verification pattern (assert on rows, never on exit code)

All failure modes are silent with exit code 0 — a missing token makes `call_provider()` return
`None`, `run_simulation()` return `None`, and the competition short-circuit on
`if not results: return None`.

| Assertion | Expected for `--sims 5 --prompts 5` |
|---|---|
| per-civ `simulations.jsonl` delta | **+10** each (5 sim-phase + 5 competition-phase) |
| total new ledger rows | **80** |
| `meta_log.jsonl` delta | **+5** |
| `Winner:` lines | **5** |
| rows with `[mock-zai` prefix | **80** |
| rows with a JEV `error` key | **0** (this is what proves JEV really scored) |
| distinct `content_preview` per prompt, 8 civs | **8/8** (the session-117 degeneracy guard) |

Isolate this run's rows by **count from the end of the file** (`rows[-delta:]`), not by a `ts`
cutoff — prior sessions left mock rows behind, so a `ts >=` filter pulls in history.
