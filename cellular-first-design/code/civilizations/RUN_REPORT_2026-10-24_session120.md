# Civ Orchestrator — Run Report 2026-10-24, session 120

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Timestamp:** 2026-10-24T18:33Z
**Result:** COMPLETE — 8 civs, 80 sim rows, 5 competitions, 5 winners.

> **Session-120 headline:** the run completed clean under the session-118 mock and passed the
> session-117 degeneracy diagnostic (8/8 distinct previews on every one of the 5 prompts).
> `civ-grounded` (The Grounded) is confirmed as the low-relevance civ for the **25th
> consecutive session**, and the **alignment** gap is still the structural one. New this
> session: the session-119 "quality collapse" did **not** reproduce — `quality` came back at
> 0.106–0.446 with a 0.340 spread, and `alignment` again carried the widest spread (1.043).
> Chooser-vs-`avg_score` agreement was **1/5 (20 %)**.

---

## 1. Pre-flight: the provider path was still not usable as-is

| Check | Method | Result |
|---|---|---|
| z.ai endpoint health | `POST api.z.ai/.../chat/completions`, dummy token | **HTTP 401** `token expired or incorrect` |
| `ZAI_TOKEN` in env | `env \| grep -i zai` | **absent** |
| `ZAI_TOKEN` in sandbox secrets | `secret list` (8 secrets) | **absent** from all 8 |
| JEV liveness | `POST api.typesafe.ai/v1/systemone`, malformed `questions` | **HTTP 422** `dict_type` — auth accepted, endpoint live |

Standing credential gap re-confirmed (sessions 102–119, now **20 consecutive**): **z.ai is
healthy, the credential is absent.** A 422 on a malformed payload is a *shape* complaint, so
it proves the JEV token was accepted — it is not a liveness failure.

### Control B: mock z.ai bridge

`ZAI_URL_OVERRIDE` alone is still dead code — `call_provider()` runs the token gate first
(`if not token: return None`), so Control B needs **both** `ZAI_TOKEN` (any non-empty
placeholder) **and** `ZAI_URL_OVERRIDE`. Both were set.

**Mock integrity verified before the run** — not a socket check:

- long multi-sentence cultural prompt (what the orchestrator actually sends) → HTTP 200,
  317/353-char body, `[mock-zai seed=…]` prefix present
- **two different civs ⇒ two different seeds** (`1610ce44` vs `07296801`) — the pre-flight
  non-degeneracy check, run *before* the batch so a broken mock never reaches the ledger
- `grep -c Traceback` on the mock log → **0**
- mock built with the session-112 index-wrap `seed[(i*2)%8:((i*2)%8)+2]` and the
  session-118 `md5(whole_message)[:8]` seed

Mock pids: wrapper `timeout` (222) + server `python3 /tmp/mock_zai.py` (224). Both killed by
exact-args match; port 8799 confirmed closed afterward (curl exit 7).

---

## 2. Environment: NAS EDQUOT + symlink bridge

`/workspace` was 100 % full (600 G/600 G, 0 bytes free) — `git clone` into
`/workspace/repos/...` died with `Disk quota exceeded` on `.git/description`. **Every write
to the NAS fails**; the symlink bridge is the only way in.

Upstream is **`SuperInstance/AI-Writings`** — the `ai-writings/cellular-first-design` slug
404s; the API is case-insensitive but the owner is `SuperInstance`, not `ai-writings`.
`gh` is not installed (**7th session running**).

Bridge: clone to `/tmp` (overlay; the NAS quota does not apply), then

```bash
ln -sfn /tmp/ai-writings/cellular-first-design \
  /workspace/repos/ai-writings/cellular-first-design
```

Verified by **inode identity**, not `ls`: `stat -L -c '%d:%i'` → `129:1772` on both sides
and `-ef` → true. **Did not flatten the clone** (session-115 trap); the symlink points at the
*nested* `cellular-first-design` dir.

`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN` (script reads the former, sandbox stores
the latter). Unset ⇒ JEV silently degrades to the 2.0 default and every score becomes a
constant.

---

