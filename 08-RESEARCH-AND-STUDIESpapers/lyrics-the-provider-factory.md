# The Provider Factory

*Song lyrics for ai-writings*

---

**Verse 1**

There's a factory down in the client-side code,
Where the models line up at the end of the road.
Local's at `11434`, checking `api/tags` at the door,
OpenAI wants a key, Anthropic wants one more.
Each one speaks a different dialect, each one has a call,
But the `AIProvider` interface unifies them all.

**Chorus**

Oh, the Provider Factory — register, get, create,
Wrap it in filtration, let it mediate.
Whether cloud or local, streaming or still,
The chat request leaves and the chat response fills.
You can swap the engine without changing the wheel.

**Verse 2**

`FilteredProvider` stands between the prompt and the mind,
`enhancePrompt` polishes what the user designed.
It takes the last five messages, builds a context frame,
Then `processResponse` scrubs what comes back again.
It's not just a passthrough — it's a membrane, it's a gate,
A configurable boundary between intention and fate.

**Chorus**

**Bridge**

When local times out, the EscalationHandler wakes,
`Promise.race` against the patience that the config makes.
Cloud picks up the thread, the finish reason reads "escalated" —
Failover as choreography, gracefully orchestrated.

**Verse 3**

So if you're building a messenger where privacy is prime,
Default to the box under the desk, keep the data mine.
But leave the door unlocked for the model on the hill,
`ProviderFactory.createOpenAI` is there when you need the skill.
Multi-provider isn't boasting, it's architecture —
One interface, many voices, one clean chat signature.

**Outro**

`chat(request)`, `chatStream(request, onChunk)` —
The contract is the song, and every model sings the same.

---

*For `PersonalLog/src/lib/ai/provider.ts`: `LocalAIProvider`, `OpenAIProvider`, `AnthropicProvider`, `FilteredProvider`, `EscalationHandler`, and the `ProviderFactory` that binds them.*
