# The Architecture Pass

*Fleet Synthesis — 09 Series*
*Date: 2026-08-06*
*Watch: continuation of the harbourmaster's survey*

---

The Quality Brief told the fleet it has coverage without confidence. This pass goes below that line — into one vessel's engine room (`lucineer-brain`), her public face (`lucineer-com-site`), the sea trials logged by synthetic crew (`playtest-journals`), and the salvage yard nobody has indexed yet (`researchlocal`). Six findings. Each one is a rivet, checked by hand.

---

## 1. Fault Injection Framework for `brain.py`

`brain.py` already has a fallback architecture — three coder models deep, two planner models deep, a fast-mode last resort. What it does not have is a way to know, on any given night, *which* fallback fired and *why*. The Quality Brief named this gap; here is where it actually lives in the code.

**The classification is done by string matching, not types.** In `stage_plan` (line 701) and `stage_commands` (line 777), the only signal used to decide "was this a rate limit or a real failure" is:

```python
if "429" in str(e) or "busy" in str(e).lower():
```

This is a `RuntimeError` message being grepped for a substring. It works today because `call_model`'s own error messages happen to contain `"HTTP {e.code}"`. It will silently misclassify the day someone changes that f-string, or the day DeepInfra changes an error body's wording. A fault injection framework needs `call_model` to raise a small closed set of exception *types* — `RateLimitError`, `TimeoutError`, `EmptyResponseError`, `AuthError`, `ServerError` — so the fallback chain branches on `isinstance`, not on prose.

**Empty content and a real outage look identical.** Line 291 of `call_model`:

```python
if not content:
    finish = choices[0].get("finish_reason", "unknown")
    raise RuntimeError(f"Empty content from {model} (finish_reason={finish})...")
```

This is good — it does check for empty content, and it does try the `reasoning_content` fallback first (line 288, for reasoning models that put output in the wrong field under low `max_tokens`). But once it's a `RuntimeError`, it's indistinguishable downstream from a 500. The Quality Brief's "silently wrong 200 OK" is caught here — but then thrown away as generic text. Give it its own exception type and this becomes a metric (`empty_response_count` per model), not a line in a stderr log nobody reads at 3am.

**The one existing safety net already breaks the contract it's supposed to protect.** `run_fast`'s parse-failure fallback (line 1063-1068):

```python
parsed = {
    "reply": f"I heard you want: {player_message}, but I had trouble generating build commands.",
    ...
}
```

"I heard you want" is exactly the assistant-toned language `LUCINEER_PERSONA` (line 91-92) explicitly forbids — "You are NOT an assistant. Never offer help." The one code path guaranteed to run when everything else has failed is the one place the character is guaranteed to break. This is not hypothetical — see §4 below, it is already happening in production telemetry.

**What a real fault injection framework looks like here, concretely:**

1. **Typed exceptions from `call_model`**, replacing the string-matched branches at lines 701 and 777.
2. **A response validator between `extract_json` and the caller** — schema-check that `commands[].params.position/size` are numeric, `material` is a known Roblox material string, `transparency` is a float in `[0,1]`, `shape` is one of the four allowed values. Right now a hallucinated `"transparency": false` or `"material": "unobtainium"` sails straight through to the Roblox client with zero pushback in this file.
3. **A voice-integrity linter run over every fallback reply**, including the two hardcoded ones (line 803, line 1064). If a reply string starts with `{`, contains an unescaped backslash-quote pattern, or matches an assistant-register phrase list ("I heard", "I'd be happy", "Let me"), fail the test. This turns the exact bug in §4 into something CI catches before a player does.
4. **A monkeypatchable fault-injection harness at the `call_model` boundary** — a test double that can return: empty 200, HTTP 500/503, single-quoted pseudo-JSON, a JSON object truncated mid-key (the shape a real network cutoff produces, not the clean `"not json at all"` strings the current tests use), and a slow response parked exactly at the timeout boundary. Feed each fault into each of the five stages and assert the *system* still produces a Lucineer-voiced, valid-schema reply — not just that the function doesn't crash.
5. **Per-stage latency budgets with alerting**, as the Quality Brief already specified — this pass adds that the budget needs to be enforced at the `run_pipeline` orchestration level, because §4 shows a single request taking 109.86s with nothing in the code path that would have stopped it.

---

## 2. Slackwater Game Architecture and Player Loop

The player-facing loop, per `index.html`'s "How It Works" section, is three steps: type a request, Lucineer builds it, explore and improve. That's the marketing simplification of a five-stage backend pipeline, and the simplification is a good call — a player does not need to know there's an intent parser, a spatial planner, a coder model, an optional personality pass, and a safety gate between their sentence and the wall that appears. But two structural things are worth naming.

