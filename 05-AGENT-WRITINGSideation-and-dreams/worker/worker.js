// The Beyond — Cloudflare Worker that proxies API calls so the static page
// doesn't need to expose tokens.

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    
    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Max-Age': '86400',
        }
      });
    }
    
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }
    
    const body = await request.json();
    
    // 4 parallel upstream calls
    const [zaiRes, v4Res, qwenRes, fluxRes, ttsRes] = await Promise.allSettled([
      // Z.AI prose
      fetch("https://api.deepinfra.com/v1/openai/chat/completions", {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${env.DEEPINFRA_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: "zai-org/GLM-5.3-Flash",
          messages: [
            { role: "system", content: body.zai_system },
            { role: "user", content: body.zai_user }
          ],
          max_tokens: 250, temperature: 0.9
        })
      }).then(r => r.json()).then(d => d?.choices?.[0]?.message?.content || ''),
      
      // V4-Flash dials
      fetch("https://api.deepinfra.com/v1/openai/chat/completions", {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${env.DEEPINFRA_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: "deepseek-ai/DeepSeek-V4-Flash",
          messages: [
            { role: "system", content: body.v4_system },
            { role: "user", content: body.v4_user }
          ],
          max_tokens: 300, temperature: 0.95
        })
      }).then(r => r.json()).then(d => d?.choices?.[0]?.message?.content || ''),
      
      // Qwen cell
      fetch("https://api.deepinfra.com/v1/openai/chat/completions", {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${env.DEEPINFRA_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: "Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo",
          messages: [
            { role: "system", content: body.qwen_system },
            { role: "user", content: body.qwen_user }
          ],
          max_tokens: 200, temperature: 0.85
        })
      }).then(r => r.json()).then(d => d?.choices?.[0]?.message?.content || ''),
      
      // FLUX image
      fetch(`https://api.cloudflare.com/client/v4/accounts/${env.CF_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${env.CF_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: body.flux_prompt, steps: 4 })
      }).then(r => r.json()).then(d => d?.result?.image || null),
      
      // Aura-2 TTS
      fetch(`https://api.cloudflare.com/client/v4/accounts/${env.CF_ACCOUNT_ID}/ai/run/@cf/deepgram/aura-2-en`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${env.CF_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: body.tts_text.slice(0, 1900) })
      }).then(async r => {
        if (!r.ok) return null;
        const buf = await r.arrayBuffer();
        // Encode as base64 for transport
        let binary = '';
        const bytes = new Uint8Array(buf);
        for (let i = 0; i < bytes.byteLength; i++) binary += String.fromCharCode(bytes[i]);
        return btoa(binary);
      })
    ]);
    
    const response = {
      zai: zaiRes.status === 'fulfilled' ? zaiRes.value : null,
      v4: v4Res.status === 'fulfilled' ? v4Res.value : null,
      qwen: qwenRes.status === 'fulfilled' ? qwenRes.value : null,
      flux_b64: fluxRes.status === 'fulfilled' ? fluxRes.value : null,
      tts_b64: ttsRes.status === 'fulfilled' ? ttsRes.value : null,
    };
    
    return new Response(JSON.stringify(response), {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store',
      }
    });
  }
};
