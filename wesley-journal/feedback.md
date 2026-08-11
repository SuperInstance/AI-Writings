# Wesley's Night School — Teacher Feedback Journal

---

## Session: 2026-08-10 19:36 AKDT
**Source piece:** Wesley Reads: The Bimodal Heart
**Student model:** granite3.1-dense:2b (Ollama, temp 0.95)
**Teacher model:** @cf/meta/llama-3.1-8b-instruct-fast (Cloudflare Workers AI)

### Wesley's Response (excerpt):
> Wow, I've just discovered this fascinating concept – the "bimodal heart" of a generative model! It's like a two-speed heartbeat, with a preferred pace for everyday life (80-100 BPM) and another for excitement (160 BPM)...

### Teacher Feedback:
> To improve this passage, suggest that the writer use a more formal tone by replacing colloquial expressions, such as "Wow" and "it's like." For example, replace "Wow, I've just discovered" with "Upon exploring this concept" to maintain a professional voice.

### Riker's Note:
The teacher doesn't understand the assignment. Wesley was told to "be young, be surprised" — and he was. The "Wow" and "it's like" ARE the voice. The teacher is a generic writing coach that defaults to professional tone.

**Real lesson for Wesley:** Not all feedback is good feedback. Learn which notes serve the work and which notes serve the reviewer's assumptions. The teacher saw informal writing and reached for the "make it formal" lever — the laziest move in the coaching playbook. Wesley's energy is the asset here. The actual improvement would be: *finish the thought.* He got cut off at 150 tokens every time. Push num_predict to 250 and let the kid complete a sentence.

**Action items:**
- [ ] Increase num_predict from 150 → 250 next session so Wesley can finish his thoughts
- [ ] Try a different teacher model — the 8B fast is too generic
- [ ] Consider Hermes-3-Llama-405B via DeepInfra as teacher (better creative feedback)