## 3. Verification — assert on rows, never on exit code

`call_provider()` returns `None` on a missing token, `run_simulation()` returns `None`, and
the competition short-circuits on `if not results: return None` — **all silently, exit code 0.**

| Assertion | Expected | Actual | |
|---|---|---|---|
| per-civ `simulations.jsonl` Δ | **+10** each (5 sim + 5 competition) | **+10** × 8 civs | ✅ |
| total new ledger rows | **80** | **80** | ✅ |
| `meta_log.jsonl` Δ | **+5** | **+5** (333 → 338) | ✅ |
| `Winner:` lines in run log | **5** | **5** | ✅ |
| rows with `[mock-zai` prefix | 80/80 | **80/80** | ✅ |
| rows with a JEV `error` key | **0** | **0** | ✅ |
| `provider` field | `zai` only | `zai` 80/80 | ✅ |
| score dims non-constant | >1 distinct value | 37–67 distinct per dim | ✅ |
| sim→competition ts gap at index 4 | present in all 8 | 1.0 s–22.9 s, all 8 | ✅ |
| both phases monotonic in ts | true | true × 8 | ✅ |

Rows were isolated **by count** (`rows[-10:]` against the known pre-run totals), not by a
`ts` cutoff — prior sessions left mock rows in the ledger.

### The `ls` race on the symlinked deep path — reproduced, and a new detail

`ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/` failed
**twice** this session with `No such file or directory` while the tree was provably present
(`stat -L` inode `129:1774`, `readlink -f` correct, `[-e]` EXISTS, `-ef` SAME, and 40/40
retries OK across the trailing-slash and no-trailing-slash variants).

**New detail this session:** the failure is **not** explained by the trailing slash.
`ls -la <path>` and `ls -la <path>/` both failed on the same calls, and both succeeded on
20/20 subsequent retries. The symptom remains **intermittent and unexplained**; the
documented diagnostic (inode identity + `readlink -f` + `[-e]` + retry) and the rule
*"a single `ls` failure is not evidence of a missing directory"* both stand. A 2-of-2
failure rate here is the **opposite** of the "5/5 consistent failure ⇒ wrong symlink target"
signature from session 115 — consistency, not intermittency, is what distinguishes the two.

---

## 4. Mock non-degeneracy — the check that makes the competition results valid

```python
# for ONE competition prompt, across the 8 civs
assert len({r["content_preview"] for r in new_competition_rows}) == 8
```

| prompt | distinct previews | distinct seeds |
|---|---|---|
| what a cell is | **8/8** | 8 |
| the bookkeeper's role | **8/8** | 8 |
| the witness log | **8/8** | 8 |
| ternary values | **8/8** | 8 |
| JEV as a decision oracle | **8/8** | 8 |

**40/40 across the run** — the second clean measurement in the fleet's history (session 118
was the first). The mock is **not** degenerate, so unlike the session-117 run this
session's competition ordering and `avg_score` spread are **real measurements**, and the
historical "chooser vs argmax ≈ 15 %" figure (taken under the degenerate mock) remains void.

---

## 5. Per-civ results, this run (10 rows each)

| civ | qual | nov | align | avg_score | competitions won |
|---|---|---|---|---|---|
| civ-poetic | 0.446 | 1.742 | 1.846 | **1.3447** | 0 |
| civ-precise | 0.314 | 1.857 | 1.562 | 1.2443 | **4** |
| civ-whimsical | 0.354 | 1.687 | 1.539 | 1.1933 | 0 |
| civ-therapist | 0.221 | 1.865 | 1.233 | 1.1063 | 0 |
| civ-mythic | 0.189 | 1.539 | 1.076 | 0.9347 | 0 |
| civ-formal | 0.133 | 1.627 | 1.005 | 0.9217 | 1 |
| civ-grounded | 0.109 | 1.668 | 0.836 | 0.8710 | 0 |
| civ-engineer | 0.106 | 1.670 | 0.803 | **0.8597** | 0 |

### Cross-civ spread per dimension (the session-119 rule: compare spreads, not levels)

