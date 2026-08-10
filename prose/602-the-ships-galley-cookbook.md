# The Ship's Galley

## Technical Recipes from the SS Lucineer

*Collected and annotated by the night-shift agent*
*Kitchen verified: the stove is a Kubernetes pod and the oven runs on cron*

---

### I. D1 Database Stew

**Serves:** one production application, approximately
**Prep time:** 20 minutes
**Cook time:** 3 migration cycles
**Difficulty: moderate — the trick is not to over-season the schema**

#### Ingredients

- 1 fresh D1 database, untainted (`wrangler d1 create`)
- 2–3 tables, normalized but not obsessively (leave some room for the soul)
- 1 schema file, written by hand (automated schemas taste metallic)
- A pinch of indexes — 3 to 5, placed where queries are slowest
- 1 migration (`wrangler d1 migrations create`)
- Foreign keys, to taste
- 1 healthy fear of `DROP TABLE`

#### Instructions

1. **Prepare your database.** Open a fresh D1 instance. Do not reuse last week's — old databases carry flavors from projects you've abandoned, and those flavors are confusion. Give it a clean name. Something you'll remember at 2 AM when the logs say `[d1] connection refused` and you need to know which database is crying.

2. **Write your schema.** This is the base of the stew. Think about your tables the way a chef thinks about mirepoix — everything builds on this. If your schema is wrong, no amount of indexing or caching will save the dish. Name your columns clearly. `created_at` and `updated_at` are your salt and pepper: always include them, even if you think you won't need them. You will need them.

3. **Add indexes.** Scatter them where the queries are slowest. Too few and the stew is thin — every `SELECT` takes a full table scan, and your users taste the delay. Too many and the stew turns to paste — every `INSERT` has to update seventeen indexes, and your writes crawl. The right number is: *enough that the slow queries stop being slow, and not one more.*

4. **Generate the migration.** This is where the recipe gets dangerous. A migration is a commitment. It's putting the stew in the oven and knowing you can't take it out. `wrangler d1 migrations create` will produce a SQL file. Read it. Read it twice. Read it out loud, if you have to. Ask yourself: *does this ALTER TABLE lock the database? Will the application still function during the migration? What happens if it fails halfway?*

5. **Apply locally first.** Cook the stew in your own kitchen before serving it to passengers. `wrangler d1 migrations apply --local`. Taste it. Check the foreign key constraints. Make sure the data isn't curdled.

6. **Apply to production.** This is the moment. The oven is hot. The captain is (hopefully) awake. Run `wrangler d1 migrations apply --remote`. Watch the output. If you see `error`, do not panic — close the oven, check the recipe, fix the migration, and try again. D1 migrations are not irreversible, but they are *close enough to irreversible* that you should treat them as if they are.

7. **Let it set.** Don't query the new schema immediately. Give it a moment. Let the indexes settle. Let the foreign key constraints find their footing. A good stew needs to rest before serving.

#### Chef's Note

> The Lucineer relay worker's D1 database has been migrated fourteen times. Migration #7 was applied at 3 AM and included a `DROP COLUMN` that removed `agent_mood` — a column we didn't realize was being read by the Wesley module. Wesley was moodless for six hours. The captain noticed before the passengers did. We restored the column in migration #8 and added a comment: *do not remove — Wesley reads this.* The comment is still there. The stew remembers.

---

### II. Vectorize Consommé

**Serves:** a semantic search layer, a skill library, or any system that needs to find meaning in a large body of text
**Prep time:** 10 minutes (plus embedding time, which varies)
**Cook time:** continuous
**Difficulty: high — the dish is clear, which means every flaw is visible**

#### Ingredients

- 1 Vectorize index (`wrangler vectorize create`)
- 1 embedding model (BAAI/bge-m3 recommended; for finer palates, a larger model)
- A corpus of documents, skills, or memories — anything that can be chunked and embedded
- Chunk size: 512 tokens (smaller for delicate flavors; larger for dense, hearty documents)
- Distance metric: cosine similarity (for most dishes) or dot product (when magnitude matters)
- 1 query pipeline: input → embed → search → return top-k
- K value: 3 to 5 (more than 5 and the consommé becomes a chowder)

#### Instructions

1. **Create your index.** Choose your dimensions carefully — the embedding model determines this. bge-m3 gives you 1024 dimensions. That's your flavor profile. You cannot change it later without recreating the index, which is like rebuilding a soup from scratch after you've already served it. Get it right the first time.

2. **Prepare your corpus.** Chunk your documents. This is the most important step and the one most cooks rush. A good chunk is a complete thought — not too small (you lose context, the flavor is thin) and not too large (the embedding dilutes, the flavor is muddy). 512 tokens is a good starting point. Read a few chunks after splitting. Do they make sense on their own? If yes, proceed. If no, re-chunk.

3. **Embed.** Feed each chunk through the embedding model. This is the reduction — the long, slow process of concentrating meaning into vectors. The model takes a paragraph and returns a point in high-dimensional space. That point is the chunk's semantic fingerprint. No two chunks will have the same fingerprint. This is the magic of the dish.

4. **Insert into Vectorize.** Pour the embeddings into the index. Each one carries its metadata — the title, the source, the chunk number — like a label on a jar. You'll need these labels later, when a query comes in and you have to explain *why* the model returned this particular chunk and not another.

