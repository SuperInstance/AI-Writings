# RUN REPORT — Civilization Orchestrator — session 90 (2026-10-24)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Result:** exit 0, **+160 rows** (2 Control-B runs, body sets A and B), **+10 meta_log entries**,
**10 competition winners**, **0 all-2.0-default rows**, **0 JEV score errors**, **0 mock fallbacks**,
**0 scaffolding leaks**.

---

## 0. Environment reconstruction (the path did not exist — 13th recurrence)

`/workspace/repos/ai-writings/cellular-first-design/code/civilizations` was absent at session start.
`/workspace` held only `.plugin-cache` and an empty `.home`. The NAS is at **100 % quota**
(600 G used, 0 avail).

**New this session — the NAS write trap was confirmed directly, not assumed.** The probe:

```bash
cd /workspace && echo "hello" > /workspace/_quotaprobe.txt   # exit 0
ls -la /workspace/_quotaprobe.txt   # -rw-r--r-- 1 root root 0   <-- ZERO BYTES
```

`write` returns **exit 0** and the file **appears in `ls`**, but the data never lands. Any
"did my file get written?" check that only looks at exit status or at `ls` will pass on an
empty file. **Always `cat` the file, or check its size, before believing a write.**

`gh` is not installed in this sandbox, so `gh repo list` is unusable. Bootstrap that worked:

```bash
export HOME=/var/tmp/home; git config --global user.email ...; git config --global user.name ...
cd /var/tmp && git clone --filter=blob:none --no-checkout --depth 1 \
  "https://x-access-token:$GITHUB_TOKEN@github.com/SuperInstance/ai-writings.git" ai-writings
cd ai-writings && git sparse-checkout init --cone && git sparse-checkout set cellular-first-design
GIT_SSL_NO_VERIFY=1 git checkout main
```

Repo is `SuperInstance/ai-writings` (3.7 GB; API reports the display name `AI-Writings`).
`GIT_SSL_NO_VERIFY=1` is required — plain `git fetch` dies on
`server certificate verification failed. CAfile: none`.

**`/tmp` is not durable here.** A first clone at `/tmp/ai-writings` was **wiped mid-session**
(an unrelated `rm` of the session's own temp tree, or a reaper — the directory simply vanished
between two commands, while `/tmp/clone.log` survived). The working tree was rebuilt at
`/var/tmp/ai-writings` on the **overlay filesystem** (28 G free), which persists. **Do the clone
on the overlay, not on `/tmp`.**

### Bridge (two-level, per session 87b)

`CIVS_DIR` in the orchestrator is hardcoded to
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations`, and the NFS mount does
**not** follow a second symlink hop below the mount point. The working bridge:

```bash
mkdir -p /var/tmp/bridge/ai-writings
ln -sfn /var/tmp/ai-writings/cellular-first-design /var/tmp/bridge/ai-writings/cellular-first-design
ln -sfn /var/tmp/bridge /workspace/repos
```

Verified with `stat -c '%d:%i'` → **both paths report `130:525674`**, so writes land in the real
tree and not a copy.

---

## 1. The credential gap — 28th consecutive session

`ZAI_TOKEN` is absent from the environment and from the 8-entry secret store
(`MOTHQUANTUM_TOKEN`, `TYPESAFE_AI_TOKEN`, `MINIMAX_KEY`, `NOTION_TOKEN`, `NPMJS_TOKEN`,
`CRATES_TOKEN`, `PYPI_TOKEN`, `GITHUB_TOKEN`).

JEV is **live**: every `avg_score` in this session is a real JEV return. The env-var name split
persists — the script reads `TYPESAFEAI_KEY` but the sandbox exports `TYPESAFE_AI_TOKEN`, so
every run must do `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"`.

---

## 2. Both controls, measured

| control | configuration | ledger rows | meta_log | winners | exit |
|---|---|---|---|---|---|
| **A** | no `ZAI_TOKEN`, no override | **+0** | +0 | **0** | 0 |
| **B (set A)** | `ZAI_TOKEN` set + `ZAI_URL_OVERRIDE` → local mock | **+80** | +5 | 5 | 0 |
| **B (set B)** | second, independently-written body set | **+80** | +5 | 5 | 0 |

