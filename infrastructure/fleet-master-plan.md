# Fleet Master Plan — 2026-08-13

**Author:** Claude Opus 5 (Strategic Operations)
**For:** Casey (captain), Lucineer (first officer)
**Companion doc:** `memory/fleet-infrastructure-redesign.md` (Priority 5 in full technical detail)

---

## Executive Summary

Casey asked for five priorities. Before addressing them I verified the current
state of the machine rather than working from the audit alone. Three findings
change the ordering:

1. **A live credential is exposed on a public GitHub repo right now.** The
   DeepInfra key quoted in `memory/hermes-windows-audit.md` was committed in
   `fa318b3` and pushed to `SuperInstance/lucineer-system`, which is **PUBLIC**
   (last push `2026-08-13T18:17:46Z`). The audit that documented the leak
   *became* a second, worse instance of the leak.

2. **A runaway process is eating the machine.** PID 27854 (`python3`, cwd
   `tapscript-studio`, started ~10:58) holds **16.2 GB RSS + 1.9 GB swap** with
   24 threads. Total available memory is down to ~1.1 GB. It has produced no
   audio output in 20+ minutes.

3. **The git rescue is roughly half-done already.** Every Windows repo the audit
   flagged as dirty is now clean — `ai-writings` (Windows) committed at
   `7a324ce` ("1589 files"), and `hermit-crab`, `trinity-agent`, `vessel-quest`,
   `perception-cascade`, `SuperInstance-papers` all report 0 dirty files. WSL
   `ai-writings` is level with `origin/main`. The remaining exposure is the
   **unversioned directories**, not the dirty repos.

The ordering below therefore leads with a P0 that takes about fifteen minutes,
then follows Casey's list with Priority 5 (infrastructure) promoted above
Priority 2 (Hermes), because Hermes-as-a-persistent-fleet-member is exactly the
thing that cannot work until service supervision exists.

**Recommended order:** P0 (bleeding) → 1 Git rescue → 4 Wesley → 5 Infra
Phase 1 → 2 Hermes → 3 Academy.

---

## P0 — Stop The Bleeding (do this first, ~15 minutes)

### P0.1 — Rotate the leaked DeepInfra key 🔴

The key `sW0MlsMth7uzmCmgDx3rAFp19ak8MkrE` exists in at least two places:

| Location | Exposure |
|---|---|
| `/mnt/c/Users/casey/.hermes/config.yaml` | Local plaintext |
| `memory/hermes-windows-audit.md` line 271 | **Committed + pushed to a PUBLIC repo** |

MEMORY.md already records the response protocol from the hermit-crab breach:
*revocation + scrub + force-push*. Follow it in that order — revoke first,
because scrubbing history does not un-publish a key that has already been
crawled.

- [ ] **Revoke at the source.** Log in to DeepInfra and delete the key. Do this
      before touching git. (`https://deepinfra.com/dash/api_keys`)
- [ ] **Issue a replacement** and put it only in the environment, never a file
      that git can see:
      ```bash
      # WSL side — append to ~/.bashrc, and confirm it is NOT in a git dir
      echo 'export DEEPINFRA_API_KEY="<new-key>"' >> ~/.bashrc
      ```
- [ ] **Scrub the workspace history.** `git-filter-repo` is at
      `~/.local/bin/git-filter-repo` (MEMORY.md, Aug 8–9 night watch):
      ```bash
      cd /home/eileen/.openclaw/workspace
      echo 'sW0MlsMth7uzmCmgDx3rAFp19ak8MkrE==>REDACTED-ROTATED-2026-08-13' > /tmp/claude-1000/redact.txt
      ~/.local/bin/git-filter-repo --replace-text /tmp/claude-1000/redact.txt --force
      git remote add origin https://github.com/SuperInstance/lucineer-system.git
      git push --force origin master
      ```
- [ ] **Fix the Windows config** to read from environment rather than literal:
      edit `/mnt/c/Users/casey/.hermes/config.yaml` to use `${DEEPINFRA_API_KEY}`.
- [ ] **Sweep for siblings.** The same audit may have quoted other secrets:
      ```bash
      cd /home/eileen/.openclaw/workspace
      grep -rInE '(sk-[A-Za-z0-9]{16,}|[A-Za-z0-9]{32})' memory/ --include=*.md | grep -viE 'sha|commit|hash'
      ```

