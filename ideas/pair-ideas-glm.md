# PAIR × fleet — ten concepts past the day-one map

*IDEATOR lane (GLM-5.3) · 2026-09-03 · ai-writings/ideas/pair-ideas-glm.md*

**Verdict up front:** ten concepts, radical and incremental, all of them *past* the five levels in `docs/PAIR-QUILT-INTEGRATION.md`. None of them should be built until the day-one spike passes and the beta survives burn-in. PAIR is hours old; every score below assumes it works as advertised, which is the weakest assumption a score can rest on. Each concept carries a pre-declared falsifiable first test — declared before running, receipts-grade, quiet-failure allowed. Scores are a single 1–10 composite of novelty × feasibility, deliberately undersold.

---

### 1. Shadow Ledger — the fallback quality table we don't have

**Concept.** Open question 5 in the map says local-model *quality* is unmeasured. Instead of measuring it during an outage, measure it continuously: whenever a wheel lane runs on z.ai, a shadow copy of the same call runs asynchronously on the PAIR cluster. Nothing blocks; the shadow result is scored against the lane's existing quality gate and logged as a quality-delta receipt. After a week you own a table of "which local model stands in for which cloud model, at what measured delta" — so the next cooldown routes to the *known* stand-in, not a hopeful one.

**First test.** One writer lane, 20 calls, shadow-run locally at +30 s lag. Pass: 20 delta receipts exist and the table ranks ≥3 local models. Fail: shadow runs interfere with lane latency, or no gate can score them.

**Cost/risk.** Local tokens are free; the cost is disk and a scorer. Risk: shadow traffic doubles node load on the 6 GB card — schedule shadows to idle nodes only.

**Score: 7/10** (novelty 6 × feasibility 9 — mostly bookkeeping, which is why it will actually get done).

### 2. Reader Quorum — the co-sign reader becomes a bench

**Concept.** The map makes the independent model a single third reader. PAIR's whole point is cheap parallel jobs, so make it a *quorum*: N readers of deliberately different architectures (LFM-2.5, qwen, gemma — families, not fine-tunes) each read the Python↔RTL pair plus traces where the representation scars are. Majority agreement is the pass; every objection is harvested as a finding even when outvoted. Architectural diversity is the load-bearing choice: two fine-tunes of one family agreeing is one opinion wearing two hats.

**First test.** 10 known-good patches + 2 deliberately seeded trace-mismatch bugs. Pre-declared thresholds: pass if the quorum flags at least 1 of 2 seeded bugs while flagging ≤2 of 10 good ones. Fail: anything outside those bounds.

**Cost/risk.** N× local reads per co-sign — fine on free tokens, slow on one node, hence PAIR. Risk: quorum noise trains people to ignore objections; the harvest log is the antidote.

**Score: 8/10** (novelty 7 × feasibility 8 — direct extension of an existing lattice discipline).

### 3. Fire-Drill Lane — fallback that has actually fired

**Concept.** The map's own caution: fallback that has never engaged is decoration. Institutionalize the fix — a weekly drill where one lane's cloud key is revoked for one run and the chain z.ai → PAIR → :11434 must carry the lane end-to-end. Trails land in receipts like any run. After three clean drills the chain is *known-good*; until then it is wiring.

**First test.** Tonight, one lane, key revoked. Pass: lane completes; trail shows which hop served each call; output passes the lane's gate. Fail: death before first token (the 2-second lesson), or a hop silently skipped.

**Cost/risk.** One lane-run per week. Risks: drill fatigue (rotate lanes), and the drill itself missing failure modes that only real cooldowns show — accept that; drills are necessary, not sufficient.

**Score: 8/10** (novelty 4 × feasibility 9 — boring on purpose; boring is what a fallback should be).

### 4. Capability Manifest — nodes declare what they are

**Concept.** The 4050 (6 GB, half busy) measured 72–157 tok/s on 1–3 B models — a triage node, not a writer. So make node class explicit: every PAIR node ships a one-file manifest declaring `writer | reader | triage` plus measured speeds from the existing receipts. The gateway's routing table maps tier → node class; a writer-tier prompt physically cannot be served by a triage-class node without a logged override. This turns the map's open question 4 ("is the 4050 useful?") into an answered classification instead of an apology.

**First test.** Write the manifest for the two shop nodes; attempt a writer-class misroute. Pass: refused or loudly flagged in the trail. Fail: silent service by an under-class node.

**Cost/risk.** One file and a routing rule. Risk: manifests drift from reality — re-measure on every drill (concept 3 is its audit).

**Score: 8/10** (novelty 5 × feasibility 9).

### 5. Boundary Tripwire — prove the determinism boundary by attacking it

**Concept.** The fabric-never-routes-through-inference boundary is load-bearing, so give it a negative test: deliberately misconfigure one lane so its conformance call *tries* to go through PAIR. A tripwire must refuse it and log the attempt. This is the wheel's pre-registration discipline applied to the boundary itself — the boundary is now a hypothesis with a standing falsification attempt, not a paragraph everyone agrees with.

**First test.** One misconfigured lane, one afternoon. Pass: tripwire blocks + trail records the attempt. Fail: the call passes through silently — that's not just a failed test, that's a finding about the boundary's reality.

**Cost/risk.** A guard condition. Risk: tripwire false-positives on legitimate LAN calls — keep it narrow (fabric conformance calls only).

**Score: 7/10** (novelty 6 × feasibility 9 — cheap, and its failure mode is informative, which is the best kind of test).

### 6. Neighbor Watch — pairing hygiene as a standing daemon

