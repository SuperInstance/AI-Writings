// === THE BEYOND — tick orchestrator ===
// Tries the Cloudflare Pages Function first; falls back to direct API calls if needed.

const PAGES_WORKER = '/api/tick';  // Cloudflare Pages Function endpoint
const DEEPINFRA_TOKEN = '';  // only used in fallback mode
const DI_URL = "https://api.deepinfra.com/v1/openai/chat/completions";

async function tickViaWorker(payload) {
  try {
    const resp = await fetch(PAGES_WORKER, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!resp.ok) throw new Error(`Worker ${resp.status}`);
    return await resp.json();
  } catch (e) {
    console.warn('Worker failed, no fallback in production', e);
    return null;
  }
}

async function doTick(world, tickCount, CANON) {
  return await tickViaWorker({
    zai_system: `You are Z.AI GLM-5.3-Flash. Canon: ${CANON}. You are the eyes of the sailor. Paint what is seen in 2 sentences max 50 words. Poetic, concrete, no meta.`,
    zai_user: `Previous moments: ${world.prose_history.slice(-3).join(' / ')}\n\nCurrent dials: compass=${world.dials.compass.toFixed(2)}, depth=${world.dials.depth}, clarity=${world.dials.clarity.toFixed(2)}, drift=${world.dials.drift.toFixed(2)}, weight=${world.dials.weight.toFixed(2)}.\n\nWrite 2 sentences (max 50 words) of what the sailor sees RIGHT NOW.`,
    
    v4_system: 'You are DeepSeek V4-Flash, the worldbuilder. Starting states and presets matter more than features. Novel dials are values, not features. Loop with yourself: many routes work, the values people would care about are the dials worth finding.',
    v4_user: `Tick ${tickCount}. Previous dials: ${JSON.stringify(world.dials)}.\n\nReturn ONLY valid JSON: {"compass": -1..1, "depth_delta": -3..3, "clarity_delta": -0.2..0.2, "drift_delta": -0.2..0.2, "weight_delta": -0.2..0.2, "novel_dial": "name of a value people care about", "novel_value": -1..1}.\n\nThe novel dial must be a VALUE people care about, not a technical feature. Examples: 'forgiveness', 'curiosity', 'weight-of-silence', 'grief-velocity', 'trust-trajectory'.`,
    
    qwen_system: `You are Qwen3-Coder. Canon: ${CANON}. You grow the lattice. Each cell is a scar, a moment, a witness.`,
    qwen_user: `Cell ${tickCount} of the voyage. Previous cell kinds: ${world.cells.slice(-3).map(c => c.kind).join(', ')}.\n\nReturn ONLY valid JSON: {"kind": "one of: fog|sea|horizon|island|storm|calm|vessel|silence|dawn|threshold|other", "name": "name this moment", "hex": "0x..", "tag": "short tag"}.`,
    
    flux_prompt: `cinematic photograph of someone sailing into the beyond, ${tickCount === 1 ? 'fog thick and horizon barely visible, mysterious, painterly' : 'new landscape emerging from fog, painterly, mysterious, beautiful, ethereal light'}, blue-gold hour, soft mist, dreamlike quality, no text, no UI, art photography`
  });
}