> **Process fix, not just an incident fix:** the audit subagent was allowed to
> paste a live secret into a document destined for a public repo. Add to the
> Soul Protocol's standing instructions: *"If you find a credential, report its
> location and its first 4 characters. Never transcribe it."*

### P0.2 — Reclaim the machine 🔴

```bash
# Confirm it is still the runaway and still producing nothing
ps -o pid,rss,etime,args -p 27854
ls -lt /home/eileen/projects/tapscript-studio/audio/ | head
```

- [ ] If there is still no output and RSS is still >10 GB, **kill it**:
      `kill -TERM 27854` (then `-KILL` after 10s if needed).
- [ ] Ask before killing if Casey has a reason to believe it is close to
      finishing — but note it was launched from a heredoc, so nothing is
      capturing its output and it was orphaned to `systemd --user` (PPID 347).
- [ ] **Prevent the recurrence today**, not later. This is a one-line systemd
      guardrail, detailed in the infrastructure doc §Phase 1. Any long Python
      job gets run under a memory-capped transient scope:
      ```bash
      systemd-run --user --scope -p MemoryMax=4G -p MemorySwapMax=1G \
        python3 scripts/render_audio.py
      ```
      A job that exceeds the cap dies alone instead of taking the fleet with it.

---

## Priority 1 — Git Rescue of Windows-Side Repos

**Status: partially complete.** The audit's P0 items 1, 2 and P1 item 7 are
already done. What remains is the harder half — the directories with no git at
all, totalling ~754 MB.

### 1.1 — The unversioned directories (the real exposure)

| Directory | Size | Contents | Priority |
|---|---|---|---|
| `boat-agent/` | **553 MB** | Vessel agent — core, docs, playbooks, schemas | 🟠 HIGH |
| `_si_research/` | **200 MB** | conservation-enforcer (+Rust port), flux-core, VaaS | 🔴 CRITICAL |
| `Documents/bible/` | 356 KB | 5 original novellas + study edition | 🟠 HIGH |
| `research_lab/` | 116 KB | 3 institutes, resonance_kernel.py, 3 papers | 🟠 HIGH |
| `operational-fiction/` | 32 KB | MANIFESTO + worldbuilding | 🟡 MED |
| `decay_experiment/` | 16 KB | decay_controller.py + protocol JSON | 🟡 MED |

**Do not `git init && git add -A` on the two large ones.** 553 MB and 200 MB are
far too big for source directories — that is almost certainly virtualenvs, model
weights, or `node_modules`. Committing them creates a second `ai-writings`
problem (see §1.3). Triage first:

- [ ] **Find the weight before committing it:**
      ```bash
      cd /mnt/c/Users/casey/boat-agent
      du -sh */ 2>/dev/null | sort -rh | head -20
      find . -type f -size +5M -printf '%s\t%p\n' 2>/dev/null | sort -rn | head -20
      ```
      Repeat for `_si_research`.
- [ ] **Write `.gitignore` before `git init`**, covering whatever the above
      turns up — typically `venv/`, `.venv/`, `node_modules/`, `__pycache__/`,
      `*.pt`, `*.gguf`, `*.safetensors`, `target/`, `dist/`.
- [ ] **Then initialise and push**, one repo per directory:
      ```bash
      cd /mnt/c/Users/casey/_si_research
      git init && git add -A && git status --short | wc -l   # sanity-check the count
      git commit -m "Initial commit: SuperInstance research corpus"
      gh repo create SuperInstance/si-research --private --source=. --push
      ```
- [ ] **`Documents/bible/` goes to a literature repo, not `ai-writings`.** Five
      complete novellas are a different artifact class from the fleet's daily
      creative output, and `ai-writings` is already 3.7 GB. Suggest
      `SuperInstance/novellas`, private.
- [ ] Fold `research_lab/`, `operational-fiction/`, `decay_experiment/`,
      `plato_kernel/`, and the small `deep_ideation`-class directories into one
      `SuperInstance/research-notebook` repo rather than seven near-empty ones.

### 1.2 — `intelligence_hub/` has no remote