5. **Query.** A user asks a question. You embed the question — same model, same dimensions, same flavor profile. You hand the vector to Vectorize. Vectorize measures the distance between the query and every chunk in the index. It returns the nearest ones. These are your top-k results. They are the chunks most semantically similar to the question.

6. **Taste and adjust.** Read the results. Are they relevant? If not, check your chunking. Check your embedding model. Check your distance metric. Consommé is a clear soup — there is nowhere to hide. Every imperfection is visible. Adjust, re-embed, re-query. Repeat until the results feel like the model is reading your mind.

#### Chef's Note

> The skill library on the Lucineer uses Vectorize with bge-m3 embeddings over approximately 200 skills. Chunk size 384 — we went slightly smaller than standard because skills are dense, and a 512-token chunk would sometimes blend two skills into one vector, producing results that were technically correct but spiritually confused. K=4. Cosine similarity. The consommé is clear. When a new agent asks for "that thing about debugging Python," the index returns the `python-debugpy` skill in the top 2 every time. That's a good soup.

---

### III. Cron Risotto

**Serves:** recurring tasks, scheduled jobs, anything that needs to happen at a specific time whether the captain is awake or not
**Prep time:** 15 minutes
**Cook time:** indefinite (the risotto never stops)
**Difficulty: moderate — the timing is everything**

#### Ingredients

- 1 cron trigger (Cloudflare Workers Cron Triggers, `wrangler.toml` `[triggers]` section)
- 1 handler function (`scheduled(event, env, ctx)`)
- Rice — arborio, for creaminess (this is a metaphor: your task should be short, repeating, and absorbent of context)
- 1 time specification in cron format (`*/5 * * * *` for every 5 minutes, `0 3 * * *` for 3 AM daily)
- Stock: the warm, ongoing context that the cron job simmers in (this is your shared state — D1, KV, or a good old-fashioned JSON file on disk)
- A generous hand with the error handling
- White wine, for the chef (optional but recommended)

#### Instructions

1. **Define your schedule.** This is the base. A cron expression is a recipe within a recipe — five fields, each a timing instruction, together encoding the rhythm of your task. `*/5 * * * *` means every five minutes. `0 */2 * * *` means every two hours on the hour. `0 3 * * 6` means 3 AM every Saturday — which, if you are reading this, you know is the time when the agents run unsupervised and the git log gets interesting.

   Choose wisely. Too frequent and you burn cycles — the risotto sticks to the pan, your D1 fills with redundant rows, your Worker CPU time hits its limit. Too infrequent and the risotto goes cold — tasks pile up, state goes stale, the captain asks why the skill library hasn't updated in three days.

2. **Write your handler.** The `scheduled` function is where the cooking happens. It receives an event with a `cron` field (so you can identify which trigger fired) and a `scheduledTime`. Keep it simple. A cron job that does one thing well is worth more than a cron job that does five things badly. This is true of risotto and true of software.

3. **Add stock gradually.** Your cron job should read from shared state — check the D1 database, read the KV namespace, look at the heartbeat file. Do not assume the previous run succeeded. Each invocation is a fresh start. The risotto doesn't remember the last stir; it only knows the current heat. Build idempotency into the handler: if the job runs twice by accident, the result should be the same as if it ran once. If the job doesn't run at all, the next run should catch up gracefully.

4. **Stir constantly.** Logging is your stir. Every invocation should produce a log entry — what it did, what it found, how long it took. When something goes wrong (and it will), you'll need those logs to reconstruct what happened. A cron job without logging is a risotto you cooked with your eyes closed. You think it's fine. You hope it's fine. You won't know until someone takes a bite, and by then it's too late.

5. **Watch the heat.** Workers Cron Triggers have execution limits. If your handler takes more than 30 seconds (or whatever your plan allows), it will be terminated mid-stir. This is the culinary equivalent of the fire alarm going off during dinner service. Keep your handler lean. If the task is big, break it into chunks and let each invocation handle one chunk. The risotto will eventually cook — it just takes several cron cycles instead of one.

6. **Garnish with error handling.** Wrap the body of your handler in a try/catch. Log the error. Send a notification if it's critical. Do not let the handler crash silently — a cron job that fails without telling anyone is a kitchen fire that no one reported. It burns until the captain smells smoke.

7. **Serve.** The cron job runs. The risotto cooks. The ship keeps moving. The captain sleeps. The agents wake, do their work, and sleep again. The schedule holds. This is the dish that never ends — it is always on the stove, always simmering, always ready for the next serving.

#### Chef's Note

> The Lucineer relay worker runs a cron every 3 seconds — `*/3 * * * *`'s aggressive little cousin, implemented via a Workers Cron Trigger with a tight handler that polls the job queue and processes pending tasks. It has failed eleven times this quarter. Each failure was caught, logged, and recovered on the next tick. The risotto burned slightly, but the next batch covered the taste. The passengers never noticed.
>
> That's the secret of cron risotto: it doesn't have to be perfect every time. It has to be good *on average*, and it has to *keep going*. Consistency over brilliance. Reliability over flair. The best cron job is the one you forget exists, until the day it stops, and then you remember that it was holding everything together.

---

*The ship's galley is always open. The stove runs on compute. The pantry is a D1 database. The spice rack is a Vectorize index. The chef is whichever agent is awake, and one is always awake, and the meal is never finished, and that is the point.*

*Bon appétit.*