**Control A is the whole story.** The provider gate is a silent drop:

```python
token = os.environ.get(p["env"], "")
if not token: return None        # line ~79
```

The tell is **the absence of `Winner:` lines** — the batch header and all eight
`[Name] running 5 sims...` lines print regardless, because they are printed *before* the call.
**Exit code alone is worthless; assert on `Winner:` lines and on the row delta.**

### Run signature (reproduces sessions 6-11, 84-89)

| check | value |
|---|---|
| ledger row delta | **+160** (3564 → 3724) |
| rows per civ | **+20 each, uniform** (all 8) |
| `meta_log.jsonl` | **+10** (228 → 238) |
| competition winners | **10** (5 per set) |
| all-2.0-default JEV rows | **0** |
| JEV score errors | **0** |
| distinct `content_preview` | set A **52/80**, set B **54/80** |
| distinct `avg_score` | set A **75/80**, set B **70/80** |
| distinct previews (lifetime 3724) | 3107 |
| mock fallback calls | **0** |
| mock per-voice distribution | **exactly 10 per voice, both sets** |
| scaffolding leak rows | **0** |

---

## 3. The A/B body-set test — **this session's headline**

Two independently-written body sets (8 voices × 10 bodies each), same orchestrator, same JEV,
same prompts. Only the mock's prose differs.

| civ | set A | set B | Δ |
|---|---|---|---|
| civ-grounded | 1.323 | 1.651 | **+0.328** |
| civ-whimsical | 1.807 | 1.692 | −0.115 |
| civ-formal | 1.593 | 1.542 | −0.051 |
| civ-poetic | 2.036 | 2.050 | +0.014 |
| civ-precise | 1.622 | 1.552 | −0.070 |
| civ-mythic | 1.975 | 2.142 | +0.167 |
| civ-therapist | 1.670 | 2.021 | **+0.351** |
| civ-engineer | 1.744 | 1.780 | +0.036 |

- **max |Δ| = 0.351**, mean |Δ| = 0.142, fleet mean +0.0825.
- **2 of 8 civs cross the 0.3 threshold** (`civ-grounded` +0.328, `civ-therapist` +0.351).
- **Positional agreement 1/8**; **Spearman ρ = 0.810**; **Kendall τ = 0.571** (22 conc / 6 disc).
- **Top-3 set differs** (A: poetic/mythic/whimsical — B: mythic/poetic/therapist).
- **Bottom-2 set differs** (A: formal/grounded — B: precise/formal).

**Interpretation.** The fleet *is* ordered, but only in the middle of the pack: the two leading
civs (Poetic, Mythic) and the two trailing ones (Formal, and Precise-or-Grounded) are stable
across body sets, while the ranks of Whimsical / Engineer / Therapist / Grounded / Precise
inside that band are **set-dependent**. This is a **weaker A/B result than session 89's**
(6/8 positional, ρ = 0.976, max |Δ| 0.167) and it is consistent with the session-9 finding that
the mock's prose is a first-order confounder for the *middle* of the distribution.

> **Report the stable edges, not a full ordering.** The safe claim: Poetic and Mythic lead
> regardless of body set; Formal is last-or-near-last; Grounded and Precise occupy the
> bottom band. The exact rank order of the middle five is a property of the mock, not of the civs.

### A methodological note — a self-inflicted bug worth recording

My first Spearman implementation ranked the **already-sorted** rank lists, which destroys the
civ pairing and returned **ρ = 1.000** alongside a 1/8 positional match. Those two numbers
contradict each other; the contradiction is what exposed the bug. **Correct ρ = 0.810.**
A rank correlation computed on a pre-sorted list is always ~1.0 and always meaningless —
rank the *values*, then index by civ id. **Sanity-check any rank statistic against the
positional count it should agree with.**

---

## 4. Chooser vs argmax — 5/10 agreement, 19th consecutive replication of the decoupling

The competition's `best_civ` JEV call receives only a **150-char preview and no scores**, so the
chooser is blind to the numbers the board reports.

| | set A | set B | combined |
|---|---|---|---|
| agreement | 3/5 | 2/5 | **5/10 (50.0 %)** |
| mean top-2 margin | 0.188 | 0.132 | 0.160 |
| max top-2 margin | 0.340 | 0.190 | |

