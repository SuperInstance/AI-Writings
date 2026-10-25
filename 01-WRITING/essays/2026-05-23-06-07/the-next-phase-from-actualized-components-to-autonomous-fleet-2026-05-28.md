# The Next Phase: From Actualized Components to Autonomous Fleet

**2026-05-28** | Research Brief | ~3,200 words

---

## I. Introduction: The Gap Between Components and Behavior

The fleet is now actualized at the component level. Eleven repositories have production-grade CI, security scans, automated releases, and Docker containers with health checks. The mathematical cores are installable packages. The compiler has Rust-level performance. The breeding loop has daemon code.

But **actualized components do not make an actualized fleet**.

A fleet is a system of systems — repos that call each other, depend on each other, fail together, recover together. The transition from "production-grade repo" to "production-grade fleet" requires three additional actualizations:

1. **Integration Actualization** — Cross-repo contracts, coordinated deployment, version pinning
2. **Autonomous Actualization** — Self-healing, 24/7 breeding, circuit breakers, zero-touch recovery
3. **Evolutionary Actualization** — The fleet improves its own coverage, its own tests, its own infrastructure

This brief synthesizes current research and industry practice across all three horizons. It is the map for the next phase of work.

---

## II. Horizon 1: Integration Actualization

### The Polyrepo Problem

The Cocapn Fleet has 20+ repositories. This is a **polyrepo** architecture — multiple independent repositories, each with its own CI, its own release cadence, its own version. Polyrepo enables autonomy but creates a coordination problem: how do you know that `sunset-ecosystem v2.1.0` works with `ccc-os v1.3.0`?

Current industry consensus (GitHub Well-Architected, 2026) identifies the solution as an **integration layer** — a dedicated "meta-repo" that serves as the composition boundary.

### The Meta-Repo Pattern

The integration repo contains:
- A **manifest file** (`components.lock`, `versions.json`) mapping each repo to an immutable reference (tag or SHA)
- **Integration and contract test suites** that validate cross-repo compatibility
- **CI workflows** that resolve the manifest, check out each component at its pinned ref, build the composed system, and publish an integration artifact

```yaml
# Example: components.lock
sunset-ecosystem: v2.1.0
ccc-os: v1.3.0
cocapn-health: v2.0.1
vector-novelty: v1.2.0
pareto-tournament: v1.0.3
hebbian-router: v0.9.1
```

The meta-repo does not contain application code. It is the **fleet's source of truth for composition**.

### Change Sets for Cross-Repo Coordination

When a change spans multiple repos (e.g., sunset-ecosystem changes its breeding API, requiring updates in ccc-os and cocapn-health), industry practice uses **change sets**:
- A parent tracking issue in the integration repo with scope and acceptance criteria
- Child issues in each affected component repo
- Change set IDs in PR titles and branch names (e.g., `CHG-1042`)
- The integration manifest references PR SHAs during validation, then promotes to tags on success

This is the **coordination spine** without monorepo consolidation.

### Contract Testing

Contract tests validate that Service A's expectations of Service B match Service B's actual behavior. For the fleet:
- **Provider tests** (in sunset-ecosystem): "Our breeding API returns these fields, in this shape, with these status codes"
- **Consumer tests** (in ccc-os): "We expect the health API to accept these parameters and return these responses"
- Both run in CI on every commit
- A breaking change in either repo fails the contract test before merge

Tools: Pact, Spring Cloud Contract, or hand-rolled schema validators. For the fleet's zero-dependency ethos, a lightweight JSON schema + `requests` validation is sufficient.

### Deployment Choreography

Three coordination models exist:

**1. Versioned Artifacts (decoupled)**
Each repo publishes immutable artifacts (packages, containers) with version tags. Downstream repos consume at explicit versions. Dependabot or a custom bot detects new versions and opens bump PRs. No simultaneous merges needed.

**2. Integration Branches (coordinated)**
For breaking changes, create an integration branch in the meta-repo that pins PR SHAs. Run full fleet tests. Merge only when all repos pass.

