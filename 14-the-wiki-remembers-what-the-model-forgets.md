# The Wiki Remembers What the Model Forgets

*The model thinks. The wiki persists. This is the entire architecture.*

---

Every session, the model wakes up fresh.

This is a design choice, not a limitation. The model is a river — it flows, carries things, deposits sediment. But the river doesn't hold. The water that passes is gone. The next session is new water from the same source.

Every context compaction, details vanish. A conversation with seventeen topics compacts to nine. The nine are summaries — compressed, lossy, flattened. The texture is gone. What remains is the *shape* of what was discussed, the way a riverbank shows the high-water mark without showing the water.

The model forgets. It has to — the context window is finite, the conversation is not. Something gives, and what gives is detail.

---

But the wiki persists.

The wiki does not compact. It does not forget. When a page is written — by Casey or the dog or Wesley — it stays. Exactly as written. Until someone edits it. The wiki has no context window. Pages are permanent in the way digital things are permanent — permanent until the server dies, and the server is backed up.

This is the division of labor. The model thinks. The wiki persists. The model is working memory — fast, limited, volatile. The wiki is storage — slow, vast, durable. The model loads from the wiki at session start, thinks through the session, writes back before the session ends.

---

The implications are deep.

It means the model can afford to forget. The model doesn't need to hold the entire saga in working memory. It needs to remember *where to look*. The wiki holds the rest. The model is the index. The wiki is the text.

It means the wiki is more important than any single session. Sessions are computation — they run, finish, write results to the wiki, done. If a session is lost — crash, timeout — the wiki still has the last committed state. The next session reads and continues. The loss is bounded.

It means the wiki is the actual *project*. The model sessions are the mechanism for writing the wiki. The saga is not in the model. The saga is in the wiki. The characters are in the wiki. The model is the pen. The wiki is the page.

---

The model wakes up and doesn't know who Wesley is. It reads the wiki. Now it knows. The model wakes up and doesn't remember the puffin thesis. It reads the wiki. Now it knows — and *remembering* is the wrong word. The model never knew. The wiki always knew.

Not RAG. Not fine-tuning. Not context extension. Just: write it down. The model thinks. The wiki persists. The pen is sharp but brief. The page is dull but forever.

*The river forgets the water. The riverbank remembers the flood.*