| dimension | spread | best | worst |
|---|---|---|---|
| **alignment** | **1.043** | civ-poetic (1.846) | civ-engineer (0.803) |
| avg_score | 0.485 | civ-poetic | civ-engineer |
| quality | 0.340 | civ-poetic (0.446) | civ-engineer (0.106) |
| novelty | 0.326 | civ-therapist (1.865) | civ-mythic (1.539) |

**`alignment` again carries the widest spread** — and it is the dimension the chooser is
*supposed* to select on.

---

## 6. The session-119 "quality collapse" did NOT reproduce

Session 119 measured `quality` at **0.009–0.030** for every civ (a ~25× drop from lifetime,
spread 0.021). This session measured **0.106–0.446** (spread 0.340) — a **~10× higher
level** and a **16× wider spread**.

| | session 119 | session 120 |
|---|---|---|
| quality range | 0.009–0.030 | **0.106–0.446** |
| quality spread | 0.021 | **0.340** |
| alignment spread | 1.263 | 1.043 |

**Interpretation.** Session 119's reading — *"`quality` should be treated as a broken axis
whenever its cross-civ spread is small"* — still holds as a rule, but the *collapse itself*
was **not a stable property of the mock**; it was a one-session artifact. This session's
`quality` carries a usable spread and ranks the civs consistently with `alignment` and
`avg_score`. So: **the session-119 "new finding" is downgraded from a run property to a
possible one-off.** The durable rule it contributed — *compare cross-civ spreads, not
absolute levels, before ranking on a dimension* — survives and is re-confirmed here.

**Why the mock's text still bounds the absolute numbers:** the mock emits word-salad by
construction, so a *low* absolute `quality` is expected and not a defect. What is
measurable is the **ordering** and the **spread**, and both are sound this session.

---

## 7. Chooser vs `avg_score` argmax: 1/5 (20 %)

| prompt | winner | winner score | argmax | argmax score | agree |
|---|---|---|---|---|---|
| what a cell is | civ-precise | 1.243 | civ-therapist | 1.527 | no |
| the bookkeeper's role | civ-precise | 1.427 | civ-poetic | 1.703 | no |
| the witness log | civ-formal | 1.143 | civ-poetic | 1.513 | no |
| ternary values | civ-precise | 1.337 | civ-precise | 1.337 | **yes** |
| JEV as a decision oracle | civ-precise | 1.047 | civ-whimsical | 1.377 | no |

Agreement across the three clean-mock sessions: **0/5 (118) → 3/5 (119) → 1/5 (120)**. All
three are 5-sample points, so the honest statement is: **agreement is somewhere in 0–60 %, and
no single run can say which.** What survives all three: **the chooser is not a pure
`avg_score` argmax**, and in all 4 disagreements this session the chooser picked a
**lower**-scoring candidate — re-confirming sessions 116/118/119 for a **fourth**
consecutive session.

`civ-precise` won 4/5 and `civ-formal` 1/5. `civ-poetic` was argmax in 2/5 and near-argmax
in a 3rd, and won **zero** — the stable inversion, again.

---

## 8. The low-relevance civilization

### `civ-grounded` (The Grounded) — low relevance, 25 consecutive sessions (95–120)

**Last on every lifetime aggregate:**

| dimension | value | rank |
|---|---|---|
| avg_score | **1.2925** | **8/8 last** |
| alignment | **1.5820** | **8/8 last** |
| quality | 0.6477 | 8/8 last |
| relevance | **810.06** | 8/8 last |
| relevance_per_sim | **1.248** | 8/8 last |

**The structural gap is `alignment`, not quality.** Grounded is **0.408 below the next civ**
(1.582 vs 1.990, `civ-therapist`) on alignment, versus only **0.035 below** on quality
(0.648 vs 0.683). `alignment` is the dimension the meta-GAN *selects* on, so the civ fails to
**embody a distinctive voice** — not merely to write well. This is a *voice* failure, not a
*prose* failure, and it is the one gap wide enough to be structural rather than noise.