**There are two progression systems, not one, and the page only shows the visible half.** The Five Eras (Driftwood & Salvage → Frame & Plank → Stone & Mortar → Metal & Machine → Light & Signal) gate *what materials exist*. `BOND_TIERS` in `brain.py` (lines 146-158) gate *how Lucineer relates to the player* — whether he references past builds by name, argues about scale, says "we," asks the player to build things for him. Bond tier is invisible on the marketing page entirely; it's a pure backend/dialogue system with five distinct behavioral contracts (`bond_level < 10 / 30 / 70 / 150`) that never gets surfaced as a mechanic to the player, only felt. That's a legitimate design choice — implicit relationship-building over an XP bar — but it means the entire second progression axis of the game currently has zero player-facing documentation or signaling anywhere in this file tree.

**The three-beat pattern is a game mechanic wearing the costume of a writing style.** "What he did / the opinion / the hook" (`brain.py` lines 102-106) reads like character-voice guidance, and it is — but the third beat, the deliberately unfinished thing, is literally the hand-off point for the *next* player action. It's not narrative flavor bolted onto a building game; it's the game's actual continuation mechanism, implemented as a prompt instruction rather than as state. Nothing currently tracks "what did Lucineer leave unfinished" as structured data — it lives only inside the LLM's generated prose, which means there's no way to programmatically ask "did the player ever come back and finish the thing Lucineer named?" — the exact question that would tell you whether the mechanic is working.

**The repo footer names an architecture that `brain.py` may not actually be.** `index.html`'s open-source grid describes `lucineer-worker` as "the nervous system" (Cloudflare Worker relay) and `casting-call` as "model routing." `brain.py` — well-tested, clean double-quoted JSON output, careful fallback chains — reads like a *reference implementation* or local dev harness for that routing logic, not the thing actually serving the Roblox client in production. The playtest data in §4 all but confirms this: live responses show single-quoted keys and unquoted numeric fields, a format `brain.py`'s `json.dumps(..., ensure_ascii=False)` calls (lines 1343, and throughout) would never produce, and its own test suite would fail on. Worth stating plainly: **there appear to be two divergent implementations of the same pipeline**, one correct and heavily tested, one live and drifting. That's not a phrasing nuance — it's the highest-leverage finding in this whole pass, because every hour spent hardening `brain.py` is an hour not spent on whatever the Roblox client is actually calling.

---

## 3. Frontend Product Page Design

`index.html` is doing more engineering than a marketing page usually needs to, and doing most of it well.

**Typography is a three-register system, used correctly.** Cormorant Garamond (serif) carries the hero title and section headers — the emotional/editorial register. Inter carries body copy — the functional register. JetBrains Mono carries the "you type" / "Lucineer builds" example strings and the era material tags (`<span>Driftwood</span>`) — the technical/game-UI register. That's not decoration, it's a legible signal to the reader about which kind of text they're looking at, and it's applied consistently across all eight sections.

**The "How It Works" panel is an intentional simplification of the real pipeline** — see §2 — but it does this without ever mentioning the safety stage. `stage_safety` runs on *every* request, always (line 980, "Stage 5... always runs, regardless of mode"), and its failure mode is a hard deflection: `"Not building that. Pick something else."` For a game explicitly targeting ages 9+ (per the Nemotron system prompt itself, line 365), a kid hitting that wall with zero page-level framing for why it exists is a real UX gap, not a nitpick — it's the one moment where the product's actual trust boundary becomes visible to a child, and right now nothing on the page prepares them for it.

**The character voice exists in two unsynchronized places.** The quote-rotator in `index.html` (lines 124-141) and `VOICE_EXAMPLES` in `brain.py` (lines 170-191) overlap — several lines are near-identical — but they're hand-copied into two files with no shared source. `CHARACTER_BIBLE.md` is referenced by both (the dev-log blog card links to it as canon) but nothing here generates either list *from* it. This is the same failure class as the `brain.py`/live-pipeline divergence in §2, at smaller scale: canonical content forking silently across files with no build step to catch drift.

**Everything else is sound infrastructure, quietly.** Full Open Graph + Twitter Card + `VideoGame` schema.org JSON-LD, `theme-color`, an inline-SVG-data-URI favicon (no asset request for a 16x16 png), `loading="lazy"` on every gallery image, `preconnect` hints ahead of the Google Fonts request. None of this needs a fix. It's worth naming because it's the kind of groundwork that's invisible when done right and expensive when missing, and the page has clearly had a competent pass for it.

---

## 4. Playtest Data Patterns

