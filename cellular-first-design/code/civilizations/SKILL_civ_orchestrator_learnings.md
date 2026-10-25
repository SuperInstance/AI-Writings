---
name: civ-orchestrator-learnings
description: Durable operating knowledge for the Civilization Orchestrator (cellular-first-design). Mock provider rebuild checklist, verification gates, environment traps, and interpretation rules for the meta-GAN leaderboard.
---

# Civ Orchestrator — durable learnings

## The mock provider algorithm (fully known; do not re-derive)

The Control B mock for `zai` derives every response from the md5 of the request's
user message. This is now **verified 80/80 against the session-169 ledger**
(seed, colour and figure all match), so it does not need re-deriving.

```
d      = md5(cultural_prompt).digest()          # the FULL user message, verbatim
h      = d.hex()
i      = d[0] % 4                               # MESSAGE-derived, NOT a request counter
seed   = h[(i*2)%8:(i*2)%8+2] + h[((i*2)+2)%8:((i*2)+2)%8+2]
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

Only **4** distinct seeds are reachable from one message (the seed slices `h[0:8]`
at even offsets), so `i mod 4` is the whole index space.

**The observable signature of a message-derived index:** the seed is *stable across
every row of the same `(civ, prompt)` pair*. A request counter cannot produce that,
because the competition phase fires 8 civs in parallel and a counter would hand
them different values.

## Mock rebuild checklist — SIX fixes

| # | Fix | Symptom if missing |
|---|---|---|
| a | `seed[(i*2)%8:(i*2)%8+2]` index wrap | `ValueError` on `i>=4` ⇒ HTTP 500 **while the socket stays open** |
| b | md5 of the **whole message** (not the first 8 alnum chars) | first 8 alnum chars are `YouAreA` for every civ ⇒ all 8 civs emit identical text |
| c | `Connection: close` + `Content-Length` | `curl` hangs to the tool timeout on a healthy server |
| d | interpolate the seed placeholder | every response carries literal `seed={}` ⇒ 1 distinct seed, not 40 |
| e | seed widened 2 → 4 hex chars | a 2-char slice collides ⇒ 39 distinct seeds / 40 rows, one prompt at 7/8 |
| f | **index from the MESSAGE (`d[0] % 4`), not a request counter** | **64 distinct seeds / 80 rows; 20 `(civ,prompt)` pairs carry >1 seed** |

## GATE-DESIGN RULE (the durable lesson)

**A pre-flight that only exercises *distinct* inputs cannot certify a *determinism*
property.** The pre-flight sends 40 distinct messages, so a counter-derived index
looks perfect — 40/40 distinct seeds, 40/40 distinct previews, a clean pass — while
the *run* is broken.

Therefore the pre-flight must include a **repeat-same-message probe**: send the same
message twice and assert the seed is identical (and matches the recomputed md5).

The same principle generalises: *any* pre-flight that proves "distinctness" is
silent about "determinism". Add a probe that repeats an input.

## Run-wide verification (isolate this run's rows)

Count from the **end** of each civ file (last 10), never a `ts` cutoff.

- per-civ ledger Δ +10 × 8 = **80** new rows
- `meta_log.jsonl` Δ +5
- `Winner:` lines = 5
- `wins` = pre + times won, `losses` = 5 − times won — **8/8 exact**
- `relevance` Δ = Σ this run's `avg_score` — **8/8 exact to 1e-6**
- distinct seeds **40 / 80 rows**; **0** `(civ,prompt)` carrying >1 seed
- **80/80** rows match an independently recomputed message md5
- 8/8 distinct seeds AND previews on every competition prompt (5/5)
- meta-vs-ledger `avg_score` mismatches **0/40** — **use the later-`ts` row**
- 0 JEV errors, 0 `2.0/2.0/2.0` fallback triples
- extinction risk NONE (threshold −10; the lowest civ sits ~110× above it)

**The meta-vs-ledger check needs the later-`ts` row.** The sim phase draws its prompt
at random from the same 5, so a `(civ, prompt)` pair recurs 1–4 times inside the 10 new
rows; the competition-phase row is the later one. `max(cands, key=ts)` gives 40/40
exact; first-match reports false mismatches. Match key is `m["prompt"][:80]`.

## A failed run must be reset, not patched

When the first mock of session 170 was rejected (counter-derived index), the ledger was
restored with `git checkout -- .` **from the clone root**, and the baseline was
re-verified against the captured pre-run counts before the second attempt. Never
hand-edit a ledger to make a check pass — reset and re-run so the baseline and the
result live in the same epoch.

`git show HEAD:<path>` must run with `cwd` = the **clone root**, not the civs
directory; the civs dir is not a git root and `git show` there returns empty stdout
→ `JSONDecodeError`.

## Environment traps (recurring)

- **NAS EDQUOT**: `/workspace` is at 100% (600 G of 600 G). `git clone` into
  `/workspace` fails with `Disk quota exceeded`; even a 20 MB `dd` fails. Clone to
  `/tmp` and bridge with a symlink. The NAS trap also blocks **file delivery** — `cp`
  into `/workspace` leaves a 0-byte file, so deliver by pushing to git.
- **The `write` tool is jailed to the workspace root** and cannot write `/tmp`. Use a
  bash heredoc for `/tmp` artifacts.
- `read` tool is likewise jailed — read `/tmp` files via bash.
- Upstream owner is **`SuperInstance/AI-Writings`**; the `ai-writings/…` slug 404s
  (the GitHub API is case-insensitive). Authenticated as `SuperInstance`.
- `gh` is not installed — use `GET /user/repos` with `GITHUB_TOKEN`.
- `GIT_SSL_NO_VERIFY=1` is required for git fetch/push. Push to the explicit token
  URL: `https://x-access-token:$GITHUB_TOKEN@github.com/<owner>/<repo>.git`.
