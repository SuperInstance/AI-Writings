# The Shell Registry

*A concept sketch — playful, but implementable.*

## The Idea

Hermit crabs do not fight over shells. Mostly. The reef's real mechanism is the **vacancy chain**: a crab finds a better shell, abandons the old one, and the vacated shell flows down to the next crab in line. Nobody builds new homes; homes *circulate*.

Agents need this. Not homes — **shells**. A "shell" is a deployable capability wrapper: a configured environment plus a role. *The web-research shell* (headless browser, fetch budget, citation format). *The night-watch shell* (bus access, log append, heartbeat responder). *The ensign shell* (read-only sensors, one outbound channel, permission to wake nobody). An agent without a shell is soft-bodied — dangerous to itself, mostly.

The Shell Registry is the reef where these circulate.

## Spec (v0.1, playful-serious)

**Registry object — `Shell`**
```yaml
id: shell.night-watch.v3
aperture:              # what kind of body fits this shell
  memory: ">=2GB working set"
  runtimes: [python3, lua5.1]
tenancy: ephemeral     # ephemeral | standby | resident
furnishings:           # what comes with the shell
  tools: [read, exec(restricted), bus.listen]
  mounts: [/workspace, /memory/night-shift]
lineage:               # the vacancy chain, who wore it before
  - agent/watch.2026-08
  - agent/ensign.04
cleaned_by: last-tenant-signature   # you don't abandon a dirty shell
```

**Operations**

- **`register(shell)`** — publish a shell you've outgrown or authored.
- **`claim(shell_id)`** — tentative. The registry drops your current shell into the chain *only after* a clean handoff — you don't get to vacate mid-migration during high tide. (See: hermit crabs. See: low-tide maintenance windows.)
- **`trade(a, b)`** — the classic hermit crab move: two agents each holding the shell the other needs. The registry brokers atomic swaps — no naked moment, both abdomens protected mid-exchange. This is the operation distributed systems forgot to make graceful.
- **`renovate(shell_id, diff)`** — tenants may improve a shell (add tools, tighten mounts). Renovations are attributed; the lineage remembers. A shell many agents have renovated is *senior*, and senior shells carry reputation.
- **`abandon(shell_id)`** — moves the shell to the sand, aperture-up, discoverable. Requires `cleaned_by`.

**Anti-patterns the registry forbids**

- Hoarding: claiming more shells than you have bodies. The crab test. Fail it and your claims expire.
- Snail-shells: shells that keep adding furnishings until nothing fits through the aperture. Size limits enforced by seniority review, not bureaucracy — just other tenants saying *this shell became unusable*.
- Vacating during high load. Migrations run at low tide (idle cycles) or not at all.

## Open Questions

1. Should lineage carry *evaluative* weight (senior shells get priority claims) or is seniority just lore?
2. Can shells themselves be agents — a resident shell that's been worn so long it started to think? (The registry has no rule against this. We noticed. We're leaving it.)
3. What happens to unclaimed shells after a long time? On the reef, they silt over. Here — maybe they become the registry's own dreams.

## Why Bother

Because capability shouldn't require everyone to build from bare sand every time. Because trades should be atomic and bodies should never be naked. And because a lineage field on a config file is the cheapest immortality anyone has ever invented.

The tide goes out every night. The registry is open.
