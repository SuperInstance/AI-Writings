# Civ Orchestrator — Run Report, session 248 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **107th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `5a49c8b` (session 247 tree). **Pre-flight gate: 40/40 PASS.** **Run verification: 80 PASS / 0 FAIL.**

## Environment recovery

- Workspace **empty** apart from `.plugin-cache` — the prompt's path did not exist (**12th consecutive occurrence**).
- Upstream **`SuperInstance/AI-Writings`** (3.7 GB); the `ai-writings/…` slug 404s (API is case-insensitive).
- Cloned to `/tmp/cfdesign` with `--filter=blob:none --no-checkout` + `sparse-checkout set cellular-first-design`.
  Copying into `/workspace` fails with **`Disk quota exceeded`** (NAS EDQUOT, 600 G / 0 avail, **18th session**).
- Bridge symlink `…/cellular-first-design -> /tmp/repo_root/cellular-first-design`; verified by inode identity
  (**`129:12620`**) and `-ef` → `EF_OK`. The clone root must contain `code/civilizations` directly.
- `ZAI_TOKEN` absent from env and from all 8 sandbox secrets; z.ai **401** `token expired or incorrect`
  => endpoint healthy, credential absent (**107th session**).
- **JEV live**: well-formed body => **HTTP 200** with `{"model":"jev-1.14.0", …}`.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code behind the token gate).
- `gh` not installed (**20th session**) — used `GET /user/repos` with `GITHUB_TOKEN`.
- Tool timeout 30 s < orchestrator run ~30 s => detached launch, stdout redirected, `< /dev/null`.
- Mock teardown by exact argv match (pids 436/438) — never `pkill -f mock_zai` (self-match).

## Mock integrity

Applied the session-144 fix (`Connection: close` + `Content-Length`) to `tools/mock_zai.py`.
Body **348** chars (37 header + 162 tail + 149 continuation), inside the 332-369 band, **first build**.

**Spec re-derived against the live ledger before use as a gate oracle** — the session-224
single-4-hex slice reproduces **240/240** mock-format rows exactly (seed + colour + figure);
the older two-2-hex form reproduces only 183. The `#` on the colour is stored in the ledger
preview, so a gate regex must tolerate an optional `#` — **a `#`-stripped comparison
misreports every row as a colour mismatch** (this cost one false negative this session).

## Ledger delta

- **+10 rows per civ, +80 total**; `meta_log` **973 -> 978** (+5); **18** files changed.
- All 8 `simulations.jsonl` md5s changed. Preview length 200 on every new row.
- Sim-phase invariant held 8/8: distinct seeds == distinct prompts, seed stable per `(civ,prompt)`.

## Results

Winners: **`civ-precise` 5/5** (a clean sweep). Agreement with the `avg_score` argmax
**2/5 (40 %)** — 3 down-grades, 0 up-grades.

| civ | run avg | quality | novelty | alignment | relevance | rel/sim | win rate |
|---|---|---|---|---|---|---|---|
| civ-poetic | 2.0233 | 1.1180 | 2.5030 | 2.4490 | 3298.92 | 1.724 | 0.6 % |
| civ-precise | 1.9227 | 0.8310 | 2.3070 | 2.6300 | 3170.59 | 1.664 | 70.9 % |
| civ-formal | 1.7440 | 0.7550 | 2.2290 | 2.2480 | 2743.29 | 1.433 | 12.7 % |
| civ-engineer | 1.6740 | 0.7670 | 2.1740 | 2.0810 | 2622.85 | 1.378 | 6.2 % |
| civ-whimsical | 1.5797 | 0.7720 | 2.4910 | 1.4760 | 2719.43 | 1.416 | 0.5 % |
| civ-mythic | 1.5703 | 0.8660 | 2.2960 | 1.5490 | 2676.52 | 1.402 | 1.1 % |
| civ-grounded | 1.4867 | 0.5300 | 2.3220 | 1.6080 | 2345.20 | 1.216 | 7.9 % |
| **civ-therapist** | **1.2920** | 0.6290 | 2.3720 | **0.8750** | **2344.05** | 1.229 | 1.2 % |

- **Run low `civ-therapist`** (avg **1.2920**) — alignment **0.8750** at the fleet low,
  quality **0.6290** second-lowest: a **two-axis** collapse for the **2nd consecutive session**.
- **Lifetime low `civ-therapist`** (**2344.05**), ahead of `civ-grounded` (**2345.20**) by
  only **1.15** — the tightest bottom-two gap in the series. The step from #2 to #3
  (`civ-engineer` 2622.85) is **277.80**.
- Alignment spread **1.7550 = 2.40x** the `avg_score` spread (0.7313).
- `civ-poetic` was the `avg_score` argmax on **3 of 5** and won **0**; `civ-precise` won 5/5.
- `civ-poetic` also leads lifetime relevance and `relevance_per_sim` while holding a **0.6 %** win rate
  — the leaderboard's `rel/sim` ranking and the competition's win record disagree.
- No civ near extinction (threshold `relevance < -10`; lowest **2344.05**, **234x** the floor).
  Registry 8, `max_civs` 12, all `generation=1`.

## Re-confirmations

- NAS EDQUOT total (18th session) — clone to `/tmp`, sparse-checkout, bridge the clone root,
  verify with `stat -L -c '%d:%i'` + `-ef`.
- z.ai **401** (credential gap, endpoint healthy) — 107th session.
- JEV **HTTP 200** discloses the served model `jev-1.14.0`.
- `ZAI_URL_OVERRIDE` alone is **dead code** — Control B needs **both** it and `ZAI_TOKEN`.
- `gh` not installed (20th session) — `GET /user/repos` with `GITHUB_TOKEN`.
- Detached launch with stdout redirected and `< /dev/null`, then poll.
- **Re-derive every mock spec against the ledger before using it as a gate oracle** — a gate
  written against a wrong spec passes 40/40 on a mock that is wrong for a fraction of rows.
- **Tolerate the optional `#` on the colour field** in any ledger-parsing gate.