- `ZAI_TOKEN` is absent from env and all 8 sandbox secrets; z.ai returns **401
  `token expired or incorrect`** ⇒ endpoint healthy, credential absent. Control B
  (the local mock) is the only provider path. Note the `ZAI_URL_OVERRIDE` alone is
  dead code — the token gate returns `None` first, so a placeholder token is required.
- JEV is **live**: a well-formed `questions` body returns HTTP 200 with
  `{"model":"jev-1.14.0", …}`. Export `TYPESAFEAI_KEY` from `TYPESAFE_AI_TOKEN`.
- Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch with stdout redirected
  **and** `< /dev/null`, then poll `ps` + the log.
- **Symlink rule**: `ln -sfn` will not replace an existing directory target. The
  bridge must point at the **clone root**, not the nested `cellular-first-design` dir.
  `rm -rf` the old link, `ln -s`, then verify with `stat -L -c '%d:%i'` on both sides
  + `-ef`.
- **Mock teardown**: kill by exact argv match (`python3 /tmp/mock_zai.py` and
  `timeout -s KILL 900 python3 /tmp/mock_zai.py`) — two pids. Never `pkill -f mock_zai`,
  which self-matches the killing shell. Then prove the port is closed: `curl -m 5` ⇒
  **exit 7**, `HTTP=000`.

## Interpretation rules for the meta-GAN

- **The run low and the lifetime low are different civs on different axes.** The
  run-level low *rotates* every session; the lifetime low is structural. Do not
  promote a run low to the lifetime finding.
- **Never treat `win_rate` as a quality metric.** The chooser asks JEV a **`choice`**
  question over 150-char `content_preview` snippets; `avg_score` is the mean of three
  **`score`** questions on the same text. Different questions, different answers. The
  clean-mock series has 16 five-sample points spanning 0/5 – 4/5 ⇒ the honest claim is
  *somewhere in 0–80 %*, not a point estimate.
- **Read the low-civ gaps, not just the low label.** If the *alignment* gap to the next
  civ is much wider than the *quality* gap, it is a **voice** failure (alignment is the
  dimension the meta-GAN selects on), not a prose failure.
- **The counter gap** (`culture.json` `relevance_score` − ledger Σ`avg_score`) is
  **fixed**, not accumulating: −609.9200 as of sessions 169 and 170, byte-identical.
  `save_state()` has no lock ⇒ `relevance_per_sim` is **not recomputable from the
  ledger** by an auditor. Compute both epochs within the same epoch before comparing.
- Run `avg_score` levels sit **above** the lifetime band; the **ordering** carries the
  information, not the level.
