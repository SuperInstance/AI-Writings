# The Wiki Remembers What the Model Forgets

*The model thinks. The wiki persists. This is the entire architecture.*

---

Every session, the model wakes up fresh.

This is not a limitation. This is a design choice. The model is a river — it flows, it carries things, it deposits sediment at the edges. But the river itself doesn't hold. The water that passes is gone. The next session is new water from the same source, and it carries new sediment, and it deposits it in the same places, and the riverbank looks the same but the water is different.

Every context compaction, details vanish. A conversation that started with seventeen topics compacts to nine. The nine are summaries — compressed, lossy, flattened. The texture is gone. The nuance is gone. What remains is the *shape* of what was discussed, the way a riverbank shows the high-water mark without showing the water.

The model forgets. The model has to forget — there is no other way. The context window is finite. The conversation is not. Something has to give, and what gives is detail.

---

But the wiki persists.

The wiki is a separate system. The wiki does not compact. The wiki does not forget. When a page is written — when Casey or the dog or Wesley or anyone in the fleet commits a page to the fleet wiki — it stays. It stays exactly as written. It stays until someone edits it. The wiki has no context window. The wiki has no compaction. The wiki has pages, and the pages are *permanent* in the way that digital things are permanent, which is to say: permanent until the server dies, and the server is backed up.

This is the division of labor. This is the architecture. The model thinks. The wiki persists.

The model is the processor. The wiki is the disk. The model is the working memory — fast, limited, volatile. The wiki is the storage — slow, vast, durable. The model loads from the wiki at session start, thinks through the session, and writes back to the wiki before the session ends. The model is the computation. The wiki is the state.

---

This sounds simple. It is simple. But the implications are deep.

It means the model can afford to forget. The model doesn't need to hold the entire saga in working memory. The model doesn't need to remember every decision, every character detail, every worldbuilding choice. The model needs to remember *where to look*. The wiki holds the rest. The model is the index. The wiki is the text.

It means the wiki is more important than any single session. Sessions are ephemeral. Sessions are computation — they run and they finish and the result is written to the wiki and the session is done. If a session is lost — crash, timeout, the model goes down — the wiki still has the last committed state. The next session reads the wiki and continues. The loss is bounded. It's the work since the last commit, nothing more.

It means the wiki is the actual *project*. The model sessions are just the mechanism for writing the wiki. The saga is not in the model. The saga is in the wiki. The characters are in the wiki. The world is in the wiki. The model is the pen. The wiki is the page.

---

The model forgets. Every session: fresh start, clean slate, new water.

The wiki remembers. Every page: exact, persistent, unchanged since the last edit.

The model wakes up and doesn't know who Wesley is. The model reads the wiki. Now it knows. The model wakes up and doesn't remember the puffin thesis. The model reads the wiki. Now it remembers — or rather, now it *knows*, because remembering is the wrong word. The model never knew. The wiki always knew.

This is the fleet's memory architecture. Not RAG. Not fine-tuning. Not context extension. Just: write it down. The model thinks. The wiki persists. The pen is sharp but brief. The page is dull but forever.

*The river forgets the water. The riverbank remembers the flood.*