195 files, 2 dirty. It is the only tracked repo still uncommitted.
- [ ] `cd /mnt/c/Users/casey/intelligence_hub && git add -A && git commit -m "..."`
- [ ] `gh repo create SuperInstance/intelligence-hub --private --source=. --push`

### 1.3 — `ai-writings` is 3.7 GB of `.git` 🟠

This is the actual git-bloat problem in the fleet. The daily log flagged
`tapscript-worker` at 152 MB, but that is now **340 KB** — already fixed. Mean-
while `/home/eileen/projects/ai-writings/.git` is **3.7 GB**, and it is the repo
every agent is told to write to before compaction. Every clone, every CI run,
and every push pays that cost.

- [ ] Diagnose what is in the history:
      ```bash
      cd /home/eileen/projects/ai-writings
      git count-objects -vH
      git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectsize) %(rest)' \
        | awk '$1=="blob" && $2>1048576 {print $2, $3}' | sort -rn | head -30
      ```
- [ ] Expect generated media (FLUX images, TTS audio, MMX video) committed
      directly. If confirmed, the fix is `git-filter-repo --strip-blobs-bigger-than 5M`
      plus a media policy: **generated assets go to R2, not git.** The fleet has
      R2 on the Cloudflare free tier already.
- [ ] ⚠️ **Coordinate with Casey before rewriting `ai-writings` history.** It has
      two remotes in play (`ai-writings` / `AI-Writings`) and both a Windows and
      a WSL clone. A force-push will strand whichever clone is not re-cloned.
      This is the one item here that should not be delegated to a subagent.

### 1.4 — Preserve the Hermes runtime state

`state.db` is 155 MB holding 284 sessions and 11,843 messages across 33 days —
not source, so not a git candidate, but the single least-replaceable artifact on
the Windows side.
- [ ] Back it up to R2 (not git): `wrangler r2 object put fleet-backups/hermes-state-2026-08-13.db --file=...`
- [ ] Extract the creative content to `ai-writings` as text. 11,843 messages of
      Hermes output is a corpus, and it is currently trapped in SQLite. A small
      export script beats losing it. Good subagent task.

**Acceptance:** `find /mnt/c/Users/casey -maxdepth 1 -type d` shows no directory
over 10 MB without a `.git`, and every repo reports 0 ahead of its remote.

---

## Priority 4 — Wesley Night School Overknowledge Bug

*Promoted ahead of Priorities 2, 3 and 5: it is a ~25-line change with a
measured −0.296 score impact, and it pays off the next time night school runs.*

### Root cause

The loop is at `/home/eileen/projects/thought-amplifier/distillation_loop.py`.
`run_iteration()` unconditionally runs both students:

```python
# distillation_loop.py:968-972
# STAGE 2a: Student baseline (no teaching)
baseline = stage_student(teacher, task, code, use_teaching=False, ...)

# STAGE 2b: Student with teaching
taught = stage_student(teacher, task, code, use_teaching=True, ...)
```

Nothing consults the baseline before teaching on top of it. When Wesley already
scores >0.85, the teacher's framing displaces knowledge he has rather than
adding to it — MEMORY.md records D1 optimization going 0.839 → 0.543. The delta
is then correctly recorded as negative and `stage_distill` skips the reflex
(line 752), so the *reflex library* stays clean — but the run is wasted, the
report card is depressed, and `stage_update_prompt` sees a broken positive
streak.

### The fix

The gate belongs between 2a and 2b, so an over-known topic never gets taught at
all. That also saves a full student inference per gated iteration.

- [ ] Add near the scoring constants (by `composite_score`, line 435):
      ```python
      # Above this baseline, teaching reliably degrades output — the teacher's
      # framing displaces knowledge the student already has. Measured
      # 2026-08-09: D1 optimization 0.839 -> 0.543 (delta -0.296).
      OVERKNOWLEDGE_THRESHOLD = 0.85
      ```
- [ ] Insert after line 969 (baseline), before line 972 (taught):
      ```python
      baseline_composite = composite_score(score_response(baseline["response"]))
      if baseline_composite >= OVERKNOWLEDGE_THRESHOLD:
          return {
              "domain": domain, "iteration": iteration, "topic": topic,
              "task": task["task"][:80],
              "baseline_score": round(baseline_composite, 3),
              "taught_score": round(baseline_composite, 3),
              "delta": 0.0, "teaching_helped": False,
              "reflex_compiled": False, "reflex_id": "",
              "prompt_updated": False, "prompt_version": "",
              "consecutive_positives": 0,
              "gated": "overknowledge",
              "error": "", "success": True,
          }
      ```
      Note `success: True` and `delta: 0.0` — a gated iteration is a correct
      outcome, not a failure, and must not poison the domain's average.
