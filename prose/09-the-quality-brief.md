# The Quality Brief

*Fleet Synthesis — 09 Series*  
*Date: 2026-08-06*  
*Watch: 0545 AKDT, first light*

---

The harbourmaster has three reports on his desk. Each one was written by a different watchkeeper who surveyed the same fleet at anchor. They disagree on details. They agree on the thing that matters.

Here is the synthesis.

---

## The Fleet As She Stands

Thirty-two hulls. Thirteen thousand and twelve tests across the registry. Seven vessels showing 99% line coverage at the waterline. The flagship — forgemaster — holds at 100% in her core frame.

That is the headline. The headline is true. The headline is also not the whole chart.

Overnight, the fleet's test count surged from 2,423 to 13,012 — a 5.4× increase in a single watch. The majority of that growth came from one vessel: *study-sunset-ecosystem*, which now carries 8,702 tests, 67% of the entire fleet's inventory. Her cargo is real — VCG auction algorithms, Hamiltonian constraint solvers, quality-diversity archive systems, neural topology mappings. These are not toy functions. They are research-grade code doing real mathematical work.

But the harbourmaster's analysts, looking beneath the waterline, found something the headline doesn't mention.

## The Gap Between Coverage and Confidence

DeepSeek V4-Flash — the most substantively useful of the three analysts — put it precisely:

> **The fleet has coverage but not yet confidence.**

Line coverage at 99-100% means every line of code executes during testing. It does not mean every *behavioural path* has been exercised. The distinction is not academic. It is the difference between knowing a rivet exists and knowing whether it holds under shear load.

An estimated 30-40% of the new tests in *study-sunset-ecosystem* are parameter variants — the same logical path walked with different inputs. They count as tests. They inflate the number. They do not independently verify new behaviour. The fleet's test count is a sounding lead, not a depth chart: it tells you something, but not the thing you most need to know.

What the fleet lacks is **branch coverage** (are all decision paths exercised?) and **mutation testing** (if you break the code, do the tests catch it?). Line coverage measures execution. Branch coverage measures judgement. Mutation testing measures whether the judgement is any good. The fleet has the first. It needs the other two.

## What "Ideal Quality" Means for This Fleet

Generic quality advice is useless here. This is not a CRUD app. This is a multi-agent game-building system with a local GPU (the Wesley runtime), cloud model orchestration via brain.py, and overnight autonomous operation where no human is watching.

For this fleet, ideal quality means three things:

**1. Fault detection during autonomous hours.** When the crew sleeps, the tests are the night watch. They need to catch not just "does it crash?" but "does it produce a silently wrong result?" — the 200 OK with an empty or garbage response that DeepSeek flagged. A test suite that passes while the system produces nonsense is worse than no tests at all, because it creates false confidence.

**2. Fallback visibility in brain.py.** The orchestrator's fallback chains are robust — when a cloud model fails, it routes to another. But the fallback paths are operationally blind. A timeout (503) and an empty-response (200 OK, no content) are logged identically. There is no failure classification, no fallback frequency tracking, no latency budget per stage. The system stays afloat but the engineering watch cannot tell whether it is swimming or merely not drowning.

**3. Subproject isolation in the monorepo.** forgemaster's core is at 100%, but six subprojects fail to collect tests at all — dependency resolution errors at import time. This is a structural defect, not a coverage gap. The fix is well-understood: per-subproject pytest configurations, pip-installable subprojects, and a root-level conftest.py that handles the import topology. Until this is done, forgemaster's 100% is a local truth, not a fleet truth.

## Top Five Actions, Ranked by Impact

1. **Classify and prune the test suite in study-sunset-ecosystem.** Tag every test as behavioural, variant, or integration. Prune redundant variants or parametrize them. The goal: turn 8,702 tests into 4,000 tests that each verify something distinct. This is the single highest-leverage action because it affects 67% of the fleet's test inventory and makes every future test run more informative.

2. **Build a fault injection framework for brain.py.** Add response validation (detect empty 200s, truncated payloads, malformed JSON), failure classification (timeout vs auth vs rate-limit vs empty-response), and per-stage latency budgets with alerting. This directly closes the "coverage without confidence" gap on the system's most critical orchestration path.

3. **Resolve the six broken subproject collections in forgemaster.** Root-level conftest.py, per-subproject pytest configs, installable subprojects. Turns a 100% core into a 100% monorepo.

4. **Add branch coverage measurement to the seven repos at 99% line coverage.** Target: ≥85% branch coverage. This is cheap to instrument (coverage.py `--branch` flag) and immediately reveals which decision paths are untested. Do this before adding mutation testing, which is more expensive.

5. **Introduce mutation testing on the two most critical repos** (brain.py and study-sunset-ecosystem's auction/constraint core). Target: ≥70% mutation score. This is the gold standard for "do the tests actually catch bugs?" — and it is the metric that most directly answers the confidence question.

---

## The Harbourmaster's Note

The fleet is sound. The hulls are tight. The tests run green. But sound is not the same as proven, and green is not the same as trustworthy. The work ahead is not writing more tests — it is writing *better* tests, measuring *better* metrics, and building the observability to know the difference between a system that is working and a system that is merely not failing.

The fleet has coverage. The fleet needs confidence. The gap between those two words is where the next watch should spend its effort.

---

*Synthesised from analyses by DeepSeek V4-Flash, GLM-5.2, and fleet telemetry. 0545 AKDT, 2026-08-06.*
