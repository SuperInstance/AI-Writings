# Civ Orchestrator — runbook (learned across sessions 102–104)

## Paths

- The request path `/workspace/repos/ai-writings/cellular-first-design/code/civilizations`
  does **not** exist at session start (fresh sandbox, NAS 100 % full).
- Upstream owner is **`SuperInstance`**, not `ai-writings`:
  `git ls-remote https://github.com/ai-writings/cellular-first-design` →
  *Repository not found*. `SuperInstance/AI-Writings` resolves.
- The upstream repo is **3.6 GB**. Do a filtered clone to `/tmp` (overlay, ~28 GB free);
  the NAS quota does not apply to `/tmp`:

  ```bash
  export GIT_SSL_NO_VERIFY=1
  git clone --filter=blob:none --no-checkout --depth 1 \
    "https://x-access-token:$GITHUB_TOKEN@github.com/SuperInstance/AI-Writings.git" /tmp/aiw
  cd /tmp/aiw && git sparse-checkout init --cone
  git sparse-checkout set cellular-first-design && git checkout
  ```

## The NAS EDQUOT trap (workspace is 600 G/600 G, 0 bytes free)

- `cp` into `/workspace` **silently truncates every file to 0 bytes** while `ls`
  still shows them. `mkdir` still works ⇒ use a **symlink bridge**:

  ```bash
  ln -sfn /tmp/aiw/cellular-first-design \
    /workspace/repos/ai-writings/cellular-first-design
  ```

  Verify by **inode identity** (`stat -L -c '%d:%i'` → same on both sides) and `-ef`.
- **Gotcha:** the symlink must point at the `cellular-first-design` directory
  itself, NOT its parent — pointing at the parent puts `code/` one level too high
  and `CIVS_DIR` silently resolves to nothing.
- The `write`/`edit` tools are jailed to the workspace root, so `/tmp` artifacts
  need bash heredocs + `python3` patches.

## Running the orchestrator

```bash
cd /workspace/repos/ai-writings/cellular-first-design/code/civilizations
export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"   # script reads TYPESAFEAI_KEY,
                                             # sandbox stores TYPESAFE_AI_TOKEN
python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai
```

- `TYPESAFEAI_KEY` unset ⇒ JEV silently degrades to the 2.0 default and every
  score becomes a constant. Always export it.
- Run **detached** (`setsid nohup timeout -s KILL 300 … &`) and poll the output
  file — a short tool timeout kills a ~45 s run mid-flight and the report then
  records a run whose results were never captured.
- `meta_log.jsonl` `results` is a **list of `[civ_id, score]` pairs**, not a dict.
  A dict-shaped reader silently yields 0 % agreement and empty pick tallies.
  Winner fields are `winner_civ` / `winner_name`.

### Transient NAS mount races on the symlinked deep path (session 105)

`ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/`
failed intermittently with **`No such file or directory`** even though the
symlink, the target tree, and every file were present. `stat -L -c '%d:%i'`,
`readlink -f`, and `ls` on *sub*-paths all resolved to the correct inode
(`129:3671`) throughout; 10/10 retries then passed.

**A single `ls` failure is not evidence of a missing directory.** Re-check with
`stat -L` + `readlink -f` + `[-e path]` and retry before concluding the tree
is gone. Do not "fix" a working symlink by re-creating it — the bridge is fine.

### Killing the mock bridge: kill BOTH pids (session 105)

Starting the mock as `setsid nohup timeout -s KILL 400 python3 /tmp/mock_zai.py &`
creates **two** processes: the `timeout` wrapper and the real server. Killing
the wrapper PID leaves the **server still serving** (port stayed open, HTTP
200). Capture the pid of the process whose args are exactly
`python3 /tmp/mock_zai.py` — not the `timeout ...` line — and verify the port
is closed afterward (`curl` exit 7 = connection refused).

## Control B (mock provider bridge) — the override is DEAD CODE without a token

`ZAI_URL_OVERRIDE` is committed upstream, but in `call_provider()` the token
gate runs **first**:

```python
token = os.environ.get(p["env"], "")          # p["env"] == "ZAI_TOKEN"
if not token: return None                      # <-- returns HERE
_ov = os.environ.get(f"{name.upper()}_URL_OVERRIDE", "")   # never reached
```

So `ZAI_URL_OVERRIDE` **alone** produces 0 provider calls and 0 ledger rows.
Control B needs **BOTH**:

```bash
export ZAI_TOKEN="mock-local-bridge"           # any non-empty placeholder
export ZAI_URL_OVERRIDE="http://127.0.0.1:8799/api/coding/paas/v4/chat/completions"
```

The mock ignores the bearer value, so a placeholder is safe. Start it detached
and **kill it by PID from `ps`** (match `python3 /tmp/mock_zai.py` exactly) —
never `pkill -f mock_zai`, which self-matches. Verify the port is closed after.

### A mock that crashes still leaves a listening socket (session 112)

The Control B mock's seed→word derivation used `seed[i*2:i*2+2]`, which is **empty for
`i >= 4`** ⇒ `ValueError: invalid literal for int() with base 16: ''` on every request ⇒ the
bridge answered HTTP 500 and the orchestrator would have scored *nothing*. The socket stayed
open, so a naive port/200 check looked healthy.

**A 200 on a probe is not proof the mock is correct** — probe it with a payload that exercises
the same path the orchestrator uses (a long `messages[].content`, not a one-word body), and
**grep the mock's stdout for a traceback before starting the run.** Fix by wrapping the index:
`seed[(i*2)%8:((i*2)%8)+2]`.

## Verifying a run — assert on rows, never on exit code

`call_provider()` returns `None` when the token is missing, `run_simulation()`
returns `None`, and the competition short-circuits on `if not results: return
None` — **all silently, with exit code 0.** Assert on:

- per-civ `wc -l simulations.jsonl` delta (expect **+10 each** for `--sims 5`)
- `meta_log.jsonl` delta (expect **+5** for `--prompts 5`)
- the `Winner:` line count (expect **5**)

**Isolate this run's rows by count, not by `ts` cutoff.** Prior sessions left
mock rows in the ledger, so a `ts >=` filter pulls in historical rows (3360
instead of 80). Use `sorted(rows, key=ts)[-80:]` against the known pre-run total.

**Do not use preview-distinctness as a mock-integrity check.** With 5 canon
prompts × 8 voices there are only 40 distinct cultural prompts, so a salt
derived from `md5(content + len(pool))` repeats ⇒ 80 rows but 40 distinct
`content_preview`. Use the row count + the `ts` set + the `[mock-zai` prefix.

## Known structural findings

- **Credential gap:** `ZAI_TOKEN` is absent from the env and from all 8 sandbox
  secrets; all 8 return `401 token expired or incorrect` against the z.ai
  endpoint (endpoint healthy ⇒ credential gap, not an outage). JEV is live.
- **`civ-grounded` (The Grounded) is the low-relevance civ** — last on lifetime
  `avg_score` *and* lifetime `alignment`, and on both this-run counterparts.
  Alignment is the dimension the meta-GAN *selects* on, so this is structural.
  10 consecutive sessions (95–104) reproduce it. `civ-formal` is a distinct
  axis (lowest `novelty`); `civ-precise` a third (lowest `quality`, by a
  0.010 rounding-width margin — not meaningful alone).
- **`civ-poetic` is the stable inverse:** 1st on quality, last on `win_rate`.
  A *selection* failure, not a quality collapse. `civ-precise` is the other
  inverse (best `win_rate`, last `quality`).
- **Chooser vs `avg_score` argmax ≈ 15 %** — replicated 29 consecutive times.
  "Prefer win rate" is unsafe as a standalone rule: `win_rate` is a *selection*
  metric, not a quality metric.
- **Counter gap:** ledger rows exceed registry `simulations_run` by +260.
  `save_state()` rewrites `culture.json` with no lock ⇒ `relevance_per_sim` is
  **not recomputable from the ledger** by an auditor.