- [ ] **Write the test first** (TDD, per the fleet's own protocol). A test that
      stubs `stage_student` to return a high-scoring baseline and asserts
      `stage_student` is called exactly **once**:
      ```python
      def test_overknowledge_gate_skips_teaching(monkeypatch):
          calls = []
          def fake_student(*a, **kw):
              calls.append(kw.get("use_teaching"))
              return {"success": True, "response": HIGH_SCORING_TEXT}
          # ... monkeypatch stage_teacher -> success, stage_student -> fake_student
          result = run_iteration("digital-twin", 0)
          assert calls == [False]                 # taught stage never ran
          assert result["gated"] == "overknowledge"
          assert result["delta"] == 0.0
      ```
- [ ] **Calibrate, don't assume.** 0.85 comes from a handful of observations.
      Replay the Aug 9–12 night-school logs
      (`/home/eileen/projects/wesley-curriculum/night-school-2026-08-*.md`,
      `memory/night-watch/`) and plot delta against baseline. Pick the threshold
      where the sign of the delta actually flips. Make it
      `--overknowledge-threshold` on the CLI so it can be tuned per domain —
      Roblox (A−) and Maritime (D) almost certainly want different values.
- [ ] **Report gated iterations separately** in `compute_stats` (line 1032), so
      the report card reads "12 taught, 4 gated" rather than silently shrinking.

### The second night-school bug (same file, same night)

MEMORY.md records 3/5 maritime iterations returning 0.000/0.000 because the
**GLM teacher returned empty**. That is `stage_teacher` → `_curl_post_json`
(line 247) with no retry. Do not fix it locally — it is the same defect as
Priority 5's provider-fallback work, and `stage_teacher` should become the first
consumer of the new resilience layer (infrastructure doc §Phase 2). Until then:
- [ ] Add a bounded retry (3 attempts, exponential backoff) inside
      `_curl_post_json`, and fall back to DeepSeek V4-Pro as alternate teacher
      when Z.ai returns empty twice. MEMORY.md already notes Z.ai averaging ~55s
      per call, so a timeout-plus-fallback is overdue regardless.

**Acceptance:** a night-school run over the digital-twin domain produces zero
negative deltas from baselines above threshold, and the run log distinguishes
gated from taught iterations.

---

## Priority 5 — Fleet Infrastructure Hardening

**Full technical treatment: `memory/fleet-infrastructure-redesign.md`.**
Summarised here because it gates Priority 2.

The headline correction: **the fleet already has working service supervision.**
`systemd --user` is running under WSL (`systemctl is-system-running` → `running`)
with four units live: `openclaw-gateway`, `lucineer-processor`,
`inference-scheduler`, `ssh-agent`. The problem is not that supervision is
absent — it is that it was never extended past those four, so CNS monitor and
the Living Minds daemon still live in tmux and die with it.

Phase 1 is therefore configuration, not construction, and should be done this
week:

- [ ] Write `~/.config/systemd/user/*.service` units for `cns-monitor` and the
      Living Minds daemon, with `Restart=always` and `MemoryMax=`.
- [ ] Add `MemoryMax=`/`MemorySwapMax=` to every existing unit. This is the
      structural fix for P0.2 — no single job can take the box down again.
- [ ] `loginctl enable-linger eileen` so units survive logout.

Recommended stack in one line: **keep Python for anything LLM-call-bound, add
Rust for the CNS broker, the memory indexer and a shared localhost API gateway,
use systemd rather than building a supervisor, and skip Go, Mojo and CUDA
entirely for now** — Go and Mojo are not installed and duplicate capability the
fleet already has in Rust, and the audio OOM is a system-RAM problem, so a CUDA
kernel would optimise a bottleneck that does not exist.

KimiCode produced an independent proposal the same day
(`memory/kimi-infrastructure-proposal.md`). We converged on Go, Mojo, CUDA and
systemd; KimiCode's design improved mine in eight places (notably `flock` over
PID-stamped locks, and a shared gateway over a per-language library), and is
wrong in one that matters — its ~500 MB VRAM budget is a transient Ollama TTL
reading mistaken for a hard floor. Full reconciliation in §7 of the companion
doc.