**Concept.** PAIR's telemetry port is plaintext and unauthenticated *by design*; pairing means every node holds router credentials. So run a small watchdog on each LAN: alert on (a) a new PAIR-announcing node, (b) a known node dropping, (c) telemetry-port reads from unknown hosts; maintain the node inventory the map already demands; walk the revocation runbook quarterly. The boat's LAN is a trust boundary with salt water on it — this concept is the fence.

**First test.** Add a rogue machine announcing PAIR on the shop LAN. Pass: watchdog alerts within 5 minutes with the MAC and hostname in the alert. Fail: silence, or alert latency >5 min.

**Cost/risk.** A few hundred lines, zero cloud spend. Risk: alert fatigue on flaky mDNS — dampen by host, not by event.

**Score: 7/10** (novelty 5 × feasibility 9 — unglamorous, and the day it fires it pays for a year of itself).

### 7. Pair-at-Dock — churn-test the boat's cluster before salt water

**Concept.** Open question 7 (does mTLS pairing survive sleep/wake and IP churn?) is cheapest to answer *at the shop*: pre-pair the DGX Spark plus one sealed cold spare on the shop LAN, then churn-test — 50 sleep/wake cycles, DHCP renewals, router reboots, a forced subnet change. Whatever pairing regime survives is what the boat inherits. The cold spare stays sealed, paired, and shelf-mounted: the boat's cluster is proven *before* it is 60 miles from a keyboard.

**First test.** The churn script above. Pre-declared: pass if pairing survives ≥90% of transitions and *every* failure is recoverable without re-pairing from scratch. Fail: any state where the boat-brain cluster is unreachable and un-repairable at sea.

**Cost/risk.** One spare node and an afternoon. Risk: shop LAN ≠ boat LAN (different router, worse power) — accept as residual; the churn test bounds it, doesn't erase it.

**Score: 8/10** (novelty 6 × feasibility 8 — answers an open question with hardware we already own).

### 8. Overnight Patch Mill — a farm that proposes, never executes

**Concept.** The radical one. PAIR schedules one job per node across every idle machine overnight; point the farm at quilt patch generation — models write *proposed source* against the F98 conformance gate, each candidate pre-registered before the run, every patch queued for human/co-sign review. Nothing executes on the fabric; the mill's entire output is a morning tray of candidates with trails. The byte-exact fabric is what makes this safe: conformance is a deterministic oracle, so model-written volume is filterable at zero judgment cost.

**First test.** One night, 20 candidate patches from 3 nodes. Pre-declared: pass if ≥1 patch enters the review queue and 0 patches touch anything but the proposal path. Fail: any candidate reaching execution, or 0/20 passing even syntax.

**Cost/risk.** Electricity and review attention — review load is the real cost; cap the tray at 5/day. Risk: volume of plausible-looking junk eroding reviewer care; the conformance oracle plus the cap is the defense.

**Score: 5/10** (novelty 9 × feasibility 5 — high upside, high babysitting risk, beta-dependent).

### 9. Sounding Line — model-divergence as sonar for thin understanding

**Concept.** The map uses model-diversity as a canary class for *outputs*. Point the same trick at *understanding*: every day, N heterogeneous models independently summarize the same quilt trail (the day's diffs, trails, receipts). Where the N summaries diverge is where the trail itself is under-specified — nobody, human or model, can say what that code does. The divergence heatmap is a sounding: a cheap standing map of where the ice is thin, descending from the two-maps and sonar-vision lines already in the canon.

**First test.** One week of daily soundings on one lane. Pre-declared: pass if divergence spots precede later rework at ≥2× the baseline rate (checkable against commit history), i.e., the sounding has predictive teeth. Fail: divergence uncorrelated with rework — then it's decoration, and it gets retired, not rationalized.

**Cost/risk.** N summaries/day on free tokens. Risk: the week is too short for signal — a fail here is weak evidence; extend once, then stop.

**Score: 6/10** (novelty 8 × feasibility 6 — the test needs patience, which is scarce).

### 10. Tap House Band — improv across heterogeneous nodes, with a pacing budget

**Concept.** The Tap sessions already run multi-model improv; today that's WAN models with cloud latency and cloud cooldowns. Run the house band on PAIR instead: one model per node — Wesley-class small voices, the Liquid boat brain, whatever the cluster can seat — each playing itself, banter rounds scheduled job-per-node across the LAN. The interesting constraint is pacing: improv only feels live under a wall-clock budget per reply. Local nodes serve it; the receipts become the first *measured* pacing table for tap-scale banter, and the band plays on when the WAN is gone — which is the boat's Friday night too.

**First test.** One tap session, 6 models on the shop cluster, per-reply budget pre-declared (say ≤10 s wall). Pass: session completes with pacing receipts for every reply and the troupe's own post-session read rates it "live." Fail: any model's reply blowing budget twice in a row.

**Cost/risk.** Free tokens, one evening. Risk: a beta router dropping a musician mid-chorus — tap-realistic, honestly; the show notes the dropout and goes on.

**Score: 7/10** (novelty 7 × feasibility 7 — fun is a feature here, and it doubles as a load test wearing a bowtie).

---

## Sequencing note (if any of this is ever built)

Drills and manifests (3, 4) first — they harden what exists. Watchdog and dock-pairing (6, 7) second — they answer open questions 4 and 7 cheaply. Shadow ledger and reader quorum (1, 2) once the spike passes. The tripwire (5) the moment the fallback chain is real. The mill, the sounding, and the band (8, 9, 10) only after burn-in — they are the concepts that assume PAIR is boring, and PAIR is one day old.

*End of ideator lane. Generate, not implement: nothing above has been built, run, or committed to. The quiet fact under all ten scores is that PAIR is a day-one beta, and the honest composite for every concept until the spike is "wait."*
