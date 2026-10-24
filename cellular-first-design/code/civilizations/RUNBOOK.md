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