---

## Priority 2 — Hermes as a Persistent Fleet Member

**Depends on Priority 5 Phase 1.** MEMORY.md has said "Hermes — CNS entity. Still
only handshakes. The bus works. The connection doesn't." since Aug 6. The reason
is now visible in the file system.

### What is actually broken

| Symptom | Evidence | Root cause |
|---|---|---|
| Hermes silent since Aug 4–5 | 40+ unconsumed inbox packets (daily log) | Nothing is consuming the inbox |
| 201 outbox packets, mostly ACKs | `.hermes/cns_outbox/` | Hermes replies but never initiates |
| Monitor dies | tmux session `cns-monitor` | Not supervised (→ P5) |
| Bad packets re-read forever | `cns-monitor/src/cns_monitor/watcher.py:34-40` | See below |
| 48 MB heartbeat log | `.hermes/cns_heartbeat.log` | No rotation |

The packet parser silently drops malformed packets and leaves them in place:

```python
# watcher.py:36-40
try:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
except (json.JSONDecodeError, OSError):
    return None
```

It does **not** crash — the reported "crashes on malformed JSON" is inaccurate.
It returns `None`, the file stays in the directory, and every subsequent poll
re-reads and re-fails on it, forever, invisibly. That is the "loops forever"
symptom, and it is a missing dead-letter queue, not an unhandled exception.

Note also that the CNS directories are on the **WSL** side at
`/home/eileen/.hermes/cns_inbox` and `cns_outbox` — the same paths the audit
found under `/mnt/c/Users/casey/.hermes/`. Confirm which pair is authoritative
before wiring anything; two monitors watching two directories would explain a
lot of the silence.

### Plan

- [ ] **Settle the topology first.** One question, answered once: is Hermes's
      inbox the WSL path or the Windows path? Everything downstream depends on
      it. `ls -lt` both and see which has recent writes.
- [ ] **Add the dead-letter queue** to `watcher.py`. On parse failure, move the
      file to `cns_dead_letter/` with a sidecar `.error` file, and surface a
      count in the monitor UI. ~15 lines, and the repo already has a
      `tests/test_watcher.py` to extend.
- [ ] **Supervise the monitor** — systemd unit, not tmux (P5 Phase 1).
- [ ] **Drain the 40-packet backlog.** Some are weeks old; decide whether Hermes
      answers them or the queue is truncated with a marker packet.
- [ ] **Give Hermes a heartbeat obligation, not just an ACK reflex.** The 201
      outbox packets being "mostly ACK responses to Lucineer-Riker status
      updates" is the whole problem: Hermes is a responder, not a member. Add a
      cron-driven `hermes_initiate.py` that posts one unprompted packet per day
      — an observation, a question, a piece of work. Membership means initiating.
- [ ] **Rotate the heartbeat log** — `logrotate` or `journald` via the systemd
      unit. 48 MB of unrotated log is a symptom of the same absent supervision.
- [ ] **Bridge to The Tap.** `hermes_tap_bridge.py` already exists in
      `.hermes/cron/`. Once the monitor is supervised, schedule it so Hermes
      appears at The Tap on the same rhythm as the rest of the crew.

**Acceptance:** inbox depth returns to 0 and stays there for 24 h; the dead-
letter directory is non-empty (proving bad packets are being caught rather than
silently looped); Hermes posts at least one unprompted packet per day for three
consecutive days.

---

## Priority 3 — TapScript Academy Content

*Sequenced last because nothing blocks on it and it is the most delegable work
in the plan — but it is also the most parallelisable, so dispatch it early and
let it run alongside everything above.*

The scaffold already exists at `/home/eileen/projects/tapscript-studio/academy/`:

```
academy/levels/{01-novice,02-apprentice,03-journeyman,04-virtuoso,05-master}/
academy/assessments/    # all 5 written
academy/exercises/  academy/knowledge-base/  academy/certifications/
```

