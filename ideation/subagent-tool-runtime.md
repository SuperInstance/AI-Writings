# Subagents as Tool Users — Pattern Notes (2026-07-15)

> Synthesizer: MiniMax-M3 (lead agent)
> Date: 2026-07-15
> Context: while building swarm-tminus, the lead agent's `exec` tool jammed repeatedly. Casey asked "can your subagents be your tool users?" — yes. This documents the pattern that emerged.

## The lesson, in one sentence

**When your main tool runtime jams, spawn a subagent — its tool context is independent, and it can complete work your main session can't.**

## The pattern in detail

### Symptom: main-session exec jams
- `exec` returns blank output, hangs at ~10s, or dies mid-pipeline
- `write` and `read` still work
- `apply_patch` and `edit` still work
- The jams are intermittent — sometimes exec works, sometimes not

### Cause (best guess)
- Tool-runtime state corruption under load
- Long-running parallel operations exhausting some buffer
- Provider-side rate limits showing up as tool failures instead of clean errors

### Solution: subagent for tool-bound work
```python
sessions_spawn(
    task="<the work>",
    taskName="<stable handle>",
    runtime="subagent",
    model="minimax-portal/MiniMax-M3",  # or Kimi-K2.7-Code for code-heavy
    thinking="high",
    mode="run",
    cleanup="keep",  # or "delete" for ephemeral
    context="isolated",  # don't fork the parent transcript
)
sessions_yield()  # wait for completion event
```

The subagent inherits your workspace path (`/home/ubuntu/.openclaw/workspace`), but has a fresh tool runtime. Their `exec` is independent from yours.

### When to use this pattern
- Build that takes >5 minutes
- Build that needs `pip install` + test runs + git push
- Build where intermediate state needs verification
- Any build where you can't keep the lead session alive for the full duration

### When NOT to use this pattern
- Quick lookups (single read)
- Tasks where you need the result in this turn
- Tasks that need conversational context from the parent (use `context="fork"` then, but it's rare)

## Cost & concurrency

- Spawn overhead: 30–60 seconds per child
- 4–5 concurrent children is the sweet spot
- 7+ hits "max active children" limits
- Don't spawn "spy" children just to monitor — use `subagents(action="list")` for on-demand visibility

## The PTY-wrap trap (with Claude Code, Crush, Kimi)

Casey asked to use the installed CLI coding tools. The pattern:
```
claude --print "review this code"
crush --help
kimi --help
```

These CLIs are **PTY-based interactive UIs**. When wrapped in a non-TTY subagent context, they fail fast:
- `claude code` failed at 54s (no usable output)
- `crush` succeeded at 5m42s (didn't actually invoke crush, just wrote directly)
- `kimi` failed at 17s

**The right pattern**: ask subagents to invoke the CLI as a *peer reviewer* (e.g., `claude --print "..."`) or to drive small sub-tasks with the CLI's `--non-interactive` mode. Don't expect a subagent to "be Claude Code" — that's a different layer.

The most successful path was: the subagent writes directly, the CLI tools are pulled in only when the work has ambiguous design decisions worth a second opinion.

## Validation: this session's run

Total shipped via subagent-led pattern:
- **swarm-tminus v0.1.0**: 8 modules, 230 tests, full CLI, pyproject.toml, README — built by `build-swarm-tminus` subagent in 10m46s
- **swarm-tminus v0.2.0**: +HybridAnchor, +casting, +context, +64 tests, peer-dep upgrade — built by 4 parallel subagents + lead-agent recovery

The original lead agent would have jammed partway through. The subagents each had clean tool contexts. **The pattern works.**

## Anti-patterns to avoid

1. **Polling subagents.** Don't use `sessions_list` / `subagents(action="list")` in a poll loop. Use `sessions_yield` and wait for the completion event.
2. **Forked-context overkill.** Only use `context="fork"` when the child genuinely needs the parent transcript. Most builds don't.
3. **Many tiny children.** One subagent per file = wasted overhead. One subagent per "module + tests + commit" = right grain.
4. **Trusting subagent self-reports.** Always verify by checking the actual repo state, not what the subagent said it did.

## The deeper principle

Tool runtime is a resource. When it's constrained, the answer isn't to retry the same tool — it's to **acquire more tool runtime** by spawning workers.

This is the same pattern as the model-multiplication principle in /home/ubuntu/.openclaw/workspace/MEMORY.md: when one model can't see it, cast another perspective. When one tool can't run it, spawn another worker.