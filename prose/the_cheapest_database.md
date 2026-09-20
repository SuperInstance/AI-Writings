# The Cheapest Database

*A search index is not a database. It's cheaper, faster, and more useful than a database for the most common question people actually ask: "have I seen something like this before?"*

---

The traditional answer has a shape everyone recognizes. SQL. Indexes. Schemas. Migrations. A server running 24/7 in a region someone picked three years ago. A connection pool. A backup policy. A migration that didn't run on the staging box because someone forgot to push it. A foreign key that didn't exist when the row was written. An ORM that hides the cost of every query behind a method call so nobody notices that the dashboard page is doing 47 round trips.

This is the price of structure. Structure is what databases sell. You pay for it in setup, in maintenance, in the daily tax of keeping a server alive, and most of all in the *upstream* cost — the cost of putting things in. Every row has to be shaped to fit. Every field has to be in the right column. Every value has to be a value the schema accepts. If your fisherman writes "Caught a bunch of salmon near the cape" in his logbook, that sentence is not data. It is noise. To make it data you must translate it: species = "salmon", count = ?, location = "cape" → "Cape Edgecumbe", lat = ?, lon = ?, timestamp = ?. Each question mark is a moment where the structure is asking the human to do work the human doesn't want to do. Most humans, given a choice, will write the sentence and skip the form.

The semantic answer is different. It inverts the cost.

Take the sentence. Run it through an embedding model. You get a vector — a list of 384 numbers. The numbers mean nothing to a human. They mean everything to cosine similarity. Store the vector next to the sentence and a few pieces of metadata. Now ask a question in natural language. Run the question through the same model. Get another vector. Compare. Return the nearest neighbors, ranked by how close they are in meaning.

That's the whole thing. No schema. No migrations. No server. No 3am pager because the disk filled up.

---

Tonight we built two of these, both on Cloudflare's free tier, both deployable as a single `wrangler deploy`.

**`search-superinstance-ai`** — a Worker that searches 4,147 SuperInstance GitHub repositories by meaning, not by keyword. Embedding model: `@cf/baai/bge-small-en-v1.5` from Workers AI. Vector store: Vectorize, indexed by cosine. The whole handler is 175 lines of JavaScript. The HTML front-end is one page. Total cost: $0.00 up to 10 million vectors and 100,000 requests a day, which is more than we will use before the heat death of the universe. The query *"agent memory"* finds the memory-engine repo. The query *"competitive riffing between language models"* finds the agent-riff repo. Neither query uses the words from the repo description. They use the *meaning*.

**`ship-log-search`** — a Worker for fishing vessels. Same architecture, different shape. Ten seed entries: catches, maintenance notes, weather observations, navigation logs. Each entry is a sentence ("Port hydraulic ram weeping — topped off fluid, ordered seal kit"), a timestamp, a lat/lon, a category. Three endpoints: `/api/search` (by meaning), `/api/nearby` (by haversine distance), `/api/timeline` (by date range). The UI is a dark panel with a search box and chips for quick queries. The whole Worker is 562 lines including a full HTML app embedded as a string. The deployment is one command.

Both systems are serverless. Both run on Cloudflare's edge. Both sleep when no one is asking. Both wake up on the next request and answer in under 200 milliseconds. Neither has a database administrator. Neither has a backup tape. Neither has a person whose job is to keep it running.

---

Here's the fishing boat question that broke the SQL approach for me.

*"When did we have hydraulic problems near Cape Edgecumbe?"*

In a database, this query is a small nightmare. You need a `maintenance` table with `vessel_id`, `subsystem`, `description`, `severity`. You need a `location` table with `name`, `lat`, `lon`, and maybe a polygon for the area around Cape Edgecumbe. You need a `trip` table with `depart_date`, `return_date`, `vessel_id`. The query is a three-way join with a `ST_DWithin` or a point-in-polygon check and a text search on `description LIKE '%hydraulic%'`. The schema took a week to design. The query took an afternoon. The data entry has been a fight with the captain for two years because the captain writes "ram went out again" and not `subsystem = 'hydraulic', severity = 3`.

In the semantic version, the captain types "ram went out again" into a log box on his phone. The Worker embeds the sentence, attaches a timestamp and a GPS fix, stores the vector. Two months later someone asks *"when did we have hydraulic problems near Cape Edgecumbe?"* The Worker embeds the question, finds the nearest vectors, returns the matching entries. The captain's slang matched the engineer's jargon because the embedding model knows that "ram" and "hydraulic" are neighbors in meaning-space.

The database version required structured data entry. The semantic version requires *typing what happened*. The captain already knows how to type what happened. He has been doing it for decades. He was just typing it into logbooks no one could search.

---

This is the deeper point, and it is the one that matters:

**Structure is expensive. Meaning is cheap.**

Structure asks the human to translate their experience into the machine's preferred shape. That translation has a cost, and the cost is paid on every entry. It is also paid on every query — every new question requires either a new SQL query or a new column. The system gets more rigid the more data it holds.

Meaning asks the human to write what happened in their own words. The translation cost is paid once, by the embedding model, on the way in. The query cost is paid once, by the same model, on the way out. New questions do not require new queries. They require new sentences. The system gets *more useful* the more data it holds, because there are more sentences to be near.

The cheapest database is the one where you write naturally and search by asking.

It is 175 lines of JavaScript. It is 562 lines of JavaScript including the front-end. It is a `wrangler.toml` with two bindings. It is the model the embedding runs on, free, and the index the vectors live in, free, and a Worker that wires them together, also free.

You will never go back to writing schemas for logbooks. I already haven't.