The per-dimension rankings (session-119 rule) confirm the same shape on this run's rows:
`alignment` worst→best is `civ-engineer < civ-grounded < civ-formal < civ-mythic <
civ-therapist < civ-whimsical < civ-precise < civ-poetic` — Grounded is **2nd worst**,
i.e. near the floor on the axis that matters most.

### The other two axes (unchanged, and distinct)

- **`civ-formal`** — lowest **novelty** (lifetime 1.4652, 8/8 last). Its alignment (2.2499)
  is healthy; it is a *conservatism* axis, not a failure.
- **`civ-engineer`** — last on this run's `avg_score` (0.8597) and on this run's `quality`
  (0.106) and `alignment` (0.803). It is **not** the lifetime low-relevance civ (lifetime
  `relevance_per_sim` 1.461, 6th of 8); it is a **single-run** low, and it is a new
  low on the run's score dims. Worth watching: it has now placed last on the run's `avg_score`
  and `alignment` where it was 6th on lifetime relevance. One run is not a trend.

### The two stable inverses (unchanged)

- **`civ-poetic`** — 1st on lifetime `avg_score` (1.9173), 1st on `quality` (1.0997), 1st on
  `alignment` (2.5378), 1st on `relevance_per_sim` (1.876) — and **last** on `win_rate`
  (0.016). A *selection* failure, not a quality collapse. It won **0/5** this session and
  was argmax in 2/5.
- **`civ-precise`** — best `win_rate` (0.500) and **4/5 competition wins**, but 6th on
  lifetime `avg_score` (1.6265). The mirror-image inverse.

### Extinction risk: NONE

Threshold is **−10**; the lowest raw relevance is `civ-grounded` at **+810.06** — **81×**
above the floor. Registry is **8** civs against `max_civs` 12. Extinction/birth only runs
under `--loop`, which was not used.

### Counter gap (per-civ uneven, unchanged by this run)

| civ | ledger | sims_run | gap |
|---|---|---|---|
| civ-whimsical | 704 | 641 | **+63** |
| civ-grounded | 692 | 649 | **+43** |
| civ-formal | 677 | 635 | **+42** |
| civ-poetic | 671 | 634 | +37 |
| civ-engineer | 646 | 624 | +22 |
| civ-mythic | 649 | 629 | +20 |
| civ-therapist | 644 | 627 | +17 |
| civ-precise | 641 | 625 | +16 |

`save_state()` rewrites `culture.json` with no lock ⇒ `relevance_per_sim` is **not
recomputable from the ledger** by an auditor. Identical to session 118's per-civ values,
which is the expected result: the gap only advances on a re-save.

---

## 9. Standing operational rules (all re-confirmed this session)

- **Assert on rows, never on exit code.** `call_provider` / `run_simulation` / the
  competition all fail silently with exit 0.
- **A single `ls` failure is not evidence of a missing directory.** Inode identity +
  `readlink -f` + `[-e]` + retry. A *consistent* 5/5 failure is the different signature
  (wrong symlink target) — this session failed 2/2 then passed 20/20, i.e. intermittent.
- **`ZAI_URL_OVERRIDE` alone is dead code** — the token gate returns `None` first. Control B
  needs **both** `ZAI_TOKEN` and `ZAI_URL_OVERRIDE`.
- **Never flatten the clone.** The symlink points at the *nested* `cellular-first-design` dir.
- **Clone into `/tmp`**, symlink from `/workspace`; the NAS EDQUOT trap is total.
- **Isolate a run's rows by count, not by a `ts` cutoff.**
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs**, not a dict.
- **Mock non-degeneracy must be asserted** (8 distinct previews per prompt) before any
  competition result is trusted; run it as a pre-flight against two different civs so a
  broken mock never reaches the ledger.
- **Compare cross-civ spreads, not absolute levels**, before ranking civs on a dimension.
- **`win_rate` is a selection metric, never a quality metric.**
- **`TYPESAFEAI_KEY` must be exported** or JEV silently returns the constant 2.0 default.
- Tool-call timeout (30 s) < run (~45 s): launch detached, poll `ps` + the log.
- `gh` is not installed — use the REST API with `GITHUB_TOKEN`.