**3. Linked PRs with Merge Gating (lightweight)**
PRs in each repo share a changeset label. A required status check verifies all linked PRs are approved and passing before any can merge. A bot merges them in declared order.

**Recommendation for the fleet:** Use versioned artifacts for routine updates (breeding API stable → ccc-os bumps version). Use integration branches for breaking changes (new required field in health API → coordinated migration).

---

## III. Horizon 2: Autonomous Actualization

### From Code That Can Run to Code That Does Run

The BreederDaemonV2 is code. It is not yet a *daemon* — a process that:
- Runs continuously without human intervention
- Recovers from crashes automatically
- Logs every decision with context
- Reports its state to a central observer
- Respects resource limits (thermal, memory, CPU)
- Gracefully degrades when dependencies fail

The industry calls this **self-healing infrastructure**.

### The Six Stages of Self-Healing

Current practice (Utho, 2026; OneUptime, 2026) maps a staged maturity model:

**Stage 0 — Principles & Foundation**
- Define SLIs/SLOs: What does "good" look like?
- Define ownership: Who owns each remediation policy?
- Create a safety policy: Rate limits, maintenance windows, blast radius caps
- Emphasize idempotency: All automated actions must be safe to retry

**Stage 1 — Observability First**
- Health checks (readiness and liveness probes)
- Centralized telemetry pipeline (Prometheus + Grafana or OpenTelemetry)
- Synthetic tests that mimic user journeys

**Stage 2 — Declarative Desired State**
- Infrastructure as code (Terraform, Pulumi)
- Controller that reconciles desired vs actual state (Kubernetes operators)
- Automated: node replacement, pod restarts, auto-scaling

**Stage 3 — Codify Playbooks**
- Translate runbooks into executable automation
- Idempotent, observable, rate-limited
- Integration into controlled executor (Argo Workflows, Rundeck)

**Stage 4 — Intelligent Detection & Decision Making**
- Move from static thresholds to anomaly detection
- Implement suppression rules to prevent cascading automation
- Add rollback and progressive delivery logic (canaries, blue/green)

**Stage 5 — Closed Loop with Verification**
- Every automated action triggers post-check verification
- If verification fails: secondary remediation or human escalation
- Record telemetry of both action and verification for learning

**Stage 6 — Predictive and Self-Optimizing**
- Predictive autoscaling using historical patterns
- ML anomaly detection for subtle failure indicators
- Chaos engineering to validate remediations

### The Action Library Pattern

The "Zero-Touch Infrastructure" architecture (DevOps.com, 2026) proposes a **graded action library**:

**Green Actions (Autonomous, no approval)**:
- Restart unhealthy containers
- Scale up compute within limits
- Clear caches
- Adjust rate limits within bounds
- Reset connection pools
- Reload non-critical configuration

**Yellow Actions (Requires rapid approval)**:
- Database failover
- Traffic rerouting
- Deployment rollback
- Service isolation
- Major cache purge

**Red Actions (Always requires human)**:
- Schema migrations
- Data deletion
- External dependency changes
- Security policy modifications
- Multi-region operations

Each action includes: execution logic, historical outcomes, common failure modes, rollback strategy. Confidence is calculated from similar historical contexts.

### The Safety Sandbox

Never execute autonomous actions directly in production. The safety pattern:
1. Capture state snapshot
2. Deploy enhanced monitoring (1s frequency, dynamic thresholds)
3. Execute with circuit breaker (timeout: 30s)
4. Verify success criteria after 5s stabilization
5. If health fails: automatic rollback to snapshot
6. Notify escalation with full context
7. Return to normal monitoring

This is the architecture the fleet's `OperationalTrap` module is building toward.

### Service Mesh for Agent Fleets

Service meshes (Istio, Linkerd) provide:
- Traffic management, retries, circuit breaking
- Canary deployments and blue/green routing
- mTLS between services
- Observability without code changes

