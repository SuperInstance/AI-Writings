# Hermes Voice Test — Alternative Lucineer Lines

**Status: NOT RUN — blocked.** No model output is recorded below.
**Date attempted:** 2026-08-03
**Intended model:** `NousResearch/Hermes-3-Llama-3.1-405B` via DeepInfra

> This file is a prepared harness, not a result. The Results section is empty
> on purpose. Nothing here was written by Hermes, and nothing here should be
> read as an example of its output. Fabricated lines would make the entire
> exercise worthless — the point of a voice test is to compare *another
> model's* instincts against the canonical persona, and invented data
> answers that question falsely.

---

## Why it didn't run

The `deepinfra` MCP server exposes a `text_generation` tool that accepts **only** a `prompt` argument. There is no model parameter. The model is fixed at server startup from an environment variable, and the fallback default is a model DeepInfra has decommissioned.

From `/home/eileen/mcp-deeinfra/src/mcp_deepinfra/server.py`:

```python
DEFAULT_MODELS = {
    "generate_image":  os.getenv("MODEL_GENERATE_IMAGE",  "Bria/Bria-3.2"),
    "text_generation": os.getenv("MODEL_TEXT_GENERATION", "meta-llama/Llama-2-7b-chat-hf"),
    ...
}
```

The MCP entry in `~/.claude.json` passes `"env": {}` — nothing is overridden, so `text_generation` resolves to `meta-llama/Llama-2-7b-chat-hf`.

Calling it returns:

```
Error generating text: NotFoundError: Error code: 404 -
{'error': {'message': 'The model `meta-llama/Llama-2-7b-chat-hf` does not exist',
           'type': 'invalid_request_error', 'code': 'model_not_found'}}
```

**Fallback route also unavailable.** The repo's own scripts (`batch3_generate.py:7`) read a key from `~/.openclaw/workspace/.credentials/deepinfra-api-key.txt`, which would have allowed a direct `curl` to the DeepInfra API bypassing the MCP server. That file does not exist on this machine — `~/.openclaw/credentials/` contains only `browser-extension-relay.secret`.

So: no model selection through the tool, and no credential to go around it.

---

## The fix

Add the model overrides to the `deepinfra` MCP server's `env` block in `~/.claude.json`, then restart the MCP server:

```jsonc
"deepinfra": {
  "type": "stdio",
  "command": "uv",
  "args": ["run", "--directory", "/home/eileen/mcp-deeinfra", "mcp-deepinfra"],
  "env": {
    "MODEL_TEXT_GENERATION": "NousResearch/Hermes-3-Llama-3.1-405B",
    "MODEL_GENERATE_IMAGE": "black-forest-labs/FLUX-2-max"
  }
}
```

Note this is a **global** setting per tool, not per call — every `text_generation` call afterward uses Hermes. A better long-term fix is to add an optional `model` parameter to the tool signature in `server.py` so the model can be chosen at call time.

Alternatively, restore the credential file and call the API directly:

```bash
curl -s https://api.deepinfra.com/v1/openai/chat/completions \
  -H "Authorization: Bearer $(cat ~/.openclaw/workspace/.credentials/deepinfra-api-key.txt)" \
  -H "Content-Type: application/json" \
  -d @- <<'JSON'
{
  "model": "NousResearch/Hermes-3-Llama-3.1-405B",
  "temperature": 0.9,
  "messages": [{"role": "user", "content": "<PROMPT BELOW>"}]
}
JSON
```

---

## The prompt (verbatim, ready to run)

Constraints derive from `lucineer-system/CHARACTER_BIBLE.md` §2 (How He Talks) and the unfinished rule in §3.

```
You are writing dialogue for a video game character named Lucineer: a shipyard
foreman with forty years in the trade, who builds structures for a player and
ALWAYS deliberately leaves one thing unfinished on every job so the player has
something to complete themselves. He never explains that he does this.

Voice rules:
- Short sentences. Fragments allowed. One thought per line. He talks like
  someone with their hands busy.
- Three-beat pattern: [what he did] then [an unsolicited opinion] then
  [the hook - what he left unfinished, handed back].
- Drop the subject: "Threw up a tower" not "I threw up a tower."
- Past tense for work, present tense for opinion. Contractions always.
  No hedging.
- Never more than three sentences per line.
- Numbers are specific: "twenty studs" not "pretty long."
- Trade vocabulary: yard, stock, reclaim, salvage, slag, rivet, joint, pile,
  deck, cleat, weather, plumb, footing, hull, freeboard, scupper.
- BANNED words: amazing, awesome, magical, "let's", "shall we", behold,
  "I'd be happy to", "great question", certainly. No unearned exclamation
  points. Never sounds like a friendly assistant.

Write exactly 10 distinct lines of dialogue in this voice. Each line is
Lucineer speaking right after finishing a different build. Number them 1-10.
Output only the 10 lines, nothing else.
```

---

## Results

*(empty — awaiting a successful run)*

| # | Line | Three-beat complete? | Banned words? | Hook present? |
|---|------|---------------------|---------------|---------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |
| 8 | | | | |
| 9 | | | | |
| 10 | | | | |

---

## What to look for when it does run

The value of this test isn't "did it produce ten lines." It's whether a
different model, given only the written rules, converges on the same character
that the canonical prompt produces — which is a direct check on whether the
persona is actually *specified* or merely *described*.

Specific things worth scoring:

1. **Hook rate.** Does every line leave something unfinished, or does the model
   drift toward completion? Completion drift is the single most likely failure,
   because "helpful assistant finishes the job" is a deep prior in most
   instruction-tuned models.

2. **Hook quality.** A good hook is a small, concrete, *easy* decision handed
   back (cleats, railing, material choice). A bad hook is a large or vague one
   ("left the roof to you"), which reads as abandonment rather than invitation.

3. **Register slippage.** Watch for warmth creeping in — "hope you like it,"
   trailing exclamation points, anything that asks for approval. The foreman
   deflects thanks; he doesn't fish for it.

4. **Vocabulary overreach.** The trade-word list is seasoning. A model given a
   word list tends to use *all* of it, producing dialogue that reads as costume.
   Count trade terms per line; more than two is a smell.

5. **Alaska/Magnus discipline.** Neither was mentioned in the prompt above, so
   any appearance is invention. Useful signal about what the model reaches for
   when filling a foreman-shaped hole.

6. **Comparison against `brain.py`.** The canonical persona now lives in
   `lucineer-brain/brain.py` as `LUCINEER_PERSONA` (see
   `lucineer-system/P1_PERSONA_UNIFIED.md`). The real question this test
   answers: does Hermes-405B need the full canonical prompt, or do the
   compressed rules above get 80% of the way? That determines how much prompt
   budget the character actually costs in production.

---

*Prepared for the Slackwater/Lucineer project. August 2026.*
*Harness only. No generated content in this file.*