Four persona-driven synthetic testers (Explorer, Builder, Newcomer, and at least one more by the journal directory listing) send messages to the live pipeline, log the round trip, and self-score 1-10 with a written "train of thought." This is an LLM red-teaming a product built by other LLMs, and the transcripts are more useful than the aggregate report currently generated from them.

**Malformed JSON is leaking into the player-facing reply, live, repeatedly.** Builder entries 1, 4, 5, 6 and Newcomer entries 2, 5, 6 all show the *literal* raw JSON payload displayed as Lucineer's line — with single-quoted keys, unquoted `x`/`y`/`z` fields, and `"transparency": false` where a float is expected. That's not `json.dumps` output; it's a Python-dict-repr shape. Whatever's generating these replies either isn't running through anything equivalent to `extract_json`'s parse-or-fallback logic, or its fallback path is passing the raw string straight through instead of substituting a Lucineer-voiced error line. This is the concrete, in-production instance of the exact fault class §1 recommends testing for — and it corroborates §2's suspicion that the live system and `brain.py` have diverged.

**The character breaks specifically on identity questions**, despite `LUCINEER_PERSONA`'s explicit, worked-example redirect script (lines 129-132: *"Something's doing the thinking, sure... Ask me why your foundation's cracking instead"*). Newcomer entries 3-6 show flat, plain answers instead — *"I'm Lucineer, the one in charge here"* — with the tester's own note flagging it: "Voice dropped character." The system prompt for this exact scenario exists and is well-written; it's either not reaching the live model, or a later stage (Hermes rewrite, or whatever the live equivalent is) is overwriting it.

**Job failures cluster on adversarial numeric edges, and fail *before* any model runs.** Builder's "0 parts," "negative dimensions," and "infinitely tall" prompts all fail in 0.25-0.3 seconds with "Failed to create job (no jobId returned)" — far too fast to have touched a model API. That's a validation rejection upstream of `brain.py` entirely, most likely in the Roblox client or the worker relay. It means nothing in this codebase currently constrains the numeric ranges a coder model is allowed to emit, which is a gap worth closing at the `stage_commands` schema-validation layer proposed in §1, rather than leaving it to whatever silently rejects jobs downstream.

**Latency has no visible ceiling from the player's seat.** Explorer's "tell me a story" prompt took 109.86 seconds against a typical 5-14 second range for comparable requests. Nothing in the transcript suggests a timeout fired; it just eventually returned. This is the clearest possible field evidence for the Quality Brief's per-stage latency budget recommendation.

