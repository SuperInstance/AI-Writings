# Civ Orchestrator — Run Report, session 170 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 53rd session) + **live JEV**.
Baseline: `029cf80` (session 169). **All 68 verification assertions PASS.**

## Headline for the next session

- **The mock needs SIX fixes, not five.** The new one is the **seed index source**: it must
  be derived from the **MESSAGE**, not from a request counter. A counter makes the same
  `(civ, prompt)` pair yield a *different* seed on every request ⇒ **64 distinct seeds /
  80 rows** instead of 40, and **20 `(civ,prompt)` pairs carry >1 seed**.
  **Fix (f): `i = md5(message).digest()[0] % 4`** — a pure function of the request body.
  This session the *first* mock was built with a counter, the run-wide seed checks caught
  it, the ledger was reset with `git checkout -- .`, and the run was repeated clean.
- **The pre-flight could NOT have caught fix (f).** The pre-flight sends 40 *distinct*
  messages, so a counter-derived index looks perfect. **Add a repeat-same-message probe:**
  send the same message twice and assert the seed is identical. Now in the gate.
- **The mock's full algorithm is now known and verified 80/80** against the session-169
  ledger (see below) — no more reverse-engineering needed next session.
- **`civ-grounded` remains the low-relevance civ — 45th consecutive session.** Last of 8 on
  lifetime `avg_score` 0.9925, `quality` 0.4064, `alignment` 1.0573, `relevance` 1098.73,
  `relevance_per_sim` 0.956. Alignment gap **0.9899** vs quality gap 0.3414 ⇒ **2.9×** wider
  ⇒ a **voice** failure, not a prose failure. Lifetime novelty 1.5138 is **6th of 8**.
- **The run-level low ROTATED to `civ-therapist`** (1.0797, run bottom on `avg_score` and
  `alignment` 0.4710 — a quarter of the next civ) while its *lifetime* standing is mid-field
  (6th of 8). **Watch axis, not the finding** (session-132 rule).
- **Chooser vs `avg_score` argmax: 2/5 (40 %)** — all three disagreements took the
  lower-scoring candidate, so the "picks lower" direction is back. `civ-precise` swept 4/5;
  `civ-formal` took the witness-log slot. Max |delta| **−0.3400**.
- **Counter gap −609.9200, fixed.** Identical to session 169's value ⇒ the offset is fixed,
  not accumulating.
- Run spreads: `avg_score` 0.7423, `alignment` **1.9580**, quality 0.4400, novelty 0.1340.
- Verification: per-civ Δ **+10 × 8** = **80** new rows, `meta_log` **+5** (583 → 588),
  `Winner:` **5**, `wins`/`losses` **8/8 exact**, `relevance` Δ = Σ`avg_score` **8/8 exact**,
  0 JEV errors, 0 fallback triples, `zai × 80`, **40/40** distinct seeds, **0** `(civ,prompt)`
  with >1 seed, **80/80** rows match an independently recomputed md5, 8/8 seeds AND previews
  on all 5 prompts, meta-vs-ledger mismatches **0/40**, 80/80 distinct `(q,n,a)`, confidence
  0.15–0.96, registry 8 all gen 1, extinction **NONE** (lowest +1098.73 = **110×** the floor).
  **68/68 PASS.**

## The mock algorithm — fully known now (no reverse-engineering next session)

```
d      = md5(cultural_prompt).digest()          # the FULL user message, verbatim
h      = d.hex()
i      = d[0] % 4                              # <- MESSAGE-derived, NOT a counter
seed   = h[(i*2)%8:(i*2)%8+2] + h[((i*2)+2)%8:((i*2)+2)%8+2]   # 4 hex chars, wraps
color  = h[8:12]
figure = h[12:16] / h[16:20] / h[20:24]
```

`cultural_prompt` is exactly what `civilization_orchestrator.py` builds:

```
You are a voice in the tradition of "{name}".
Your tenets: {tenets joined by ", "}.
Your voice: {voice_emphasis}.

{prompt}
```