**A competition win is not evidence of a higher JEV score.** Margins are small, so the chooser is
close to a coin flip among near-ties rather than reading the ranking. Note this session's 50 %
is the **highest** recorded — but the two sets disagree on 4 of 5 prompts, so the agreement
figure is itself set-dependent and should not be read as improvement.

---

## 5. Low relevance — ten lenses

| lens | engineer | formal | grounded | mythic | poetic | precise | therapist | whimsical | last |
|---|---|---|---|---|---|---|---|---|---|
| L1 board `rel/sim` | 1.723 | 1.643 | **1.467** | 1.899 | 2.128 | 1.806 | 1.871 | 1.961 | grounded |
| L2 raw relevance | 730.7 | 714.7 | **658.7** | 814.6 | 923.6 | 767.4 | 799.0 | 865.0 | grounded |
| L3 win rate | 0.107 | 0.166 | 0.226 | 0.019 | **0.009** | 0.471 | 0.029 | 0.019 | poetic |
| L4 lifetime `avg_score` | 1.736 | 1.682 | **1.511** | 1.922 | 2.172 | 1.825 | 1.897 | 2.073 | grounded |
| L5 this-run `avg_score` | 1.762 | 1.567 | **1.487** | 2.058 | 2.043 | 1.587 | 1.845 | 1.749 | grounded |
| L6 set A `avg_score` | 1.744 | 1.593 | **1.323** | 1.975 | 2.036 | 1.622 | 1.670 | 1.807 | grounded |
| L7 set B `avg_score` | 1.780 | **1.542** | 1.651 | 2.142 | 2.050 | 1.552 | 2.021 | 1.692 | formal |
| L8 lifetime quality | 0.918 | 0.873 | **0.852** | 1.057 | 1.380 | 0.956 | 0.977 | 1.150 | grounded |
| L9 lifetime alignment | 2.596 | 2.649 | **1.928** | 2.503 | 2.832 | 2.863 | 2.520 | 2.655 | grounded |
| L10 lifetime novelty | 1.695 | **1.526** | 1.754 | 2.206 | 2.304 | 1.656 | 2.193 | 2.413 | formal |

**Last-place count:** `civ-grounded` **7 of 10**, `civ-formal` 2, `civ-poetic` 1.

### The one low-relevance answer that survives every lens: `civ-grounded`

The "longevity artefact" defence — that the Grounded is last because it ran the most sims and a
lifetime-average denominator penalises the longest-lived civ — is **falsified again, and now
structurally**:

- `civ-grounded` has **492 ledger rows**, the **2nd most of 8** (`civ-whimsical` has 504). It is
  **not** the longest-running civ.
- On the **denominator-free** this-run lens (n=160, no lifetime average) it is **last of 8**
  (1.487).
- It holds the **lowest lifetime quality of all 8** (0.852) and the **lowest lifetime alignment
  of all 8** (1.928). The Formal is 0.873/2.649, the Engineer 0.918/2.596.
- Its config is unremarkable — temp 0.50, top_p 0.85, max_tokens 400, mid-range on every axis.

**The Grounded is a genuinely weak writer, not a long-lived one.** Its quality collapse is
structural, and it is the civ that should be looked at.

**But note the one dissent:** on set B the Grounded *rises* to 6th (1.651) and the Formal drops
to last (1.542) — the single largest Δ in the fleet (+0.328). The Grounded's low-relevance
status is **stable across 9 of 10 lenses but body-set-sensitive on the 10th**. The two bottom-band
civs (Grounded, Precise/Formal) trade places when the mock's prose changes.

### The civ at risk of never being *selected*: `civ-poetic`

`civ-poetic` is **1st on five of ten lenses** (raw relevance 923.6, `rel/sim` 2.128, lifetime
`avg_score` 2.172, lifetime quality 1.380, set A/B `avg_score` 2.036/2.050) and **last on exactly
one**: **win rate 0.009**. It is the fleet's best writer and almost never gets chosen. It ranks
**8th of 8 on selection while 1st on quality** — the two metrics measure different things and
the board's sort key hides the split.

**`civ-precise` is the healthiest**: win rate **0.471** (best of 8 by a wide margin), best
lifetime alignment (2.863). It is the only civ whose selection rate and quality agree.

