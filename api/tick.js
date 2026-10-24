// The Beyond — Pages Function that proxies API calls

export async function onRequestPost(context) {
  const body = await context.request.json();
  const env = context.env;
  
  const ACCT_ID = "049ff5e84ecf636b53b162cbb580aae6";
  
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
    fetch(`https://api.cloudflare.com/client/v4/accounts/${ACCT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${env.CF_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: body.flux_prompt, steps: 4 })
    }).then(r => r.json()).then(d => d?.result?.image || null),
    
    // Aura-2 TTS — do this after prose arrives
    Promise.resolve(null)
  ]);
  
  // If we got prose, do TTS in second phase
  let ttsB64 = null;
  const zaiProse = zaiRes.status === 'fulfilled' ? zaiRes.value : '';
  if (zaiProse) {
    try {
      const ttsResp = await fetch(`https://api.cloudflare.com/client/v4/accounts/${ACCT_ID}/ai/run/@cf/deepgram/aura-2-en`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${env.CF_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: zaiProse.slice(0, 1900) })
      });
      if (ttsResp.ok) {
        const buf = await ttsResp.arrayBuffer();
        let binary = '';
        const bytes = new Uint8Array(buf);
        for (let i = 0; i < bytes.byteLength; i++) binary += String.fromCharCode(bytes[i]);
        ttsB64 = btoa(binary);
      }
    } catch {}
  }
  
  const response = {
    zai: zaiProse,
    v4: v4Res.status === 'fulfilled' ? v4Res.value : null,
    qwen: qwenRes.status === 'fulfilled' ? qwenRes.value : null,
    flux_b64: fluxRes.status === 'fulfilled' ? fluxRes.value : null,
    tts_b64: ttsB64
  };
  
  return new Response(JSON.stringify(response), {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/json',
      'Cache-Control': 'no-store',
    }
  });
}

export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
    }
  });
}