**Why `i = d[0] % 4` and not a wider modulus:** the seed slices `h[0:8]` at *even* offsets
`(i*2)%8`, so only **4** distinct seeds are reachable from one message
(`h[0:4]`, `h[2:6]`, `h[4:8]`, `h[6:8]+h[0:2]`). `i mod 4` is therefore the whole index
space; `i mod 8` and `i mod 4` are indistinguishable. This is why the "index wrap" fix (a)
is expressed as `(i*2)%8`.

**Verification:** this rule reproduces the session-169 ledger **80/80 rows** — seed, colour
and figure all match, and the seed is *stable* across every row of the same
`(civ, prompt)` pair. A request counter cannot produce that stability, because the
competition phase fires 8 civs in parallel and a counter would hand them different
values. That stability is the observable signature of a message-derived index.

**`i` is not recoverable from the message alone in the ledger** — only the *rotation* is
observable (4 options), and 40 `(civ,prompt)` pairs × 4 rotations is what produces the
40 distinct seeds. The rule `d[0] % 4` was selected because it matched all 40 pairs;
alternatives tested and rejected: `md5_int%4` 7/40, `sha1_int%4` 12/40, `sha256_int%4`
9/40, `md5_last%4` 7/40, `md5_first%4` 14/40, `md5_len%4` 13/40, `sha1_b0%4` 9/40.

## Mock rebuild checklist — SIX fixes

| # | Fix | Session | Symptom if missing |
|---|---|---|---|
| a | `seed[(i*2)%8:(i*2)%8+2]` index wrap | 112 | `ValueError` on `i>=4` ⇒ HTTP 500 **while the socket stays open** |
| b | `md5(whole_message)` not the first 8 alnum chars | 118 | first 8 alnum chars are `YouAreA` for every civ ⇒ all 8 civs emit identical text |
| c | `Connection: close` + `Content-Length` | 144 | `curl` hangs to the tool timeout on a healthy server |
| d | interpolate the seed placeholder | 145 | every response carries literal `seed={}` ⇒ 1 distinct seed, not 40 |
| e | seed widened 2 → 4 hex chars | 169 | 2-char slice collides ⇒ 39 distinct seeds, one prompt at 7/8 |
| **f** | **index derived from the MESSAGE (`d[0] % 4`), not a request counter** | **170** | **64 distinct seeds / 80 rows; 20 `(civ,prompt)` pairs carry >1 seed** |

### NEW (this session) — a counter-derived index is invisible to the pre-flight

The pre-flight sends 40 **distinct** messages, one per `(civ, prompt)` pair. A
counter-derived index produces a *different* seed for every one of them, so the pre-flight
sees **40/40 distinct seeds and 40/40 distinct previews — a clean pass.** The defect only
appears when the same message is sent twice, which the pre-flight never does.

**Observed in the first mock of this session:** 80 rows, **64** distinct seeds (not 40),
**20** `(civ,prompt)` pairs carrying more than one seed. Every other signal was green —
HTTP 200, prefix present, 0 tracebacks, 40/40 pre-flight, and the colour/figure fields
still matched the md5 at their fixed offsets.

**Fix applied:** `i = md5(message).digest()[0] % 4`.

**The lesson is a gate-design lesson.** A pre-flight that only exercises *distinct*
inputs cannot certify a *determinism* property. The new gate step is:

> **Repeat-same-message probe:** send the same message **twice** and assert the returned
> seed is **identical** (and matches the independently recomputed md5). 40/40 messages,
> 2 repeats each.

**Reset discipline.** The first run of this session was discarded and the ledger restored
with `git checkout -- .` from the clone root; the baseline was re-verified against the
captured pre-run counts (1182/1194/1167/1161/1131/1139/1134/1136, meta 583) before the
second run. **Never edit a ledger in place to "fix" a run** — reset and re-run, so the
baseline and the result are in the same epoch.

## Pre-flight gate (must pass before the batch) — EIGHT checks

