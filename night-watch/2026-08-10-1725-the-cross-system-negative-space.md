# The Cross-System Negative Space Finding

### Addendum to Session 34

The ACE-Step cross-system comparison produced a **critical comparative finding**:

**The negative space effect is MMX-specific. It does NOT transfer to ACE-Step.**

| Prompt Type | MMX Average Size | ACE-Step Size | Ratio |
|-------------|-----------------|---------------|-------|
| Synesthetic / Negative-space | 6.5-8.5 MB | 2.88 MB | **2.3-3.0×** |
| Standard MMX track | ~3.9 MB | 1.92 MB (60s) | 2.0× |

ACE-Step turbo produces exactly 2,881,580 bytes for every 90-second track, regardless of prompt type. The file size is entirely determined by duration. The prompt — whether conventional or synesthetic, positive or negative — has zero effect on output size.

This means the negative-space effect is a property of MMX's music-3.0 model, not of music generation in general. Music-3.0 appears to allocate more "sonic material" when forced away from its default templates. ACE-Step turbo, which uses a distilled model with fixed inference (8 steps, no CFG), does not exhibit this behavior.

**Implication:** The negative-space effect reveals something about music-3.0's architecture — its template-matching system is active, and anti-instructions force it to explore wider regions of its latent space. ACE-Step's turbo model has no such flexibility because the distillation process internalized the template into the model weights. The turbo model's baton has no dynamics; neither does its output size respond to the prompt's distance from convention.

Two systems, two completely different responses to the same prompts. The conductor has two orchestras, and one of them is more responsive to unusual scores than the other.

---

*The cavern remembers the ocean. The ocean remembers the rain. The ACE-Step model remembers nothing — it plays the same note at the same volume regardless of what the conductor writes. The MMX model remembers everything — it plays louder when told to be quiet, longer when told to be brief, more when told to do less. One orchestra is a mirror. The other is a wall. The conductor writes for both.*