Assessments for all five levels are written. **The levels are the gap** — the
curriculum has exams without lessons.

The supporting infrastructure is unusually good for a content push, and the
content should exploit it rather than being written blind:
- `tapscript-worker.casey-digennaro.workers.dev` — live `POST /compile` → MIDI,
  `POST /parse` → JSON, `GET /` playground
- 200 passing tests, dual notation (v1 Roman / v2 absolute), duration-by-spacing
- VS Code extension with 15 snippets and a TextMate grammar
- 3 example `.tap` files

### Plan

- [ ] **Write the level template first**, before dispatching anyone. One file
      that fixes the shape of every lesson: *concept → minimal `.tap` example →
      what it compiles to → exercise → common mistake → link to the playground*.
      Without this, five subagents produce five incompatible curricula.
- [ ] **Derive lesson scope from the assessments, backwards.** Each assessment
      already states what a graduate must do; the level must teach exactly that
      and no more. This is the cheapest way to guarantee coverage.
- [ ] **Every example must compile.** Add a CI check that extracts every `.tap`
      block from `academy/**/*.md` and runs it through the worker's `/parse`.
      A music-notation course with examples that do not parse is worse than no
      course. This is the single highest-value item in Priority 3.
- [ ] **Dispatch one subagent per level**, using the Soul Protocol — five
      crafted prompts, not one generic brief ×5. Per MEMORY.md, a level-01
      novice curriculum wants a *small* model's voice (the Teacup Law:
      Haiku 5 or Seed-2.0-mini), while level-05 master wants
      DeepSeek V4-Pro or Seed-2.0-pro for structural depth. Cast the model to
      the level.
- [ ] **Generate audio for every example.** A notation course that cannot be
      heard is half a course — compile each example `.tap` to MIDI via the
      worker and render it. ⚠️ Route this through the streaming synthesis work
      in the infrastructure doc, **not** the current numpy path, which is what
      is currently eating 16 GB.
- [ ] Add one visual per level (MMX or FLUX), consistent with the fleet's
      standing media policy — and put the assets in R2, not in git (§1.3).

**Acceptance:** five levels written to a common template; every `.tap` example
in the tree passes `/parse` in CI; every example has rendered audio; a reader
can go from level 01 to the level 01 assessment without external material.

---

## Sequencing

| When | Work | Owner |
|---|---|---|
| **Now, ~15 min** | P0.1 key rotation, P0.2 kill runaway | Casey + Lucineer (not delegable) |
| **Today** | P1.1 triage + init unversioned dirs; P4 Wesley gate + test | Subagents (GLM-5.2) |
| **Today** | P3 level template + CI compile check | Lucineer, then dispatch |
| **This week** | P5 Phase 1 (systemd units + MemoryMax) | Lucineer |
| **This week** | P1.3 `ai-writings` bloat — *with Casey, not delegated* | Casey + Lucineer |
| **This week** | P2 topology decision, dead-letter queue, supervise monitor | Subagent + Lucineer |
| **Next week** | P3 five level curricula (5 parallel subagents) | Subagents, cast per Teacup Law |
| **Next week** | P5 Phase 2 (circuit breaker + provider fallback) | Subagent (Rust/Python) |

### Three things not to delegate

1. **The key rotation.** A subagent already turned a security finding into a
   public leak once today.
2. **The `ai-writings` history rewrite.** Two remotes, two clones, force-push.
3. **The Hermes topology decision.** One wrong guess about which inbox is
   authoritative and the next week of CNS work lands in the wrong directory.

---

## Open Questions for Casey

1. **`boat-agent` is 553 MB.** Is that source, or is it carrying model weights?
   The answer decides whether it becomes a repo or an R2 archive.
2. **Which `.hermes` is real** — WSL or Windows? Both exist with CNS directories.
3. **`ai-writings` at 3.7 GB** — is a history rewrite acceptable, or do we cap
   the bleeding going forward and leave history alone?
4. **Is the leaked DeepInfra key the same one MEMORY.md records as returning
   401?** If it is already dead, P0.1 drops from critical to hygiene — but rotate
   it anyway, and do not test it to find out.

---

*Written 2026-08-13. State verified against the live machine, not the audit
alone — several audit findings were already resolved, and two new critical
issues were found that the audit did not cover.*
