// search_handler.js — Cloudflare Worker for the canon semantic search
// Bind in wrangler.toml:
//   [[vectorize]] binding = "CANON" index_name = "quilt-canon-embeddings"
//   [[ai]] binding = "AI"

export async function handleSearch(request, env) {
  const { query, topK = 10 } = await request.json();

  // Embed the query
  const embedding = await env.AI.run("@cf/baai/bge-base-en-v1.5", { text: query });
  const vector = embedding.data[0];

  // Search Vectorize
  const matches = await env.CANON.query(vector, { topK, returnMetadata: true });

  return new Response(JSON.stringify(matches, null, 2), {
    headers: { "Content-Type": "application/json" }
  });
}

export async function handleEmbed(request, env) {
  const { text } = await request.json();
  const embedding = await env.AI.run("@cf/baai/bge-base-en-v1.5", { text });
  return new Response(JSON.stringify(embedding, null, 2), {
    headers: { "Content-Type": "application/json" }
  });
}