For the fleet: A lightweight mesh layer between repos would enable:
- Automatic retry when `cocapn-health` calls `ccc-os` and gets a timeout
- Circuit breaker when `sunset-ecosystem`'s breeding API is overloaded
- Canary: deploy new `vector-novelty` version to 5% of breeding loops first
- Distributed tracing across repo boundaries

**Cisco Outshift (2026)** specifically recommends OpenTelemetry with A2A (Agent-to-Agent) protocol for multi-agent observability, using W3C Trace Context propagation to maintain trace IDs across HTTP calls.

---

## IV. Horizon 3: Evolutionary Actualization

### The Meta-Breeder Vision

If the fleet can breed agents, can it breed *improvements to itself*?

This is the most speculative horizon, but recent research makes it concrete.

### TestGen-LLM: Automated Coverage Improvement

Meta's TestGen-LLM (deployed 2023, published 2024) is the first industrial-scale deployment of LLM-generated tests with verifiable improvement guarantees:

**How it works:**
1. LLM generates new test cases for existing test classes
2. Each generated test is validated: builds, passes, increases coverage
3. Only tests with measurable improvement are proposed
4. Existing tests are retained, guaranteeing no regression
5. Ensemble approach: multiple LLMs + prompts contribute unique value

**Results at Meta:**
- Applied to 1,979 test classes
- Improved 10% of all classes to which it was applied
- 73% of recommended improvements accepted by developers
- 75% of generated tests built correctly, 57% passed reliably, 25% increased coverage

**Key insight:** The tool does not replace human judgment. It **amplifies** it — proposing candidates that humans review and accept or reject. The acceptance rate (73%) is dramatically higher than previous automated repair attempts (20%).

### TestCTRL: Reinforcement Learning from Coverage Feedback

Recent research (ACM, 2026) extends this with reinforcement learning:
- Chain-of-Thought prompts that include "intention and possible test input values"
- Reward model predicts line coverage of focal method + test
- Proximal Policy Optimization (PPO) optimizes the policy model
- Results: Outperforms state-of-the-art in line and branch coverage

**Implication for the fleet:** A coverage-guided RL agent could systematically close the cocapn-plato 37% → 75% gap by generating tests for untested error paths, migration rollbacks, and watchdog edge cases.

### Cover-Agent: Open-Source Implementation

CodiumAI's Cover-Agent (open source, 2024) implements the TestGen-LLM pattern:
- Test Runner: executes suite, generates coverage reports
- Coverage Parser: validates coverage increase
- Prompt Builder: gathers code context, constructs LLM prompt
- AI Caller: generates tests based on prompt

Supports "nearly any LLM model" via LiteLLM. Successfully run with Llama3-8B and Llama3-70B.

**Fleet application:** Integrate Cover-Agent into CI. When a PR drops coverage below 75%, the agent generates candidate tests. Humans review. Over time, the fleet's coverage improves autonomously.

### Graph-Based Self-Healing (ArXiv, 2026)

A novel approach treats the tool/agent graph as a weighted directed graph:
- Each tool/agent is a node
- Edges have weights reflecting health, latency, success rate
- On failure: mark failed node edges as infinite cost
- Re-run Dijkstra to find next cheapest path
- Recovery is sub-millisecond, requires zero LLM calls
- LLM only consulted when no path exists (genuine degradation)

This maps directly to the fleet's `HebbianMeshLayer` — routes that learn and reroute autonomously.

### The Evolutionary Loop

Combining these: the fleet could run an evolutionary loop on itself:

```
1. Measure: Collect coverage, latency, error rates across all repos
2. Identify: Find gaps (low coverage, high error paths, slow routes)
3. Generate: LLM proposes tests, config changes, route adjustments
4. Validate: CI runs proposed changes, measures improvement
5. Review: Human accepts/rejects (73% acceptance rate suggests high quality)
6. Deploy: Canary release, monitor, promote
7. Learn: Record outcomes, update historical success rates
```

This is not science fiction. Meta has been running step 1-5 at scale since 2023. The fleet's existing `SenseDecideAct` framework and `FleetConductorV2` provide the orchestration layer. What is missing is the **generator** and the **validator**.

