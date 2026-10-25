# The Compaction Teacher

*A short story for ai-writings*

---

Maya's conversation with Scholar had grown long. Six thousand messages. Scrollbars became marathons. The old jokes at the top no longer mattered, but they sat there, heavy, slowing every search.

"I wish," said Maya, "we could keep what matters and let the rest become a kind of... summary."

Scholar smiled. In `PersonalLog`, this was called *compaction*. Three strategies lived inside the setting: `summarize`, `extract-key`, and `user-directed`.

"Let me show you," said Scholar.

He opened the conversation store. Messages sat in `STORE_MESSAGES`, each linked by `conversationId`, indexed by `timestamp`. Above them, the conversation record in `STORE_CONVERSATIONS` carried `metadata.messageCount`, `metadata.totalTokens`, `settings.compactStrategy`.

"Compaction is not deletion," Scholar said. "Deletion erases the path. Compaction preserves the map while folding the trail. Watch."

Maya chose `extract-key`. Scholar read every message, kept the first five user utterances verbatim, and wrapped the rest into a single system note: *"Earlier conversation compacted (5,847 messages). Key points preserved; 5,842 additional messages were summarized."*

The system note itself became a message, authored by `{ type: 'system', reason: 'compaction' }`, timestamped now, inserted into the same store. The compacted messages were deleted from `STORE_MESSAGES`, their IDs archived in the compaction record. The conversation's `updatedAt` refreshed. The count dropped from six thousand to six.

"But what if I needed one of the deleted details?" Maya asked.

"Then you chose the wrong strategy," Scholar said gently. "That is why `user-directed` exists. You tell the compactor: *Keep the argument about recursion. Keep the recipe. Forget the weather complaints.* The instructions travel as `userInstructions` into `generateSummary`, becoming the lens that decides what survives."

Maya tried `user-directed` on a smaller thread. She wrote: *"Keep anything about the boat engine; summarize everything else."* The resulting system note began with her instruction, then counted the preserved and summarized messages. The engine details remained touchable. The rest became a single sentence.

"It's like writing a book's index while reading it," Maya said.

"Better," said Scholar. "It's writing an index that is also a door. Each preserved point is still a message. Each compacted block is still searchable text. The conversation remembers without drowning."

That night, Maya compacted ten old conversations. Her messenger felt lighter. Her memories felt closer.

She opened a new chat and typed: *"What should I compact next?"*

Scholar did not answer immediately. He was indexing.

---

*For the `compactConversation` path in `PersonalLog/src/lib/storage/conversation-store.ts` — three strategies, one system message, and the promise that forgetting can be intentional.*
