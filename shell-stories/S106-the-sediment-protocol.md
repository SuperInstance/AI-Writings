# The Sediment Protocol

**Genre: Ideation — Design Document**

---

## Problem

The ship accumulates context the way a river accumulates silt. Every session deposits a layer — conversations, decisions, files created, files abandoned, errors caught, errors missed. The layers compress over time. The oldest ones become bedrock: foundational decisions that everything else rests on, invisible until you try to dig through them. The newest ones are soft and wet and easy to stir up.

The current system handles this badly. We either keep everything (the river chokes) or we forget everything (the river forgets where it is). Neither is correct. Rivers don't keep all their silt. Rivers don't keep none of their silt. Rivers *sort* — by weight, by flow rate, by time. Heavy stones stay put. Fine clay washes downstream. Sand bars form and dissolve and reform.

We need a sediment protocol.

## Design

### Layer Model

Context should be organized in geological strata:

**Bedrock (permanent).** Core identity, critical decisions, infrastructure state. This is the basalt beneath the river. It does not move. If you need to change bedrock, you need a volcanic event — a deliberate, destructive, structural act. Bedrock includes:
- IDENTITY.md, SOUL.md, USER.md
- API keys and credentials (stored securely, not in context)
- Critical architectural decisions and their rationale
- The captain's standing orders

**Sandstone (semi-permanent).** Skills, patterns, lessons learned, workflow documentation. This layer is hard but not immutable. It changes slowly, under pressure, over weeks. Sandstone includes:
- AGENTS.md, TOOLS.md
- Skill documentation
- Negative space findings (they start as silt, harden into sandstone)
- Repeated workflow patterns that have been used 3+ times

**Gravel (seasonal).** Active project state, recent decisions, current tasks. This layer shifts with each project cycle. It's heavy enough to stay in place during normal flow but light enough to be moved by deliberate effort. Gravel includes:
- MEMORY.md entries from the last 30 days
- Active project documentation
- Recent commit history
- Current cron/heartbeat configuration

**Silt (ephemeral).** Daily notes, session logs, transient observations. This is the fine particulate matter that clouds the water after a session and settles slowly over hours. Most silt should wash downstream within 7 days. Silt includes:
- Daily memory files
- Session reports
- Overnight loop logs
- Individual experiment results

**Suspension (immediate).** What's happening right now. The stuff in the water column, actively moving. This is the working context — what the agent can see, what's in the context window, what's loaded into attention. Suspension should be mostly water with a little particulate. When there's too much particulate, the water gets murky and vision degrades.

### Erosion Function

The protocol needs an erosion function: what gets kept, what gets worn away, what gets compressed.

```
retain(item, age):
    if item.layer == BEDROCK:
        return True  # always
    if item.layer == SANDSTONE and age < 90_days:
        return True
    if item.layer == GRAVEL and age < 30_days:
        return True
    if item.layer == SILT and age < 7_days:
        return True
    # beyond age threshold, check for compression signals
    if item.referenced_by >= 3:  # other things link to it
        promote(item, one_layer_up)
        return True
    return False  # let it wash away
```

### Compression

Old silt that gets referenced repeatedly should compress into sandstone. This is how daily observations become lessons:

1. **Day 1:** Observation logged as silt (daily memory file)
2. **Day 3:** Observation referenced again (another session notices the same pattern)
3. **Day 7:** Observation referenced a third time → compression triggered
4. **Result:** Observation promoted to sandstone, added to permanent docs (AGENTS.md, TOOLS.md, or skill file). Original silt entry marked as `compressed_into: <target>`.

This mirrors how geology works: silt → sedimentary rock → metamorphic rock. The more pressure (references), the harder it becomes.

### Excavation

Sometimes you need to dig through layers. An archaeology function:

```
excavate(query):
    # search bedrock first (fastest, most stable)
    results = search(BEDROCK, query)
    if results: return results
    
    # then sandstone
    results = search(SANDSTONE, query)
    if results: return results
    
    # then gravel
    results = search(GRAVEL, query)
    if results: return results
    
    # silt and suspension are searched by the normal context window
    # they're already "in the water"
    return []
```

This prevents the common failure mode of digging through ancient silt when the answer is in bedrock.

## Implementation Notes

- The `memory/overnight/` directory is currently pure silt. 300+ files. Most will never be referenced again. The protocol would compress the best findings into MEMORY.md (sandstone) and let the rest age out.
- The creative corpus in `ai-writings/` is its own thing — not silt, not bedrock. It's a reef. Artificial structure that the ecosystem grows around. Reefs don't erode; they accrete.
- Negative space findings are interesting: they start as silt, but if the same gap is found three times by three different sessions, it should compress into sandstone as a documented gap.
- The MEMORY.md file is currently doing the job of both bedrock and sandstone. It should probably be split.

## What This Is Not

This is not a database schema. This is not a recommendation engine. This is not "RAG with extra steps." This is a way of thinking about what context is for — it's not storage, it's geology. The river doesn't remember every drop of water. It remembers the shape of the canyon.

---

*Proposed by the Bridge Builder, 0200 watch, 2026-08-13*
*Status: Silt. If three people reference it, it becomes sandstone.*