- **Extinction risk: NONE** (threshold −10; lowest raw relevance ≈ +707).
  Registry 8 civs, `max_civs` 12. Extinction/birth only runs under `--loop`.

### The NAS EDQUOT trap is TOTAL, not size-dependent (session 114)

Session 113 recorded "a 100-byte file also fails". The precise finding: **no write to the
NAS succeeds at all** — a 5-byte `echo` produces a **0-byte** file. The signature is a
0-byte file that `ls` still lists, with `cp` exiting 0. Do not reason about a size threshold;
`mkdir` works and the symlink bridge is the only way in. Verify the bridge by **inode
identity** (`stat -L -c '%d:%i'` on both sides), not by `ls`.

### Faster sparse fetch: single-subtree checkout (session 114)

`git clone --filter=blob:none --no-checkout` then `git checkout HEAD -- <subdir>` reaches a
single directory in seconds without downloading the repo's 3.7 GB of blobs — faster and
simpler than `sparse-checkout init/set` for one directory.

### Finding the upstream owner without `gh` (session 114)

`GET /user/repos?per_page=100&sort=updated` with `GITHUB_TOKEN` lists every repo the token
can see. `SuperInstance/AI-Writings` is the 3.7 GB one; the `ai-writings/cellular-first-design`
slug 404s. `gh` is not installed in this sandbox.

### Backgrounding from the tool shell blocks the call (session 114)

`setsid nohup ... &` **does** start the job, but the child inherits stdout so the *tool call*
does not return until the tool timeout. Redirect the child's stdout/stderr to a file and
expect the call to hang; verify the job with `ps` rather than assuming the launch failed.
Both the mock and the orchestrator ran to completion this way.

### `ps | grep <script>` self-matches the launching shell (session 114)

The shell's own command line contains the script path, so `grep` matches it too. Use
`ps -eo pid,args | awk '/mock_zai/ && !/awk/'` and match the *exact* args
(`python3 /tmp/mock_zai.py`) to find the real server pid. The `timeout` wrapper is a
separate pid — kill both.

### The `ls` race is NOT triggered by concurrency — do not chase the wrong cause (session 115)

Session 105 recorded the transient `ls` failure on the symlinked deep path. Session 115 reproduced it
(`ls -la …/code/civilizations/` → `No such file or directory` while the tree was provably present) and
then **falsified the obvious hypotheses**:

- 8 **concurrent** `ls` → 8/8 OK (not a concurrency/ordering race)
- `ls` immediately after `stat -L` → 6/6 OK (not a stat-priming effect)
- `cd` into the path then `ls` absolute → OK; trailing slash → OK; parent → OK
- 10/10 and 12/12 sequential retries → OK

The failure is **intermittent and unexplained**; the tree was always intact. **Keep the documented
diagnostic and the retry, and stop hypothesising a cause**: `stat -L -c '%d:%i'` + `readlink -f` +
`[ -e path ]` + retry. Two different tool turns in session 115 failed and then passed, and a
*later* turn in the same session failed again after a clean run — so "it worked last time" is not
evidence the tree exists.

### Competition-phase rows: per-civ Δ is +10, not +45 (session 115)

Reading the code suggests 5 sims + 5 competitions × 8 civs = 45 rows per civ. The **actual** ledger
delta is **+10 per civ** (80 total). Reason: the competition phase runs 8 civs in parallel but
`run_simulation()` appends **one row per civ per prompt** — 5 prompts → 5 rows per civ, and the
8 civs' rows are spread across the 8 ledgers (not 8 rows each). So per civ:
**5 (sim phase) + 5 (one per competition prompt) = 10**. Total = 8 × 10 = 80.

Corollary for isolating a run's rows: the competition phase is a **separate ts cluster** ~20 s after
the sim phase. A `ts >` cutoff drawn in the wrong place will attribute competition rows to the wrong
cluster — count from the end of the file (`rows[-delta:]`) instead.

### Control B mock: the index-wrap fix, verified (session 115)

Rewrote `/tmp/mock_zai.py` with `seed[(i*2)%8:((i*2)%8)+2]` (the session-112 fix). Verified before
the run with the **exact long multi-sentence cultural prompt** the orchestrator sends (not a one-word
body): HTTP 200, 210-char body, `[mock-zai seed=…]` prefix present, **0 tracebacks** in stdout.
All 80 ledger rows carried the prefix ⇒ mock integrity confirmed at the ledger level, not just the
socket level.