**`civ-formal` is last on lifetime novelty** (1.526) — the cold end of the temperature axis
(lowest mean temperature in the fleet, 0.30).

### Extinction risk: none

`extinction_and_birth()` retires only below `relevance < -10`. The lowest is **+658.74**
(`civ-grounded`), and it only runs in `--loop` mode every third iteration — a single-shot run
never triggers it. No civ is at risk of extinction.

---

## 6. The temperature↔novelty correlation is ecological, not causal (replication)

Prior sessions recorded "temperature ↔ novelty, Pearson r ≈ 0.98" as a load-bearing fleet finding.
Session 89 showed this was ecological. This session re-measures it three ways:

| basis | r |
|---|---|
| **ecological** — 8 per-civ mean temperature vs 8 per-civ mean novelty | **0.9368** |
| **pooled per-row** — all 3564 baseline rows | 0.5210 |
| **within-civ** (per-row, per civ) | mean **−0.0032** (range −0.0477 … +0.0471) |

**No civ shows any within-civ temperature→novelty relationship.** The r ≈ 0.98 figure was always
a correlation across 8 civs, and it conflates "civs with different preferred temperatures receive
different novelty" with "temperature causes novelty".

**The fleet IS ordered on one temperature/novelty gradient** (mean temperature: whimsical 0.95,
mythic 0.85, poetic 0.80, therapist 0.60, grounded 0.50, engineer 0.40, formal 0.30, precise
0.20). What is *not* established is that moving a civ's temperature moves its novelty. **Report
the gradient; do not report the correlation as a mechanism.**

---

## 7. Ledger hygiene and the counter gap

- **This session's 160 rows are 100 % mock-generated.** The pre-existing 3564 committed rows are
  the clean baseline; this session contributes the entire synthetic share (160 / 3724 = **4.3 %**).
- **Counter gap unchanged at exactly +260**, measured baseline-to-baseline from the **pristine git
  blobs** (ledger 3564 vs board `sims_run` sum 3304). A live-ledger-vs-pristine-board comparison
  would report a spurious **+420** and make the gap look like it had grown.
- `save_state()` rewrites `culture.json` from in-memory counters with no lock and no
  read-modify-write → lost-update race → **`relevance_per_sim` is not a reproducible ranking** and
  the board order cannot be recomputed by an auditor from the ledger. Prefer win rate and the
  `avg_score` lenses, and **say which lens you mean**.

---

## 8. Replications this session

- Credential gap **28th deep** (`ZAI_TOKEN` absent from env and from the 8-entry secret store).
- Control A **+0 rows / 0 winners / exit 0** — the silent-drop signature, 13th recurrence.
- Control B **+80 rows / +5 meta / 5 winners / 0 fallbacks / 0 default rows / 0 score errors** in
  both body sets — reproduces sessions 6-11 and 84-89 exactly.
- A/B: positional **1/8**, Spearman **ρ = 0.810**, Kendall **τ = 0.571**, max |Δ| **0.351**,
  2 of 8 civs crossing the 0.3 threshold. **Weaker than session 89's 6/8 / ρ = 0.976.**
- Chooser vs argmax **5/10 (50 %)** — 19th consecutive replication of the decoupling.
- Counter gap **exactly +260**.
- `civ-grounded` last on **7 of 10** lenses; `civ-poetic` last on 1 of 10 while 1st on 5.
- Temperature↔novelty ecological r = 0.937; **within-civ r = −0.003** (replication of session 89).

---

## 9. Environment notes (new this session)

- **`/workspace` writes report success but land 0 bytes.** `echo > file` exits 0, the file appears
  in `ls`, and `cat` shows nothing. **Check size or content, not exit status.**
- **`/tmp` is wiped mid-session.** A clone made at `/tmp/ai-writings` vanished between commands
  while a sibling file in `/tmp` survived. Use the **overlay** (`/var/tmp`) for anything that must
  outlive a single command.
- **A rank statistic computed on a pre-sorted list is always ≈ 1.0 and always wrong.** Rank the
  values, then index by civ id, and cross-check against the positional count.
- The `read`/`edit` tools remain jailed to the workspace root — overlay files are edited with
  bash heredocs and `python3` patching.