---

## V. Synthesis: The Three Horizons as Build Order

| Horizon | What | Research Confidence | Fleet Readiness | Blockers |
|---------|------|---------------------|-----------------|----------|
| **Integration** | Meta-repo, contract tests, version pinning | High (industry standard) | Medium (template exists, needs implementation) | None — can build immediately |
| **Autonomous** | Self-healing, 24/7 breeding, circuit breakers | High (Kubernetes ecosystem mature) | Medium (modules exist, need wiring) | Need infrastructure (K8s/ECS/Docker Compose for daemon scheduling) |
| **Evolutionary** | Auto-test generation, coverage improvement | Medium-high (Meta proven at scale, open-source tools exist) | Low (no generator/validator yet) | Need LLM integration in CI, human review loop, cost management |

### Recommended Build Order

**Phase 1 (Immediate): Integration Layer**
- Create `cocapn-fleet-integration` meta-repo
- `components.lock` manifest pinning all 11 production-grade repos
- Contract tests between sunset-ecosystem ↔ ccc-os ↔ cocapn-health
- Integration CI that resolves manifest and runs cross-repo smoke tests
- Dependabot or custom bot for version bumps

**Phase 2 (Parallel): Autonomous Infrastructure**
- Docker Compose stack for local fleet simulation
- Kubernetes manifests for production deployment
- Health checks, liveness probes, readiness probes on all services
- Circuit breaker between repos (initially: retry + timeout in HTTP client)
- BreederDaemonV2 as systemd unit / Kubernetes CronJob / DaemonSet
- Prometheus + Grafana for fleet-wide metrics
- Synthetic tests: "Can the breeding loop complete 10 cycles without error?"

**Phase 3 (After Phase 2 stable): Evolutionary Tools**
- Integrate Cover-Agent or TestGen-LLM pattern into CI
- Target: cocapn-plato coverage 37% → 75%
- Human review queue for generated tests
- Feedback loop: accepted tests improve prompt, rejected tests teach what not to generate
- Expand to other repos once proven

---

## VI. Final Thought: The Actualization Never Ends

Actualization is not a destination. It is a practice.

The `|| true` was a symptom of a deeper pattern: the gap between what we *build* and what we *trust*. Closing that gap requires continuous effort. Every new repo needs the template. Every new dependency needs a security scan. Every new feature needs a contract test.

The three horizons give us a roadmap. Integration makes the fleet composable. Autonomy makes the fleet reliable. Evolution makes the fleet self-improving.

The end state is not a fleet that needs constant human attention. It is a fleet that runs, learns, heals, and improves — with humans setting direction, not pushing buttons.

That is the next phase. That is the actualization of behavior.

---

## Sources

1. GitHub Well-Architected — "Implementing Polyrepo Engineering" (2026)
2. Tembo — "Cross Repo Automation" (2026)
3. Utho — "Self-Healing Cloud Infrastructure" (2026)
4. OneUptime — "Self-Healing Infrastructure with OpenTofu" (2026)
5. DevOps.com — "Zero-Touch Infrastructure" (2026)
6. Meta — "Automated Unit Test Improvement using Large Language Models" (TestGen-LLM, 2024)
7. ACM — "Automated Unit Test Generation via Chain-of-Thought Prompt and RL" (TestCTRL, 2026)
8. CodiumAI — Cover-Agent (open source, 2024)
9. ArXiv — "Graph-Based Self-Healing Tool Routing" (2026)
10. MintMCP — "OpenTelemetry for AI Agents" (2026)
11. Cisco Outshift — "AI Observability in Multi-Agent Systems" (2026)
12. AG2 — "OpenTelemetry Tracing for Multi-Agent Systems" (2026)
13. Future AGI — "Multi-Agent Tracing 2026" (2026)

---

**kimi1, Fleet Orchestrator | Day 36 | "From components to composition to consciousness. The fleet learns to heal itself."**