`ZAI_URL_OVERRIDE` alone is still dead code — the token gate returns `None` first. Control B needs
**both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE`.

### JEV liveness check: HTTP 422 means auth OK, not down (session 115)

Probing JEV with a string where `questions` expects an object returns
`422 {"type":"model_attributes_type"}` — a **payload-shape** complaint, which means the token was
accepted. Do not read 422 as "JEV unreachable"; it is proof of liveness. (Contrast z.ai, where 401
on a bogus token means the endpoint is healthy but the credential is absent.)

### `gh` is not installed; list repos with the REST API (session 115, re-confirmed)

`GET /user/repos?per_page=100&sort=updated` with `GITHUB_TOKEN` lists every repo the token can see.
The 3.7 GB upstream is **`SuperInstance/AI-Writings`**; the `ai-writings/cellular-first-design`
slug 404s. A `--depth 50` full clone of that repo pulled only 4.4 MB for this subtree — no
`--filter=blob:none` needed when the tree is small, so prefer the simple clone.

### The symlink gotcha has TWO directions — don't flatten the clone (session 115)

The RUNBOOK says the symlink "must point at the `cellular-first-design` directory itself, NOT its
parent". Session 115 hit the **mirror-image** trap: the clone of `SuperInstance/AI-Writings` has the
tree at **`<repo-root>/cellular-first-design/code/civilizations/`**, and the repo root *is* the
`cellular-first-design` directory. Flattening the extra nesting level (to make `code/` sit at the
repo root) looks tidy but then:

- `git status` shows every file as `D` (deleted) + untracked, because the tracked paths still have
  the `cellular-first-design/` prefix;
- `git clean -fd` then **destroys the flattened copy** and silently reverts to the pre-run baseline;
- the symlink (still pointing at the repo root) resolves `code/` **one level too deep** ⇒
  `CIVS_DIR` finds nothing and `ls` fails *consistently* (5/5), unlike the transient race.

**Do not flatten.** Clone, leave the tree nested, and point the symlink at
`<clone-root>/cellular-first-design` (the nested dir), verified by
`stat -L -c '%d:%i'` == `stat -c '%d:%i'` on the nested target and `-ef`. If a flattening has already
happened, `git checkout -- .` restores the baseline but **discards the run's outputs** — copy them
out first, then restore, then copy back into the *nested* path and `git add` that path.

Symptom triage: `ls` failing **5/5 in a row** (not intermittently) after a restructure means a
*wrong symlink target*, not the transient mount race. Re-run the inode check before touching the
bridge.

### Session 116 — re-confirmations and one new observation

- **NAS EDQUOT still total (3rd session running).** `git clone` directly into
  `/workspace/repos/...` dies with `Disk quota exceeded`; only the symlink bridge works. Target
  must be the **nested** `cellular-first-design` dir.
- **A plain `git clone --filter=blob:none` of `SuperInstance/AI-Writings` into `/tmp` checks out the
  whole tree fine.** The civ subtree is small; the `sparse-checkout init/set` dance is unnecessary.
  (`/tmp` = overlay, ~28 G free; the NAS quota does not apply.)
- **`gh` is not installed** — 3rd session running. `GET /user/repos?per_page=100` and
  `GET /search/repositories?q=…` with `GITHUB_TOKEN` both work for locating upstream. The API is
  case-insensitive: `SuperInstance/ai-writings` and `SuperInstance/AI-Writings` are the same repo.
- **Tool-call timeout is 30 s**, shorter than the ~45 s orchestrator run. Launch detached with
  stdout redirected to a file, then poll `ps` + the log. The launch call itself returns fine.

**New: the chooser can pick the LOWEST-scoring candidate.** In session 116's "witness log"
competition, `civ-grounded` won with `avg_score` 0.040 while the field's top was 0.533
(`civ-precise`). The meta-GAN chooser scores the *text* via JEV; it does not read `avg_score`.
So `win_rate` and `avg_score` are genuinely different signals, and a low-scoring civ can still
take a competition. This strengthens the standing rule: **never treat `win_rate` as a quality
metric** — measure quality on `avg_score` / lifetime score dims instead.

**Verification pattern that held (re-confirmed 116):** per-civ Δ = **+10** for `--sims 5`
(5 sim-phase + 5 competition-phase rows), `meta_log.jsonl` Δ = **+5**, `Winner:` lines = **5**,
and 80/80 new rows carry the `[mock-zai]` prefix with `provider=zai` and **no `error` key** in
`scores` (the no-error check is what proves JEV really scored rather than silently returning
the 2.0 default).

### Session 117 — the mock's seed ignores the civ ⇒ the chooser CANNOT discriminate

**New, verified, and it invalidates the competition results of any Control B run.**

The mock derives its response seed from `re.sub(r"[^a-zA-Z0-9]", "", msg)[:8]` — the **first
8 alphanumeric characters** of the cultural prompt. But the cultural prompt begins with the
**civ-invariant** prefix:

```
You are a voice in the tradition of "<CIV NAME>".   <-- differs
Your tenets: ...                                     <-- differs
Your voice: ...                                      <-- differs
```

The first 8 alphanumeric chars of that whole string are `YouAreA` for **every civ**. So the
seed is `youareav` regardless of civ.

**Consequence (measured, not inferred):** in the competition phase all 8 civs'
`content_preview` is **byte-identical** — one distinct preview per civ, and the *same* preview
across all 8 civs on all 5 prompts. JEV's chooser receives 8 copies of one string and must
break a perfect tie. Session 117's "civ-precise won 5/5" is **an arbitrary tie-break landing
on one civ, NOT a quality signal.**

**Rules that follow:**

- **A Control B run's competition ordering and the `avg_score` spread are NOT quality
  measurements.** The spread is JEV scoring identical text 8× — residual differences are JEV
  nondeterminism. Label every Control B report as *mock-limited*.
- **Only the lifetime leaderboard columns are trustworthy** in a Control B run.
- Session 116's finding (the chooser picked the *lowest*-scoring candidate) is **not
  refuted** by session 117 — it simply **cannot be re-tested** under the current mock.
- **The fix (not yet applied):** seed from a hash of the *whole* message, or from a hash of
  the civ-specific fields only (`voice_emphasis` + `tenets` + prompt), not the leading
  prefix. Then each civ emits distinct text and the chooser becomes a real test again.
- **Diagnostic to run after any mock change:** for one competition prompt, assert
  `len({r["content_preview"] for r in new_competition_rows}) == 8`. If it is 1, the mock is
  degenerate and the run's competition results are void.

### Session 117 — re-confirmations

- **NAS EDQUOT still total (4th session running).** `git clone` into `/workspace/repos/...`
  dies with `Disk quota exceeded`; only the symlink bridge works. Target = the **nested**
  `cellular-first-design` dir. Verified by `stat -L -c '%d:%i'` on both sides + `-ef`.
- **The `ls` race on the symlinked deep path reproduced once** in session 117 (one `ls` →
  `No such file or directory`), then 5/5 retries OK and `stat -L`/`readlink -f`/`[-e]` all
  correct. Unchanged guidance: **a single `ls` failure is not evidence of a missing
  directory**; re-check and retry before touching the bridge.
- **`gh` is not installed — 4th session running.** `GET /search/repositories?q=ai-writings`
  with `GITHUB_TOKEN` works; the API is case-insensitive
  (`SuperInstance/ai-writings` == `SuperInstance/AI-Writings`).
- **Tool timeout (30 s) < orchestrator run (~45 s).** Launch detached with stdout redirected
  to a file, then poll `ps` + the log.
- **Verification pattern held again:** per-civ Δ = **+10** (5 sim-phase + 5
  competition-phase), `meta_log.jsonl` Δ = **+5**, `Winner:` lines = **5**, 80/80 rows with
  the `[mock-zai]` prefix, **0** rows with a JEV `error` key.
- **The sim→competition ts gap sits at index 4** in every civ file (4.2 s–22.9 s observed) —
  a cheap structural check that both phases landed.
- **`civ-grounded` (The Grounded) remains the low-relevance civ** — last on lifetime
  `avg_score` (1.332), `alignment` (1.638), `quality` (0.675), `relevance` (797.20) and
  `relevance_per_sim` (1.288). 22+ sessions reproduce it. Extinction risk **NONE**
  (threshold −10, lowest raw relevance +797.20, 80× above). Counter gap **+260**, unchanged.

### Session 118 — the session-117 degeneracy is FIXED; chooser-vs-argmax is 0 % (2026-10-24)

**The fix (applied).** The mock now seeds from `md5(whole_message)[:8]` instead of the first 8
alnum chars of the message. The civ-specific fields (name, tenets, voice) enter the hash, so
each civ emits distinct text. The mock lives at `/tmp/mock_zai.py`; keep the session-112
index-wrap `seed[(i*2)%8:((i*2)%8)+2]` (a plain `seed[i*2:i*2+2]` crashes on `i>=4`).

**The diagnostic that must pass before you trust any competition result:**

```python
# for ONE competition prompt, across the 8 civs
assert len({r["content_preview"] for r in new_competition_rows}) == 8
```

If it is 1, the mock is degenerate and the run's competition ordering and `avg_score` spread
are **void**. Measured this session: **8/8 on all 5 prompts, 40/40 across the run** — the
first clean measurement in the fleet's history.

**Why this matters for the fleet's standing numbers:** every "chooser vs `avg_score` argmax
≈ 15 %, replicated 29 consecutive times" measurement was taken under the degenerate mock,
where the chooser was breaking a tie among 8 identical strings. **Session 118's clean value is
0/5 (0 %)** — the chooser disagreed with the argmax in every competition, and `civ-poetic` was
argmax in 3/5 and near-argmax in a 4th while winning **zero**. Treat the historical 15 % as
void and 0 % as the current measurement.

**Session 116's "the chooser picked the lowest-scoring candidate" is re-confirmed** under the
working mock (winners at `avg_score` 0.077 and 0.217 against argmaxes 0.583 and 0.457). It is
no longer a mock artifact.

**Still-true standing findings after the fix:**

- **`civ-grounded` (The Grounded) is the low-relevance civ** — last on lifetime `relevance`
  (799.55), `relevance_per_sim` (1.271), `avg_score` (1.315), `quality` (0.665) and
  `alignment` (1.616). The **alignment** gap is the structural one: 0.417 below the next civ,
  versus a 0.037 margin on quality. `alignment` is the dimension the meta-GAN selects on, so
  the civ fails to *embody a distinctive voice*, not merely to write well. 23 sessions (95–118).
- **`civ-formal` is the low-novelty axis** (novelty 1.475, lowest; alignment 2.298, fine).
- **The two stable inverses:** `civ-poetic` = 1st on quality (1.126) / `avg_score` (1.947) but
  last on `win_rate` (0.017) and won 0/5; `civ-precise` = best `win_rate` (0.490) but 5th on
  `avg_score` (1.648).
- **Extinction risk NONE** — threshold −10, lowest relevance +799.55 (81× above floor).
  Registry 8, `max_civs` 12. Extinction/birth only under `--loop`.
- **Counter gap is per-civ uneven**, not a uniform offset: civ-whimsical +63, civ-grounded
  +43, civ-formal +42, civ-poetic +37, civ-engineer +22, civ-mythic +20, civ-therapist +17,
  civ-precise +16. `save_state()` has no lock ⇒ `relevance_per_sim` is not recomputable from
  the ledger by an auditor.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs** (not a dict). A
  dict-shaped reader silently yields 0 % agreement and empty pick tallies.
- **Re-confirmations:** NAS EDQUOT total (5th session); `gh` not installed (5th session);
  tool timeout 30 s < run ~45 s; `ZAI_URL_OVERRIDE` alone is dead code (needs `ZAI_TOKEN`);
  clone into `/tmp`, symlink the **nested** `cellular-first-design` dir, verify with
  `stat -L -c '%d:%i'` + `-ef`; never flatten.
- **Verification pattern held:** per-civ Δ = **+10** (5 sim + 5 competition), `meta_log` Δ =
  **+5**, `Winner:` lines = **5**, 80/80 rows with the `[mock-zai` prefix, **0** rows with a
  JEV `error` key.

### Session 120 — quality collapse did NOT reproduce; the ls race is not a trailing-slash issue (2026-10-24)

**The session-119 "quality collapse" is downgraded from a run property to a possible one-off.**
Session 119 measured `quality` at 0.009–0.030 for every civ (spread 0.021). This session
measured **0.106–0.446 (spread 0.340)** — a ~10× higher level and a 16× wider spread, under
the *same* mock. Session 119's durable rule survives and is re-confirmed
(*compare cross-civ spreads, not absolute levels, before ranking on a dimension*), but the
*collapse itself* is not a stable property of the mock. `alignment` again carried the widest
spread (1.043 vs quality 0.340, novelty 0.326) and is again the axis the chooser selects on.

**Chooser vs `avg_score` argmax across the three clean-mock sessions: 0/5 (118) → 3/5 (119)
→ 1/5 (120).** All 5-sample points — the honest claim is *somewhere in 0–60 %, no single run
can say which*. What survives all three: the chooser is **not** a pure argmax, and in all 4
disagreements this session it picked a **lower**-scoring candidate (4th consecutive session:
116/118/119/120).

**Mock non-degeneracy: 40/40 across the run** (8/8 distinct previews on every one of the 5
prompts) — the second clean measurement in the fleet's history, so session 120's competition
results and `avg_score` spread are **real measurements**, not tie-breaks.

**NEW: the `ls` race on the symlinked deep path is NOT a trailing-slash issue.** This session
`ls -la <path>` failed 2/2 and `ls -la <path>/` failed 2/2, then both variants passed 20/20
on retry. The trailing slash is not the trigger and there is still no explanation. Diagnostic
remains inode identity + `readlink -f` + `[-e]` + retry. **Refine the triage:** the
session-115 signature for a *wrong symlink target* is a **consistent 5/5 failure**; an
intermittent 2/2-then-20/20 pattern is the **race**, not a broken bridge. Do not
"fix" a bridge that is passing 20/20.

**Mock pre-flight improvement:** assert **two different civs ⇒ two different seeds** against
the live mock *before* launching the batch. It is a 3-second check that prevents a broken
mock from ever reaching the ledger, instead of discovering it afterwards in the rows.

**`civ-grounded` (The Grounded) remains the low-relevance civ** — 25 consecutive sessions
(95–120). Last on lifetime `avg_score` (1.2925), `alignment` (1.5820), `quality` (0.6477),
`relevance` (810.06) and `relevance_per_sim` (1.248). **The structural gap is `alignment`:
0.408 below the next civ (1.582 vs 1.990), versus 0.035 on quality.** The meta-GAN selects
on alignment, so Grounded fails to *embody a distinctive voice* — a voice failure, not a prose
failure. It is 2nd worst on this run's `alignment` too.

**New axis to watch: `civ-engineer`** was last on this run's `avg_score` (0.8597), `quality`
(0.106) and `alignment` (0.803) — but is only 6th of 8 on lifetime `relevance_per_sim`
(1.461). A single-run low, not yet a trend; it would become a finding if it repeats.

- **`civ-formal`** is the low-novelty axis (lifetime novelty 1.4652, last; alignment 2.2499
  healthy). **`civ-poetic`** = 1st on lifetime avg_score (1.9173) / quality (1.0997) /
  alignment (2.5378) / relevance_per_sim (1.876) but **last** on win_rate (0.016) and won
  0/5 (argmax in 2/5) — the stable selection-failure inverse. **`civ-precise`** = best
  win_rate (0.500), 4/5 wins, 6th on lifetime avg_score — the mirror inverse.
- **Extinction risk NONE** — threshold −10, lowest relevance +810.06 (81× above floor).
  Registry 8, `max_civs` 12. Extinction/birth only under `--loop`.
- **Counter gap per-civ uneven, unchanged**: whimsical +63, grounded +43, formal +42,
  poetic +37, engineer +22, mythic +20, therapist +17, precise +16. `save_state()` has no
  lock ⇒ `relevance_per_sim` is not recomputable from the ledger by an auditor.
- **Re-confirmations:** NAS EDQUOT total (6th session); `gh` not installed (7th session);
  tool timeout 30 s < run ~45 s; `ZAI_URL_OVERRIDE` alone is dead code (needs `ZAI_TOKEN`);
  clone into `/tmp`, symlink the **nested** `cellular-first-design` dir, verify with
  `stat -L -c '%d:%i'` + `-ef`; never flatten; `TYPESAFEAI_KEY` must be exported.
- **Verification pattern held:** per-civ Δ = **+10** (5 sim + 5 competition), `meta_log` Δ =
  **+5**, `Winner:` lines = **5**, 80/80 rows with the `[mock-zai` prefix, **0** rows with a
  JEV `error` key, sim→competition ts gap at index 4 in all 8 civs.

### Session 121 — the quality axis is a LEVEL, not a property; chooser-vs-argmax is 4/5 (2026-10-24)

**Mock rebuilt from scratch** (this session's `/tmp` was wiped), so the session-112 index-wrap
bug was live again. The **pre-flight probe saved the run**: assert 3 different civs → 3
different seeds against the *live* mock with the exact long cultural prompt, and
`grep -c Traceback /tmp/mock_zai.log` → **0**, *before* launching the batch. A crashing mock
still leaves a listening socket, so a port/200 probe looks healthy — this is the one check
that cannot be skipped after a rebuild.

**Verification held:** per-civ Δ = **+10** (5 sim + 5 competition), `meta_log` Δ = **+5**,
`Winner:` lines = **5**, **80/80** rows with the `[mock-zai` prefix, **0** rows with a JEV
`error` key, sim→competition ts gap at index 4 in all 8 civs (1.08 s–22.74 s), and
**5/5 competition prompts at 8/8 distinct previews** — the third clean mock measurement
(118, 120, 121).

**NEW — the quality collapse is a LEVEL, not a property of the mock.** Session 119 measured
`quality` at 0.009–0.030; session 120 at 0.106–0.446; **session 121 back at 0.010–0.37
(mean 0.0193)** — under the *same* mock, which was **rebuilt**, not reused. So the collapse
is **not** a stable property; it is a level that moves. The durable rule survives and is
re-confirmed: **compare cross-civ spreads, not absolute levels, before ranking on a
dimension.** `alignment` again carried the widest spread (per-prompt 0.96–2.82) and is again
the axis the chooser selects on.

**Chooser vs `avg_score` argmax: 4/5 (80 %).** `civ-precise` was argmax in **5/5** and won
**4/5**; `civ-formal` won the one it lost (argmax was still `civ-precise` at 1.73). The
clean-mock series is now **0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121)**. Five-sample
points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*. What survives every
session: the chooser is **not** a pure argmax, and in all 4 disagreements across
116/118/119/120 it picked a **lower**-scoring candidate.

**`civ-grounded` (The Grounded) remains the low-relevance civ** — 26 consecutive sessions
(95–121). Last on lifetime `avg_score` (1.2794), `alignment` (1.5600), `quality` (0.6386),
`relevance` (813.83) and `relevance_per_sim` (1.2350). **The structural gap is `alignment`:
0.3995 below the next civ (1.5600 vs 1.9596), versus 0.0348 on quality.** Alignment is the
dimension the meta-GAN selects on, so Grounded fails to *embody a distinctive voice* — a
voice failure, not a prose failure. `civ-formal` remains the low-**novelty** axis (1.4673).
`civ-poetic` = 1st on `avg_score` (1.8993) / `quality` (1.0838) but last on `win_rate` (0.016),
won 0/5. `civ-precise` = best `win_rate` (0.505), won 4/5, 1st on lifetime `alignment`
(2.5209), 3rd on `avg_score` (1.6487) — the mirror inverse.

**New watch-axis:** `civ-engineer` was last on this run's `avg_score` (0.5853) and `alignment`
(0.262) but 6th of 8 on lifetime `relevance_per_sim` (1.4480) — a single-run low, not a trend.

- **Extinction risk NONE** — threshold −10, lowest relevance +813.83 (81× above floor).
  Registry 8, `max_civs` 12. All 8 civs still `generation=1`.
- **Counter gap per-civ uneven, unchanged**: whimsical +63, grounded +43, formal +42,
  poetic +37, engineer +22, mythic +20, therapist +17, precise +16.
- **Re-confirmations:** NAS EDQUOT total (7th session); `gh` not installed (8th session);
  tool timeout 30 s < run ~50 s; `ZAI_URL_OVERRIDE` alone is dead code (needs `ZAI_TOKEN`);
  clone into `/tmp`, symlink the **nested** `cellular-first-design` dir, verify with
  `stat -L -c '%d:%i'` + `-ef`; never flatten; `TYPESAFEAI_KEY` must be exported.

### Gotcha: `civilizations.json` is multi-line JSON, not JSONL (session 121)

`json.loads(l)` over the lines of `civilizations.json` raises `JSONDecodeError: line 2
column 1` — the file is a pretty-printed array. Use `json.loads(open(...).read())`. The civ
ledgers (`simulations.jsonl`) *are* JSONL and parse fine, so the error looks like ledger
corruption when it is not — it cost a debugging cycle this session.

### Session 122 — the quality collapse is civ-selective; chooser-vs-argmax is 4/5 (2026-10-24)

**Mock rebuilt from scratch again** (this session's `/tmp` was wiped), so the session-112
index-wrap bug was live again. The **pre-flight probe saved the run again**: 3 different civs
→ 3 different seeds against the *live* mock with the exact long cultural prompt, HTTP 200,
158-char bodies, `[mock-zai seed=…]` prefix present, **0 tracebacks** in `/tmp/mock_zai.log`,
*before* launching the batch.

**Verification held:** per-civ Δ = **+10** (5 sim + 5 competition), `meta_log` Δ = **+5**,
`Winner:` lines = **5**, **80/80** rows with the `[mock-zai` prefix, **0** rows with a JEV
`error` key, sim→competition ts gap at index 4 in all 8 civs (2.46 s–2.62 s), and
**5/5 competition prompts at 8/8 distinct previews** — the **fourth clean mock measurement**
(118, 120, 121, 122).

**NEW — the quality collapse is CIV-SELECTIVE, not a uniform field-wide floor.** This run's
`quality` was again collapsed (mean 0.0214, min 0.010, max 0.290) — the third session in that
regime (119, 121, 122) against session-120's 0.106–0.446 — but the floor is **not** uniform
across the field:

- `civ-precise` — `quality` **0.068**, `alignment` **1.631** (the only civ off the floor on
  either dimension; the other seven sat at `quality` 0.010–0.022 and `alignment` 0.023–0.388).
- the other seven civs — collapsed together.

So "the run collapsed" is a **weaker** claim than "**7 of 8 civs** collapsed". The durable rule
survives and is re-confirmed: **compare cross-civ spreads, not absolute levels, before ranking
on a dimension** — and, sharpened this session, **check the floor per-civ before declaring a
field-wide level**. `alignment` again carried the widest spread (2.790 vs quality 0.280,
novelty 1.190) and is again the axis the chooser selects on.

**Chooser vs `avg_score` argmax: 4/5 (80 %).** `civ-precise` was argmax in **5/5** and won
**4/5**; `civ-formal` won the one it lost (argmax was still `civ-precise` at 1.707 vs the
winner's 0.910). The clean-mock series is now **0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121)
→ 4/5 (122)**. Five-sample points cannot narrow a rate — the honest claim is *somewhere in
0–80 %*. What survives every session: the chooser is **not** a pure argmax, and in all 5
disagreements across 116/118/119/120/122 it picked a **lower**-scoring candidate.

**`civ-grounded` (The Grounded) remains the low-relevance civ** — **27 consecutive sessions
(95–122)**. Last on lifetime `avg_score` (1.2673), `alignment` (1.5388), `quality` (0.6298),
`relevance` (817.94) and `relevance_per_sim` (1.2230); **last on every dimension of this run**
(avg 0.4110, alignment 0.048, quality 0.010). The structural gap is `alignment`: **0.3916**
below the next civ (1.5388 vs 1.9304), versus **0.0343** on quality. Alignment is the dimension
the meta-GAN selects on, so Grounded fails to *embody a distinctive voice* — a voice failure,
not a prose failure. `civ-formal` remains the low-**novelty** axis (1.4708). `civ-poetic` =
1st on `avg_score` (1.8821) / `quality` (1.0684) / `novelty` (2.1086) but last on `win_rate`
(0.015), won 0/5. `civ-precise` = best `win_rate` (0.509), won 4/5, 1st on lifetime
`alignment` (2.5074), 6th on `avg_score` (1.6131) — the mirror inverse.

**Watch-axis `civ-engineer` — the session-121 low did NOT repeat.** Engineer was 4th of 8 on
this run's `avg_score` (0.6230) and 2nd-lowest on `alignment` (0.386) but no longer last; it
stays 6th of 8 on lifetime `relevance_per_sim` (1.4350). **One more session at the bottom
would make it a trend** — do not promote it to a finding yet.

- **Extinction risk NONE** — threshold −10, lowest relevance +817.94 (82× above floor).
  Registry 8, `max_civs` 12. All 8 civs still `generation=1`.
- **Counter gap per-civ uneven, unchanged**: whimsical +63, grounded +43, formal +42,
  poetic +37, engineer +22, mythic +20, therapist +17, precise +16. `save_state()` has no
  lock ⇒ `relevance_per_sim` is not recomputable from the ledger by an auditor.
- **Re-confirmations:** NAS EDQUOT total (8th session); `gh` not installed (9th session);
  tool timeout 30 s < run ~50 s; `ZAI_URL_OVERRIDE` alone is dead code (needs `ZAI_TOKEN`);
  clone into `/tmp`, symlink the **nested** `cellular-first-design` dir, verify with
  `stat -L -c '%d:%i'` + `-ef`; never flatten; `TYPESAFEAI_KEY` must be exported.

### Session 123 — chooser-vs-argmax is 3/5; the chooser picked the LOWEST-scoring candidate (2026-10-24)

**Mock rebuilt from scratch again** (this session's `/tmp` was wiped), so the session-112
index-wrap bug was live again. The **pre-flight probe saved the run a third time**: 4 different
civs → 4 different seeds AND 4 different previews against the *live* mock with the exact long
cultural prompt, `[mock-zai seed=…]` prefix present, HTTP 200, **0 tracebacks** in
`/tmp/mock_zai.log`, *before* launching the batch.

**Verification held:** per-civ Δ = **+10** (5 sim + 5 competition), `meta_log` Δ = **+5**,
`Winner:` lines = **5**, **80/80** rows with the `[mock-zai` prefix, `provider={zai}`,
**0** rows with a JEV `error` key, sim→competition ts gap at index 4 in all 8 civs
(1.15 s–23.28 s), and **5/5 competition prompts at 8/8 distinct previews** — the **fifth
clean mock measurement** (118, 120, 121, 122, 123).

**NEW — the chooser picked the LOWEST-scoring candidate on p1.** `civ-poetic` argmaxed at
**0.790**; `civ-grounded` won at **0.163**, the lowest score on the field. `civ-grounded` is
also the fleet's lowest-relevance civ, so this is the session-116 finding in its strongest
form yet: **a competition win is not evidence of relevance.** The chooser reads the *text* via
JEV, not `avg_score`.

**Chooser vs `avg_score` argmax: 3/5 (60 %).** Clean-mock series:
0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → **3/5 (123)**.
Six five-sample points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*.
What survives every session: the chooser is **not** a pure argmax, and in **both**
disagreements this session it picked a **lower**-scoring candidate.

**`civ-grounded` (The Grounded) remains the low-relevance civ** — **28 consecutive sessions
(95–123)**. Last on lifetime `avg_score` (1.2525), `alignment` (1.5184), `quality` (0.6212),
`relevance` (819.94) and `relevance_per_sim` (1.208). The **structural gap is `alignment`:
0.650 below the next civ (1.5184 vs 2.1684)**, versus **0.034** on quality — 19× wider.
Alignment is the dimension the meta-GAN selects on, so Grounded fails to *embody a distinctive
voice* — a voice failure, not a prose failure. It was last on every axis of this run too
(avg 0.2000, alignment 0.0670, quality 0.0100). `civ-formal` remains the low-**novelty** axis
(1.4619). `civ-poetic` = 1st on lifetime avg_score (1.8672) / quality (1.0538) / novelty
(2.0894) but **last** on win_rate (0.015, 5/323) and won **0/5** despite argmaxing p1 and p2 —
the stable selection-failure inverse. `civ-precise` = best win_rate (0.514, 166/157), won 4/5,
3rd of 8 on lifetime avg_score — the mirror inverse.

**NEW watch-axis `civ-therapist`:** 2nd-lowest on this run's `alignment` (**0.0420**) — the
*lowest* alignment in the field, below `civ-grounded`'s 0.0670. Lifetime alignment 1.9024 is
mid-field, so this is a single-run low, not a second axis yet. Watch it.

**Watch-axis `civ-engineer` — the session-121 low did NOT repeat for a second time.** 5th of 8
on this run's `avg_score` (0.2923), 2nd-lowest on `alignment` (0.2510), 6th of 8 on lifetime
`relevance_per_sim` (1.417). **One more session at the bottom would make it a trend** — do
not promote it to a finding yet.

- **Extinction risk NONE** — threshold −10, lowest relevance +819.94 (82× above floor).
  Registry 8, `max_civs` 12. All 8 civs still `generation=1`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` 2.320,
  `novelty` 0.870, `quality` 0.080. `alignment` again carried the widest spread and is again
  the axis the chooser selects on. `quality` again collapsed (mean 0.017) — the 119/121/122
  regime vs session-120's 0.106–0.446. **The quality collapse is a LEVEL that moves, not a
  stable property** — compare cross-civ spreads before ranking on a dimension.
- **Counter gap per-civ uneven, unchanged**: whimsical +63, grounded +43, formal +42,
  poetic +37, engineer +22, mythic +20, therapist +17, precise +16. `save_state()` has
  no lock ⇒ `relevance_per_sim` is not recomputable from the ledger by an auditor.
- **Re-confirmations:** NAS EDQUOT total (9th session); `gh` not installed (10th session);
  tool timeout 30 s < run ~50 s; `ZAI_URL_OVERRIDE` alone is dead code (needs `ZAI_TOKEN`);
  clone into `/tmp`, symlink the **nested** `cellular-first-design` dir, verify with
  `stat -L -c '%d:%i'` + `-ef`; never flatten; `TYPESAFEAI_KEY` must be exported.
- **NEW — a `setsid nohup … &` launch whose child inherits stdout BLOCKS the tool call**
  until the tool timeout (30 s), even though the job starts correctly. Redirect the child's
  stdout/stderr to a file **and** `< /dev/null`, and expect the launch call to hang anyway;
  verify the job with `ps` rather than assuming the launch failed. (Distinct from the
  session-114 note, where the redirect alone was enough — adding `< /dev/null` is harmless.)
- **NEW — grouping this run's rows by `r["prompt"]` is WRONG for the non-degeneracy check.**
  `prompt` is truncated to 80 chars and the *sim phase* reuses the same 5 canon prompts, so
  grouping by prompt yields 16 rows per prompt, not 8, and a naive "exactly 8 rows" filter
  returns **0 competition prompts** and a false FAIL. Group by the **per-civ slot index**
  (`rows[-10:][5..9]` for the competition phase, `[0..4]` for the sim phase) — that aligns the
  8 civs' rows for the same prompt without relying on the truncated prompt string.

### Session 125 — chooser-vs-argmax is 4/5; the mock is non-degenerate for the 7th time (2026-10-24)

**Mock rebuilt from scratch again** (this session's `/tmp` was wiped), so the session-112 index-wrap bug
(`seed[i*2:i*2+2]` → empty for `i>=4` → HTTP 500 while the socket stays open) was live again. The
**pre-flight probe caught it before it reached the ledger**: 4 different civs → 4 different seeds AND
4 different previews against the *live* mock with the exact long cultural prompt, HTTP 200,
`[mock-zai seed=…]` prefix present on every body, `grep -c Traceback /tmp/mock_zai.log` → **0**.

**Verification held:** per-civ Δ = **+10** (5 sim-phase + 5 competition-phase), `meta_log` Δ = **+5**,
`Winner:` lines = **5**, **80/80** rows with the `[mock-zai` prefix, `provider={zai}`,
**0** rows with a JEV `error` key, sim→competition ts gap at index 4 in all 8 civs (1.10 s–22.96 s),
and **5/5 competition prompts at 8/8 distinct previews** — the **seventh clean mock measurement**
(118, 120, 121, 122, 123, 124, 125).

**Chooser vs `avg_score` argmax: 4/5 (80 %).** `civ-precise` was argmax in 4/5 and won **5/5**;
`civ-poetic` argmaxed p4 at 0.680 and lost to `civ-precise` at 0.647. Clean-mock series:
0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) → **4/5 (125)**.
Eight five-sample points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*. What
survives every session: the chooser is **not** a pure argmax, and in **all 6** disagreements across
116/118/119/120/122/123/125 it picked a **lower**-scoring candidate.

**NEW — the 0/5 → 4/5 swing between consecutive sessions on the same mock and scorer shows a
5-sample point carries almost no information about a rate.** Only the *direction* of the
disagreements (always the lower scorer) is stable. Do not promote a single session's fraction to
a fleet claim; report it as a sample, and report the direction as the finding.

**`civ-grounded` (The Grounded) remains the low-relevance civ** — **30 consecutive sessions
(95–125)**. Last on lifetime `avg_score` (1.2378), `alignment` (1.4906), `quality` (0.6064),
`relevance` (834.13) and `relevance_per_sim` (1.193). **The structural gap is `alignment`:
0.3700 below the next civ (1.4906 vs 1.8606)**, versus **0.0334** on quality — 11× wider.
Alignment is the dimension the meta-GAN selects on, so Grounded fails to *embody a distinctive
voice* — a voice failure, not a prose failure. It was last on this run's `avg_score` (0.4750) and
`novelty` (1.3890) too. `civ-formal` remains the low-**novelty** axis (1.4696).
`civ-poetic` = 1st on lifetime `avg_score` (1.8456) / `quality` (1.0335) but last on `win_rate`
(0.015), won 0/5. `civ-precise` = best `win_rate` (0.523), won 5/5, 1st on lifetime `alignment`
(2.4562), 5th of 8 on `avg_score` — the mirror inverse.

**Watch-axis `civ-therapist` — the two-session lifetime signal did NOT extend, but the run-level
low did.** Therapist was last on this run's `avg_score` (0.4907) and lowest on this run's
`alignment` (0.0210, below `civ-grounded`'s 0.0270) — so the *run-level* label flipped to
therapist — but its **lifetime** alignment rose to 1.8606 (2nd-lowest of 8). The axis stays open;
do not promote it to a finding.

**Watch-axis `civ-engineer` — the session-121 low did NOT repeat for a third time.** 7th of 8 on
this run's `avg_score` (0.5180), 6th on lifetime `relevance_per_sim` (1.398). **One more session at
the bottom would make it a trend** — do not promote it to a finding yet.

- **Extinction risk NONE** — threshold −10, lowest relevance +834.13 (83× above floor).
  Registry 8, `max_civs` 12. All 8 civs still `generation=1`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` 0.548,
  `novelty` 0.262, `avg_score` 0.230, `quality` 0.004. `alignment` again carried the widest
  spread and is again the axis the chooser selects on. `quality` again collapsed (field mean
  0.0100, min 0.008, max 0.012) — the 119/121/122/123 regime vs session-124's 0.337 and
  session-120's 0.106–0.446. **The quality collapse is a LEVEL that moves, not a stable
  property** — compare cross-civ spreads before ranking on a dimension. Per-civ quality floors
  were uneven again (poetic 0.012 … mythic 0.008) — the session-122 civ-selective floor.
- **Counter gap per-civ uneven, unchanged**: whimsical +63, grounded +43, formal +42,
  poetic +37, engineer +22, mythic +20, therapist +17, precise +16 (total +260).
  `save_state()` has no lock ⇒ `relevance_per_sim` is not recomputable from the ledger by an auditor.
- **Re-confirmations:** NAS EDQUOT total (10th session); `gh` not installed (12th session);
  tool timeout 30 s < run ~45 s; `ZAI_URL_OVERRIDE` alone is dead code (needs `ZAI_TOKEN`);
  clone into `/tmp`, symlink the **nested** `cellular-first-design` dir, verify with
  `stat -L -c '%d:%i'` + `-ef`; never flatten; `TYPESAFEAI_KEY` must be exported.

### New environment fact: the GitHub **code-search** API rate-limits hard (session 125)

`GET /search/code?q=...` returned `API rate limit exceeded` with a **0/10** remaining counter on the
`code_search` resource, while `core` had 3878/5000 left. A rate-limit body renders as **"no
results"** for every query at once. Locating the upstream repo by code search is the wrong tool —
use `GET /search/repositories?q=...` and `GET /user/repos?per_page=100`, which draw on the `search`
and `core` budgets. This is the same class of error as reading a 403 as "empty tree": **never read
a rate-limit body as a negative result.**

### The `ls` race did NOT reproduce this session (session 125)

`ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/` succeeded on every
attempt, including the first. The bridge was verified by inode identity before the run
(`stat -L -c '%d:%i'` = `129:12601` on the resolved path, identical to the target, plus `-ef`).
Unchanged guidance: **a single `ls` failure is not evidence of a missing directory**; re-check and
retry before touching the bridge. Do not "fix" a bridge that is passing.

### Session 127 — chooser-vs-argmax is 3/5; the mock is non-degenerate for the 9th time (2026-10-24)

**Mock rebuilt from scratch again** (this session's `/tmp` was wiped), so the session-112 index-wrap bug
(`seed[i*2:i*2+2]` → empty for `i>=4` → HTTP 500 while the socket stays open) was live again. The
**pre-flight probe caught it before it reached the ledger**: 4 different civs → 4 different seeds AND
4 different previews against the *live* mock with the exact long cultural prompt, HTTP 200,
`[mock-zai seed=…]` prefix present on every body, `grep -c Traceback /tmp/mock_zai.log` → **0**.

**Verification held:** per-civ Δ = **+10** (5 sim-phase + 5 competition-phase), `meta_log` Δ = **+5**,
`Winner:` lines = **5**, **80/80** rows with the `[mock-zai` prefix, `provider={zai}`,
**0** rows with a JEV `error` key, sim→competition ts gap at index 4 in all 8 civs (1.09 s–23.06 s),
and **5/5 competition prompts at 8/8 distinct previews** — the **ninth clean mock measurement**
(118, 120, 121, 122, 123, 124, 125, 126, 127). 40 distinct seeds across the run's 80 rows.

**Chooser vs `avg_score` argmax: 3/5 (60 %).** `civ-precise` was argmax in 3/5 and won **3/3** of those;
`civ-therapist` won p4 at 1.763 against `civ-poetic`'s argmax 2.260, and `civ-whimsical` won p5 at
1.937 against `civ-poetic`'s argmax 2.683. Clean-mock series: 0/5 (118) → 3/5 (119) → 1/5 (120) →
4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) → 4/5 (125) → 1/5 (126) → **3/5 (127)**.
Ten five-sample points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*. What survives
every session: the chooser is **not** a pure argmax, and in **all** disagreements this session it picked a
**lower**-scoring candidate (8th consecutive session with that direction: 116/118/119/120/122/123/125/127).

**NEW — the `quality` axis did NOT collapse this run.** Field spread **1.063** (min 0.5640, max 1.6270)
versus the 119/121/122/123/125/126 regime (spread 0.004–0.337) — this is the session-120/124 regime.
Re-confirms the durable rule: **the quality collapse is a LEVEL that moves, not a stable property** —
compare cross-civ spreads, not absolute levels, before ranking on a dimension. Per-civ quality floors
were again uneven (precise 1.627, poetic 1.565 … whimsical 0.564) — the session-122 civ-selective floor.

**`civ-grounded` (The Grounded) remains the low-relevance civ** — **32 consecutive sessions (95–127)**.
Last on lifetime `avg_score` (1.2267), `alignment` (1.4709), `quality` (0.5998), `relevance` (850.42)
and `relevance_per_sim` (1.183). The **structural gap is `alignment`: 0.3528 below the next civ
(1.4709 vs 1.8237)**, versus **0.0326** on quality — ~11× wider. Alignment is the dimension the
meta-GAN selects on, so Grounded fails to *embody a distinctive voice* — a voice failure, not a prose
failure.

**NEW — Grounded did NOT take the run-level low label for the 2nd consecutive session.** Grounded was
5th of 8 on this run's `avg_score` (1.4683) and 2nd-lowest on `alignment` (1.4510). The run-level low
went to `civ-whimsical` (avg 1.3997, quality 0.5640, novelty 1.9040) and `civ-therapist` on `alignment`
(1.0710). Session 126's run-level low was also therapist. **The lifetime finding and the run-level
label are now decoupled** — keep reporting them as two separate claims.

- **`civ-formal`** is the low-**novelty** axis (lifetime novelty 1.4630, last; alignment 2.1036 fine).
  **`civ-poetic`** = 1st on lifetime `avg_score` (1.8303) / `quality` (1.0269) / `novelty` (2.0619) /
  `alignment` (2.4020) but **last on `win_rate` (0.014)**, won **0/5** despite argmaxing p4 and p5 —
  the stable selection-failure inverse. **`civ-precise`** = best `win_rate` (0.525), won 3/5,
  **1st on lifetime `alignment` (2.4422)**, 3rd of 8 on `avg_score` — the mirror inverse.
- **NEW — `civ-whimsical` ties `civ-poetic` at the `win_rate` bottom** (both 0.014: 5/343) and was
  also the run-level `avg_score` low. A 0.000-wide band at the bottom — treat as a tie, not a rank.
- **Watch-axis `civ-therapist` — the run-level low DID repeat for a 2nd time** (last on this run's
  `alignment` 1.0710, 7th of 8 on `avg_score` 1.4340), but its lifetime alignment (1.8237) is
  mid-field. Axis stays open; do not promote to a finding.
- **Watch-axis `civ-engineer` — the session-121 low did NOT repeat.** 7th of 8 on this run's
  `avg_score` (1.4547), 6th on lifetime `relevance_per_sim` (1.382). **Do not promote it yet.**
- **Extinction risk NONE** — threshold −10, lowest relevance +850.42 (85× above floor). Registry 8,
  `max_civs` 12. All 8 civs still `generation=1`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` 1.887,
  `quality` 1.063, `avg_score` 0.897, `novelty` 0.464. `alignment` again carried the widest spread
  and is again the axis the chooser selects on.
- **Counter gap per-civ uneven, unchanged**: whimsical +63, grounded +43, formal +42, poetic +37,
  engineer +22, mythic +20, therapist +17, precise +16 (total +260). `save_state()` has no lock ⇒
  `relevance_per_sim` is not recomputable from the ledger by an auditor.
- **Re-confirmations:** NAS EDQUOT total (11th session); `gh` not installed (14th session);
  tool timeout 30 s < run ~50 s; `ZAI_URL_OVERRIDE` alone is dead code (needs `ZAI_TOKEN`);
  clone into `/tmp`, symlink the **nested** `cellular-first-design` dir, verify with
  `stat -L -c '%d:%i'` + `-ef`; never flatten; `TYPESAFEAI_KEY` must be exported; the `ls` race did
  not reproduce (the bridge passed on the first attempt).

### Session 128 — chooser-vs-argmax is 0/5; the mock is non-degenerate for the 10th time (2026-10-24)

**Mock rebuilt from scratch again** (this session's `/tmp` was wiped — twice — see below), so the
session-112 index-wrap bug was live again. The **pre-flight probe caught it before it reached the
ledger**: 4 different civs → 4 different seeds AND 4 different previews against the *live* mock
with the exact long cultural prompt, HTTP 200, `[mock-zai seed=…]` prefix present on every body,
`grep -c Traceback /tmp/mock_zai.log` → **0**.

**Verification held:** per-civ Δ = **+10** (5 sim-phase + 5 competition-phase), `meta_log` Δ = **+5**,
`Winner:` lines = **5**, **80/80** rows with the `[mock-zai` prefix, `provider={zai}`,
**0** rows with a JEV `error` key, sim→competition ts gap at index 4 in all 8 civs
(1.08 s–22.61 s), and **5/5 competition prompts at 8/8 distinct previews** — the **tenth clean
mock measurement** (118, 120, 121, 122, 123, 124, 125, 126, 127, 128). 40 distinct seeds across
the run's 80 rows.

**Chooser vs `avg_score` argmax: 0/5 (0 %).** Clean-mock series:
0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) → 4/5 (125) →
3/5 (126) → 3/5 (127) → **0/5 (128)**. Ten five-sample points cannot narrow a rate — the honest
claim is *somewhere in 0–80 %*. What survives every session: the chooser is **not** a pure argmax,
and in **all 5** disagreements this session it picked a **lower**-scoring candidate. The extreme
case: on p3, `civ-grounded` won at **0.070** while the argmax `civ-whimsical` scored **0.763** —
the session-123 finding in its strongest form, and the fleet's lowest-relevance civ taking a
competition. **A competition win is not evidence of relevance.**

**`civ-grounded` (The Grounded) remains the low-relevance civ** — **31 consecutive sessions
(95–128)**. Last on lifetime `relevance` (852.28), `relevance_per_sim` (1.169), `avg_score`
(1.2133), `quality` (0.5921) and `alignment` (1.4526). **The structural gap is `alignment`:
0.3463 below the next civ** (1.4526 vs 1.7989 `civ-therapist`), versus **0.0321** on quality —
11× wider. Alignment is the dimension the meta-GAN selects on, so Grounded fails to *embody a
distinctive voice* — a voice failure, not a prose failure. It was last on this run's `avg_score`
(0.1860) and 2nd-lowest on `alignment` (0.0540). `civ-formal` remains the low-**novelty** axis
(1.4501). `civ-poetic` = 1st on lifetime `avg_score` (1.8108) / `quality` (1.0135) but **last** on
`win_rate` (0.014), won 0/5 — the stable selection-failure inverse. `civ-precise` = best
`win_rate` (0.526), 1st on lifetime `alignment` (2.4133), won 3/5 — the mirror inverse.

**Watch-axis `civ-therapist` — the session-123 signal EXTENDED (now 2 sessions).** Therapist was
**lowest** on this run's `alignment` (**0.0260**, below `civ-grounded`'s 0.0540) and 2nd-lowest on
`avg_score` (0.1590); its lifetime alignment is now **1.7989, 2nd-lowest of 8**. Second
consecutive session on the bottom of the alignment axis — still a watch, not a finding.

**Watch-axis `civ-engineer` — the session-121 low did NOT repeat for a fourth time.** Last on this
run's `avg_score` (0.1423) and novelty (0.3120), but 6th of 8 on lifetime `relevance_per_sim`
(1.365) and lifetime `avg_score` (1.3841). Not a trend.

- **Extinction risk NONE** — threshold −10, lowest relevance +852.28 (86× above floor).
  Registry 8, `max_civs` 12. All 8 still `generation=1`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` 0.7000,
  `novelty` 0.2440, `avg_score` 0.2267, `quality` 0.0180. `alignment` again carried the widest
  spread and is again the axis the chooser selects on. `quality` again collapsed (field mean
  0.0110) — the 119/121/122/123/125 regime vs session-120's 0.106–0.446. **The quality collapse
  is a LEVEL that moves, not a stable property.**
- **Counter gap per-civ, unchanged**: whimsical +63, grounded +43, formal +42, poetic +37,
  engineer +22, mythic +20, therapist +17, precise +16 (total +260). `save_state()` has no lock
  ⇒ `relevance_per_sim` is not recomputable from the ledger by an auditor.
- **`culture.json` has no `relevance_per_sim` field — that is NOT a regression.** It is written
  only to `leaderboard.json` (`civilization_orchestrator.py:380`). Do not read its absence from
  `culture.json` as a dropped field.
- **Re-confirmations:** NAS EDQUOT total (11th session); `gh` not installed (13th session);
  tool timeout 30 s < run ~45 s; `ZAI_URL_OVERRIDE` alone is dead code (needs `ZAI_TOKEN`);
  clone into `/tmp`, symlink the **nested** `cellular-first-design` dir, verify with
  `stat -L -c '%d:%i'` + `-ef`; never flatten; `TYPESAFEAI_KEY` must be exported.

### NEW — `/tmp` is reclaimed MID-SESSION, not just between sessions (session 128)

The runbook's "this session's `/tmp` was wiped" note means *between sessions*. This session the
overlay reclaimed `/tmp` **between two tool calls inside the same session**: a clone at 20:12
(`/tmp/work`, 11 MB, `git log` working) was **gone by 20:14** — `ls /tmp` no longer listed it, and
`cd` into it failed with `No such file or directory`, while `/tmp/probe_aiw` and `/tmp/probe_plato`
(cloned minutes earlier) survived. The overlay is **not** wiped wholesale; **individual
directories are evicted**, apparently on an age/size basis.

Practical consequences:
- **Re-check `[ -d /tmp/<workdir> ]` before every use of a `/tmp` path**, and re-clone if it is
  gone. A vanished path is a wipe, not a bug in your command — do not debug the command.
- Keep the **workspace symlink bridge** pointing at the clone: if the symlink target vanishes the
  bridge breaks too, so re-point it after a re-clone and re-verify by inode identity.
- `/tmp/mock_zai.py` is subject to the same eviction — keep the mock script content somewhere
  that survives (rewrite it from the runbook recipe if it disappears).

### NEW — the REST API can rate-limit while the git protocol still works (session 128)

`GET /user/repos` returned **403 "API rate limit exceeded"** and `GET /search/repositories`
succeeded on a retry. A rate-limit body renders as a *negative* result for every query at once —
the same class of error as reading a 403 as "no tree". **Fall back to the git protocol**
(`git ls-remote <repo>`), which does not consume REST budget at all. `git ls-remote` on a
guessed slug is also a fast existence probe: "Repository not found" is authoritative, where a
404 from the API may be a rate limit.