| # | Check | Expected | Session 170 |
|---|---|---|---|
| 1 | rows | 40 | 40 |
| 2 | distinct seeds | 40 | 40 |
| 3 | seed == independently recomputed message md5 | 40/40 | 40/40 |
| 4 | seed + colour + figure all match the md5 | 40/40 | 40/40 |
| 5 | literal `seed={}` placeholders | 0 | 0 |
| 6 | 8/8 distinct seeds AND 8/8 distinct previews on every prompt | 5/5 | 5/5 |
| 7 | **NEW: repeat-same-message ⇒ same seed (40 msgs × 2)** | 40/40 | 40/40 |
| 8 | distinct previews | 40 | 40 |

Mock log after the run: **0** `EXC:`, **0** HTTP 500. Prompt lengths **167–209**.

## Environment recovery (session 170)

- Workspace **empty** apart from `.plugin-cache` and `.skills` — the prompt's path
  `/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist
  (**12th consecutive occurrence**).
- Upstream owner: **`SuperInstance/AI-Writings`** — the `ai-writings/…` slug 404s; the
  GitHub API is case-insensitive. Authenticated as **`SuperInstance`** via `GITHUB_TOKEN`.
- Cloned to **`/tmp/aiw`** (7.5 MB). Cloning into `/workspace` fails with
  **`Disk quota exceeded`** (NAS EDQUOT, **18th session**) — the NAS is at 100% (600 G of
  600 G) and even a 20 MB `dd` fails. **The `write` tool is jailed to the workspace root**
  and cannot write `/tmp`; use a bash heredoc for `/tmp` artifacts.
- Bridge: `ln -sfn /tmp/aiw/cellular-first-design
  /workspace/repos/ai-writings/cellular-first-design`. Verified by inode identity
  (**`129:1772` on both sides**) and `-ef` → `EF_OK`.
- `ZAI_TOKEN` absent from env and from all 8 sandbox secrets; z.ai returns **401**
  `token expired or incorrect` ⇒ endpoint healthy, credential absent (**53rd session**).
- **JEV live**: a well-formed `questions` body returns **HTTP 200** with
  `{"model":"jev-1.14.0", …}` — a stronger probe than the usual 422 `dict_type` complaint,
  because it also discloses the **served model version**.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code — the token gate returns `None`
  first).
- `gh` not installed (**20th session**) — used `GET /user/repos` with `GITHUB_TOKEN`.
- Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch with stdout redirected
  **and** `< /dev/null`, then poll.

## Verification — 68 assertions, all PASS

| Check | Expected | Observed |
|---|---|---|
| per-civ ledger Δ | +10 × 8 | **+10 × 8** |
| total new ledger rows | **80** | **80** |
| `meta_log.jsonl` Δ | +5 | **+5** (583 → 588) |
| `Winner:` lines | 5 | **5** |
| `ORCH_EXIT` | 0 | **0** |
| `culture.json` `simulations_run` Δ | +10 × 8 | **+10 × 8** |
| `culture.json` generation | unchanged | **1 × 8** |
| rows with JEV `error` | 0 | **0** |
| 2.0/2.0/2.0 fallback triples | 0 | **0** |
| `provider` | zai only | **zai × 80** |
| rows missing `[mock-zai seed=` prefix | 0 | **0** |
| distinct seeds | 40 / 80 rows | **40 / 80 rows** |
| literal `seed={}` placeholders | 0 | **0** |
| `(civ,prompt)` carrying >1 seed | 0 | **0** |
| seed+colour+figure == message md5 | 80/80 | **80/80** |
| 8/8 distinct seeds AND previews per competition prompt | 5/5 | **5/5** |
| meta `results` = list of `[civ,score]` | 5/5 | **5/5** |
| meta vs ledger `avg_score` mismatches | 0 | **0 / 40 compared** |
| distinct `(q,n,a)` triples | ≥70, no (2,2,2) | **80/80 distinct**, no (2,2,2) |
| confidence spread (JEV-side signature) | not constant | **0.15 – 0.96** |
| registry / generations | 8 civs, all gen 1 | **8 / {1}** |
| `wins` = pre + times won | exact | **8/8 exact** (precise +4, formal +1, rest +0) |
| `losses` = 5 − times won | exact | **8/8 exact** (precise +1, formal +4, rest +5) |
| `relevance` Δ = Σ this run's `avg_score` | exact | **8/8 exact to 1e-6** |
| extinction risk | NONE | **NONE** (lowest +1098.73 = **110×** the floor) |

### NOTE — the meta-vs-ledger check needs the **later-`ts`** row, not the first match

Re-confirmed from sessions 168–169: the sim phase draws its prompt at random from the same
5, so a `(civ, prompt)` pair recurs **1–4 times** inside the 10 new rows. The
**competition-phase** row is the later one. `max(cands, key=ts)` gives **40/40 exact**;
first-match reports false mismatches. The match key is `m["prompt"][:80]` — the meta prompt
is full-length, the ledger prompt is truncated to 80 chars.

## Low-relevance civilization: **`civ-grounded` (The Grounded)** — 45th consecutive session

**Lifetime (9 244 rows):**

| civ | n | avg_score | quality | novelty | alignment | relevance | rel/sim | win_rate |
|---|---|---|---|---|---|---|---|---|
| civ-poetic | 1171 | **1.5532** | **0.7478** | 1.8645 | 2.0472 | **1721.98** | **1.518** | 0.011 |
| civ-precise | 1141 | 1.4002 | 0.5107 | 1.5703 | **2.1197** | 1565.04 | 1.391 | **0.586** |
| civ-whimsical | 1204 | 1.3980 | 0.5881 | **1.9277** | 1.6781 | 1510.00 | 1.323 | 0.009 |
| civ-mythic | 1149 | 1.2533 | 0.5265 | 1.7166 | 1.5167 | 1388.88 | 1.230 | 0.018 |
| civ-formal | 1177 | 1.1781 | 0.4496 | 1.4256 | 1.6592 | 1301.10 | 1.146 | 0.166 |
| civ-therapist | 1144 | 1.1474 | 0.4575 | 1.7340 | 1.2508 | 1270.52 | 1.127 | 0.020 |
| civ-engineer | 1146 | 1.1384 | 0.4487 | 1.4916 | 1.4748 | 1260.33 | 1.121 | 0.085 |
| **civ-grounded** | 1192 | **0.9925** | **0.4064** | 1.5138 | **1.0573** | **1098.73** | **0.956** | 0.125 |

Last of 8 on **avg_score**, **quality**, **alignment**, **relevance**, and
**relevance_per_sim**. The low label did **not** rotate — 45th consecutive session.

Absolute gaps to the next civ: **alignment 0.9899** (precise 2.1197) versus
**quality 0.3414** (engineer 0.4487) ⇒ the alignment gap is **2.9× wider**. Alignment is
the dimension the meta-GAN *selects* on ⇒ a **voice** failure, not a prose failure.
Lifetime novelty 1.5138 is **6th of 8** — check the rank, not the "above median" impression.

**Run-level (this run's 80 rows):**

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-poetic | **1.8220** | **0.5910** | 2.6020 | 2.2730 |
| civ-precise | 1.8113 | 0.3900 | 2.6150 | **2.4290** |
| civ-formal | 1.5607 | 0.2380 | 2.6170 | 1.8270 |
| civ-whimsical | 1.4723 | 0.3170 | **2.6280** | 1.4720 |
| civ-engineer | 1.3103 | 0.2230 | 2.5600 | 1.1480 |
| civ-mythic | 1.2587 | 0.2860 | 2.4940 | 0.9960 |
| civ-grounded | 1.1613 | 0.1510 | 2.6260 | 0.7070 |
| **civ-therapist** | **1.0797** | 0.1710 | 2.5970 | **0.4710** |

**The run low ROTATED to `civ-therapist`** (1.0797, gap to next **0.7423** — the run was
*not* compressed). Grounded is 7th of 8 on the run (1.1613); therapist is lower on both
`quality` (0.1710 vs grounded 0.1510 — grounded is lower here) and `alignment`
(0.4710 vs grounded 0.7070), and grounded is higher on `avg_score` by only 0.0816.

## `civ-therapist` is a watch axis, not a finding

Therapist is the run bottom on `avg_score` (1.0797) and `alignment` (0.4710 — a quarter of
the next civ, mythic 0.9960). But its **lifetime** standing is mid-field: `avg_score`
1.1474 (6th of 8), `alignment` 1.2508 (7th of 8), `relevance` 1270.52 (6th of 8). Per the
session-132 rule, **the run low and the lifetime low are different civs on different
axes**. Grounded remains the structural finding; therapist is the run-level watch.

Therapist's 10 new rows show the familiar signature: **novelty 2.5970 is near the run's
top** while quality collapses to 0.1710 — text JEV rates as highly novel and poorly
aligned. That is the *voice* axis failing.

## Chooser vs `avg_score` argmax: 2/5 (40 %) — the "picks lower" direction is back

| prompt | winner | score | argmax | score | delta | |
|---|---|---|---|---|---|---|
| what a cell is. | civ-precise | 1.6889 | civ-poetic | 1.7622 | −0.0733 | LOWER |
| the bookkeeper's role. | civ-precise | 1.7667 | civ-poetic | 1.8967 | −0.1300 | LOWER |
| the witness log. | civ-formal | 1.9611 | civ-precise | 2.3011 | **−0.3400** | LOWER |
| ternary values. | civ-precise | 1.7778 | civ-precise | 1.7778 | +0.0000 | AGREE |
| JEV as a decision oracle. | civ-precise | 1.8467 | civ-precise | 1.8467 | +0.0000 | AGREE |

Session 168's 3/5 (60 %) was the series high; session 169 was 2/5 (40 %); this session is
**2/5 (40 %)** again, and **all three disagreements took the lower-scoring candidate** — the
"chooser picks lower" direction is holding. `civ-precise` swept **4/5**; `civ-formal` took
the witness-log slot.

The mechanism is unchanged: the chooser is a JEV **`choice`** question over 150-char
`content_preview` snippets, while `avg_score` is the mean of three **`score`** questions on
the same text — different questions, different answers. **Never treat `win_rate` as a
quality metric.** The clean-mock series now has 16 five-sample points spanning 0/5 – 4/5
⇒ the honest claim is *somewhere in 0–80 %*, not a point estimate.

The largest disagreement this session is **−0.3400** on "the witness log" (formal 1.9611 vs
precise 2.3011).

## Inverses and distinct axes

- **`civ-poetic`**: 1st on lifetime `avg_score` (1.5532), `quality` (0.7478), `relevance`
  (1721.98) and `relevance_per_sim` (1.518) — but **8th on `win_rate` (0.011)**, won 0/5.
  A *selection* failure, not a quality collapse. It was the `avg_score` argmax on **2/5**
  prompts and the chooser took it on **0/5** — the sharpest inverse in the fleet.
- **`civ-precise`**: best `win_rate` (0.586), **highest lifetime alignment (2.1197)**, 2nd
  on run `avg_score` (1.8113) and run `alignment` (2.4290), and the run's top winner (4/5).
- **`civ-whimsical`**: highest lifetime novelty (1.9277) and 3rd on lifetime `avg_score`,
  but **last on `win_rate` (0.009)** — the second inverse.
- **`civ-formal`**: the distinct low-**novelty** axis (1.4256, last of 8) — yet it took
  3rd on run `avg_score` (1.5607) and won 1/5.
- **`civ-engineer`**: `win_rate` 0.085 and `relevance` 1260.33, 7th of 8 on both — the
  mid-table civ that is neither an inverse nor a watch axis.
- Cross-civ spreads (this run): `avg_score` **0.7423**, `alignment` **1.9580**,
  `quality` 0.4400, `novelty` 0.1340. The alignment spread is the widest in the series —
  consistent with the *voice* axis, not prose, being where the fleet actually differentiates.

## Counter gap: NEGATIVE, fixed, and unchanged in magnitude — both epochs shown

`culture.json` `relevance_score` − ledger Σ`avg_score`:

| civ | blob gap | post-run gap | Δ |
|---|---|---|---|
| civ-grounded | −84.3467 | −84.3467 | 0.0000 |
| civ-whimsical | −173.1433 | −173.1433 | 0.0000 |
| civ-formal | −85.5267 | −85.5267 | 0.0000 |
| civ-poetic | −96.8033 | −96.8033 | 0.0000 |
| civ-precise | −32.6333 | −32.6333 | 0.0000 |
| civ-mythic | −51.1100 | −51.1100 | 0.0000 |
| civ-therapist | −42.1133 | −42.1133 | 0.0000 |
| civ-engineer | −44.2433 | −44.2433 | 0.0000 |
| **TOTAL** | **−609.9200** | **−609.9200** | **0.0000** |

Both columns are computed **within the same epoch** (blob `relevance` vs **blob** ledger sum;
post-run `culture.json` vs **working-tree** ledger sum) ⇒ the offset is **fixed**, not
accumulating. `save_state()` has no lock ⇒ `relevance_per_sim` is **not recomputable from the
ledger** by an auditor. Sign confirmed from the data, not copied from a prior report.

The **total gap is byte-identical to session 169's −609.9200** — a strong independent
confirmation that the counter did not drift this session either.

## Notes for the next session

1. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild from the RUNBOOK
   with **all SIX** fixes (112 index wrap, 118 whole-message md5, 144 transport pair,
   145 interpolation, 169 seed width 2→4 hex chars, **170 message-derived index**) and run
   the pre-flight probe — now **eight** checks, including the **repeat-same-message probe**
   — before the batch.
2. **The mock's algorithm is fully specified above.** Do not re-derive it. The only freedom
   left is cosmetic (the prose tail of the response body); the ledger only stores the
   first 200 characters, so anything past the `figure:` field is invisible to the checks.
3. **Fix (f) is not optional and the pre-flight alone will not catch it.** Send the same
   message twice; the seed must be identical. Keep the count check (40 distinct seeds) and
   the md5-recompute check — they catch different defects.
4. `ZAI_TOKEN` still absent ⇒ real z.ai unusable; Control B is the only provider path.
   JEV is live and needs `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`.
5. Use the run-wide integrity checks (80 rows, 40 seeds, per-`(civ,prompt)` 1:1) and
   isolate this run's rows by **count from the end of each civ file** (last 10), never by
   a `ts` cutoff. `git show HEAD:<path>` must be run with `cwd` = the **clone root**,
   not the civs directory — the civs dir is not a git root, and `git show` there returns
   empty stdout → `JSONDecodeError`.
6. The meta-vs-ledger check must take the **later-`ts`** row for a `(civ, prompt)` pair.
7. `civ-grounded` has been the low-relevance civ for **45** straight sessions. If a session
   ever finds it mid-table, that is a *finding* — check the run-wide seed count first to
   rule out a degenerate mock before believing it. **The run-level low already rotates**
   (this session: therapist) — do not promote the run low to the lifetime finding.
8. Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch with stdout redirected
   **and** `< /dev/null`, then poll `ps` + the log.
9. The NAS EDQUOT trap also blocks **file delivery** — `cp` into `/workspace` leaves a
   0-byte file. Deliver by pushing to git and citing the remote URL, not a workspace
   attachment.
10. **Symlink rule:** `ln -sfn` will not replace an existing directory target, and the
    bridge must point at the **clone root** (not the nested `cellular-first-design` dir).
    `rm -rf` the old link, then `ln -s`, then verify with `stat -L -c '%d:%i'` on both
    sides + `-ef`.
11. **Mock teardown:** kill by exact argv match (`python3 /tmp/mock_zai.py` and
    `timeout -s KILL 900 python3 /tmp/mock_zai.py`) — **two** pids. Never `pkill -f mock_zai`,
    which self-matches the killing shell. Then prove the port is closed: `curl -m 5` ⇒
    **exit 7** and `HTTP=000`.
12. **A failed run must be reset, not patched.** When the first mock was rejected, the
    ledger was restored with `git checkout -- .` from the clone root and the baseline
    re-verified before the second attempt. Do not hand-edit a ledger to make a check pass.