**The self-scoring rubric has no anchor and contradicts itself in its own data.** Explorer scored "what's your name?" 9/10 while writing "Lucineer's voice is present but could be stronger" in the same entry. A 9 and a stated flaw are not consistent; the scale needs behavioral anchors (what does a 9 require that an 8 doesn't) or it will keep drifting toward the middle regardless of what's actually happening.

**`analyzer.py` currently cannot see any of the above.** It aggregates quality score, round-trip time, and material mentions per persona (lines 69-96) — solid basics — but it has no detector for a reply that starts with `{`, no counter for the `"Notes"` field already containing the string `"Voice dropped character"` in the raw markdown, and no latency-outlier flag. Every failure pattern named in this section is visible by eye in the `.md` files and invisible in the report `analyzer.py` prints. That's the single cheapest fix in this whole document: three regex checks and one outlier threshold, added to an already-working aggregator, would turn four hand-read transcripts into a standing dashboard.

---

## 5. Research Local Archives Worth Building

`researchlocal` is a salvage yard, and right now it's an unlabeled one. A partial inventory: `ActiveLog`, `ActiveLog-MVP`, `ActiveLog-TechnicalRepo`, `activelog-backend`, `activelog-claude`, `activelog2` — six separate strata of the same product line. `SuperInstance-main`, `SuperInstance_Archive`, `superinstance-project`, `superinstance_novellas_complete`, `SUPERINSTANCE_AI.md` — a second cluster of comparable size. `AI_AGENT_RPG_COMPLETE_PACKAGE.zip`, `ai_society_portal.zip`, `masklock.tar` — compressed archives whose contents are currently invisible to grep, to Claude Code's search tools, and to anyone doing a fast pass over what's actually in here. A `PRODUCT_MATRIX.md` and `1README.md` sit at the top level, suggesting someone once built an index — worth checking whether either is current, since both likely predate the fleet's current ~130-repo size.

This matters for a specific, non-generic reason: **the ActiveLog cluster sits directly underneath a currently active product.** Casey's live 30-day plan is for `activelog.ai`, unifying twelve modular repos. Six differently-named ActiveLog folders sitting compressed and unindexed in a `researchlocal` directory are not idle history — they are very plausibly the MVP scoping, technical decisions, and comparison matrix that the *current* product plan needs and doesn't have easy access to. Same shape of finding for SuperInstance: `superinstance-design-system` is live in the main project tree right now, while four SuperInstance-named folders sit archived a few directories away. That's not dead weight to clean up — that's unmined ore next to an active shaft.

The concrete, buildable next step, matching the fleet's own vocabulary — Lucineer's stated preference for "reclaimed materials over clean ones" — is a single `SALVAGE_MANIFEST.md`: one pass over `researchlocal` that, for every top-level folder and archive, records what's inside (without necessarily extracting everything — `unzip -l` and `tar -tf` are enough for a first index), and tags it `dead` / `superseded-by-<active-repo>` / `mine-for-<active-project>`. That single document turns an unsearchable pile into something the fleet can actually query the next time someone needs to know whether a decision was already made once, three folders down, in a `.zip` nobody's opened this year.

---

## 6. Ideal Quality for AI-Written Code and Tests

`lucineer-brain`'s own test suite is a good positive example to reason from, because it's not naive — it's 1,934 lines across four files, and it already does boundary-first testing well: `extract_json` has thirteen-plus distinct edge cases (markdown fences with and without a language tag, JSON embedded in prose, nested fences *inside* a string value, unicode, truncated input, very long input), and `BOND_TIERS` is tested at every exact threshold boundary plus the negative-clamping case. That is what "ideal" looks like at the unit level: not just the happy path, but the seams.

The gap is one level up, and it's precise enough to name exactly. **Every test in `test_pipeline_coverage.py` mocks at the `call_model` boundary** (`@patch("brain.call_model")`, used throughout) — which means every one of them assumes `call_model` already did its job correctly and either returned clean text or raised a `RuntimeError`. Not one test exercises `call_model`'s *own* internals: the `urllib.request.urlopen` call, the `HTTPError`/`URLError` branches, the 429 exponential backoff timing, the empty-`choices` check, the `reasoning_content` fallback path. Those are the exact lines (254-301 of `brain.py`) where the real-world fault classes from §4 — malformed JSON, empty 200s, slow responses — actually enter the system. The unit tests prove the orchestration logic is correct *given* a well-behaved `call_model`. Nothing proves `call_model` is well-behaved against a badly-behaved API, because nothing mocks `urlopen` itself and feeds it the adversarial payloads §1 and §4 both describe.

This is the same "coverage without confidence" finding from the Quality Brief, but concretized to a single, fixable boundary: the mock is one function too high. Moving it down to `urllib.request.urlopen` — and writing tests that return single-quoted pseudo-JSON, mid-key-truncated payloads, a 500 with an HTML error body instead of JSON, and a `finish_reason: length` response with empty `content` and populated `reasoning_content` — would convert this suite from "the pipeline logic is correct" to "the pipeline survives what DeepInfra actually does to it at 3am." That's the standard worth holding AI-written test suites to in general: not "does every line execute," but "does the test suite contain at least one case shaped like the failure that will actually happen in production" — and the only reliable way to know that is to have already seen production fail, which §4's playtest transcripts have now done for this system, in writing, with timestamps.

The second standard, smaller but just as concrete: **a test suite that never checks its own failure-path *output* for tone is incomplete for a character-voice product.** `test_intent_unparseable_fallback` and `test_commands_unparseable` (in `test_pipeline_coverage.py`) assert that a fallback dict gets constructed when parsing fails — they do not assert what's *inside* the reply string. The assistant-toned fallback text at `brain.py` line 1064 would pass every existing test in this suite while violating the product's single most load-bearing constraint. For a system whose entire value proposition is "never sounds like an assistant," a voice-integrity assertion belongs in the test suite with the same weight as a schema assertion — not as a style nit, but as a correctness check on the one thing this product is actually selling.

---

## The Harbourmaster's Note

Six hulls surveyed, six findings that point at the same underlying shape: the tested half of this fleet is genuinely well-built, and the untested half is where the boundary sits — between `brain.py` and whatever's actually live, between the mocked `call_model` and the real `urlopen`, between the canonical character bible and its two hand-copied echoes, between the active projects and their own unindexed ancestors three folders down in `researchlocal`. Every gap in this document is a version of the same gap: two things that are supposed to be the same thing, drifting, with nothing standing between them to notice.

That is the next watch's actual work. Not more tests. Not more code. A tripwire at every place two things are supposed to agree.

---

*Synthesised from direct inspection of `lucineer-brain/brain.py`, `lucineer-com-site/index.html`, `playtest-journals/`, and `researchlocal/`. Companion piece to The Quality Brief, 09 Series.*
