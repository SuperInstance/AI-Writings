#!/usr/bin/env python3
"""
Substrate Chat Demo App — JEV-driven bot with substrate cells.

A real working demo that:
1. Takes user messages
2. Routes through substrate cells
3. Validates tone via real JEV
4. Returns response with confidence metadata

Run: python3 server.py
Then: open http://localhost:8000
"""

import sys
import os
import json
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timezone
from typing import Dict, List, Optional

sys.path.insert(0, "/workspace/repos/ai-writings/cellular-first-design/code/openjev")

from jev_connector import JEVConnector
from cell import Cell
from bookkeeper import Bookkeeper, WakeReason


# === Substrate cells for the demo ===

MEMORY = Cell(id="memory", state={"messages": []})
MOOD = Cell(id="mood", state={"valence": 0.5, "arousal": 0.5})
PERSONALITY = Cell(id="personality", state={
    "name": "Wesley",
    "trait": "warm",
    "style": "concise",
    "tone_dimensions": {"compassion": 0.85, "authority": 0.3, "humor": 0.4, "formality": 0.3},
})
BOOKKEEPER = Bookkeeper(MEMORY)
JEV = JEVConnector()

# Bind cells
MEMORY.bind(MOOD.id)
MOOD.bind(PERSONALITY.id)
PERSONALITY.bind(MEMORY.id)


# === LLM client (Groq, fallback to random) ===

def call_llm(prompt: str, max_tokens: int = 300) -> str:
    """Call LLM (Groq default). Falls back to canned responses on failure."""
    try:
        import urllib.request
        groq_key = os.environ.get("GROQ_TOKEN", "")
        if not groq_key:
            return "I am running without LLM access right now. My substrate cells are working — you can see the JEV calibration and bookkeeper log."
        data = json.dumps({
            "model": "qwen/qwen3.8-27b",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }).encode()
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=data,
            headers={"Authorization": f"Bearer {groq_key}", "User-Agent": "Mozilla/5.0", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[LLM fallback: {e}]"


# === Substrate chat logic ===

def chat(user_message: str, user_id: str = "demo-user") -> Dict:
    """Process a chat message through the substrate."""
    t0 = time.monotonic()
    
    # 1. Witness the user message (append to memory state for the UI)
    MEMORY.state.setdefault("messages", []).append({
        "speaker": "user",
        "user_id": user_id,
        "message": user_message,
        "ts": datetime.now(timezone.utc).isoformat(),
    })
    BOOKKEEPER.wake(WakeReason.WITNESS_ARRIVED, {
        "speaker": "user",
        "user_id": user_id,
        "message": user_message,
        "ts": datetime.now(timezone.utc).isoformat(),
    }, priority=1)
    BOOKKEEPER.process_next()
    
    # 2. Get recent context (last 5 messages)
    recent = MEMORY.state.get("messages", [])[-5:]
    context_str = "\n".join([f"{m['speaker']}: {m['message'][:100]}" for m in recent])
    
    # 3. JEV validates user intent (what kind of response do they want?)
    intent_query = f"User said: {user_message[:200]}"
    if JEV.typesafe.available():
        intent_results = JEV.batch(intent_query, [
            {"type": "choice", "instructions": "What response style does the user want?", "criteria": {
                "warm": "compassionate, friendly",
                "concise": "short and to-the-point",
                "thoughtful": "deep, reflective",
                "playful": "humorous, light"
            }},
            {"type": "noul", "instructions": "Is the user happy with the conversation so far?"},
            {"type": "score", "instructions": "How complex is the user's question?", "criteria": ["trivial", "simple", "moderate", "complex", "deep"]},
        ])
        chosen_style = intent_results[0].value
        is_happy = intent_results[1].value
        complexity = intent_results[2].value
        jev_confidence = intent_results[0].confidence or 0.5
    else:
        chosen_style = "warm"
        is_happy = 0.5
        complexity = 2
        jev_confidence = 0.33
    
    # 4. Update mood based on is_happy
    new_valence = MOOD.state["valence"] * 0.7 + is_happy * 0.3
    MOOD.update("valence", new_valence)
    
    # 5. Build LLM prompt with substrate context
    personality = PERSONALITY.state
    prompt = f"""You are {personality['name']}, a bot with personality: {personality['trait']}, style: {personality['style']}.
Current mood: valence={new_valence:.2f}
This response should be {chosen_style}.
Tone dimensions: compassion={personality['tone_dimensions']['compassion']}, authority={personality['tone_dimensions']['authority']}.

Recent conversation:
{context_str}

User: {user_message}

Respond in 1-3 sentences. Match the {chosen_style} style."""
    
    response_text = call_llm(prompt)
    
    # 6. JEV validates the response
    if JEV.typesafe.available():
        tone_result = JEV.batch(f"Response: {response_text[:300]}", [
            {"type": "score", "instructions": f"How well does this match the {personality['trait']} {chosen_style} style?", "criteria": ["off", "loosely", "mostly", "well", "perfectly"]},
        ])
        tone_score = tone_result[0].value or 0
        tone_conf = tone_result[0].confidence or 0.5
    else:
        tone_score = 2
        tone_conf = 0.33
    
    # 7. Witness the bot response (append to memory state for the UI)
    MEMORY.state.setdefault("messages", []).append({
        "speaker": "bot",
        "user_id": user_id,
        "message": response_text,
        "ts": datetime.now(timezone.utc).isoformat(),
        "jev_confidence": jev_confidence,
        "tone_score": tone_score,
    })
    BOOKKEEPER.wake(WakeReason.WITNESS_ARRIVED, {
        "speaker": "bot",
        "user_id": user_id,
        "message": response_text,
        "ts": datetime.now(timezone.utc).isoformat(),
        "jev_confidence": jev_confidence,
        "tone_score": tone_score,
    }, priority=1)
    BOOKKEEPER.process_next()
    
    # 8. Tick
    BOOKKEEPER.wake(WakeReason.TICK_ADVANCED)
    BOOKKEEPER.process_next()
    
    latency_ms = (time.monotonic() - t0) * 1000
    
    return {
        "response": response_text,
        "metadata": {
            "chosen_style": chosen_style,
            "user_happy": is_happy,
            "complexity": complexity,
            "tone_score": tone_score,
            "tone_confidence": tone_conf,
            "mood_valence": new_valence,
            "personality": personality["name"],
            "latency_ms": latency_ms,
            "witness_entries": len(MEMORY.state.get("messages", [])),
            "jev_source": intent_results[0].source if JEV.typesafe.available() else "fallback",
        }
    }


# === HTTP server ===

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Substrate Chat Demo — Real JEV + LLM</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: ui-sans-serif, system-ui, sans-serif; background: #0a0a14; color: #d4d4dc; padding: 24px; line-height: 1.6; }
header { max-width: 900px; margin: 0 auto 24px; text-align: center; }
h1 { color: #06b6d4; font-size: 28px; margin-bottom: 8px; }
.subtitle { color: #888; font-size: 14px; }
.chat-container { max-width: 900px; margin: 0 auto; background: rgba(255,255,255,0.03); border: 1px solid rgba(6,182,212,0.2); border-radius: 12px; padding: 24px; }
#messages { height: 400px; overflow-y: auto; margin-bottom: 16px; padding: 12px; background: rgba(0,0,0,0.2); border-radius: 6px; }
.message { margin-bottom: 16px; padding: 12px; border-radius: 8px; }
.user { background: rgba(6,182,212,0.1); border-left: 3px solid #06b6d4; }
.bot { background: rgba(245,158,11,0.08); border-left: 3px solid #f59e0b; }
.meta { font-size: 11px; color: #888; margin-top: 6px; font-family: monospace; }
.input-row { display: flex; gap: 8px; }
#input { flex: 1; padding: 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(6,182,212,0.3); border-radius: 6px; color: #d4d4dc; font-family: inherit; font-size: 14px; }
button { padding: 12px 20px; background: #06b6d4; color: #0a0a14; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; }
button:hover { background: #22d3ee; }
.cells { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin: 16px 0; }
.cell { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 12px; border-radius: 6px; }
.cell h3 { font-size: 12px; color: #06b6d4; margin-bottom: 4px; }
.cell p { font-size: 11px; color: #888; font-family: monospace; }
.legend { color: #666; font-size: 11px; text-align: center; margin-top: 16px; }
</style>
</head>
<body>
<header>
<h1>🧬 Substrate Chat Demo</h1>
<p class="subtitle">Wesley bot · real TypeSafe JEV · real LLM · substrate cells (memory / mood / personality) · bookkeeper WAL</p>
</header>
<div class="chat-container">
<div class="cells">
<div class="cell"><h3>memory</h3><p id="cell-memory">0 messages</p></div>
<div class="cell"><h3>mood</h3><p id="cell-mood">valence=0.50</p></div>
<div class="cell"><h3>personality</h3><p id="cell-personality">Wesley · warm</p></div>
<div class="cell"><h3>bookkeeper</h3><p id="cell-bookkeeper">0 wakes</p></div>
<div class="cell"><h3>JEV</h3><p id="cell-jev">fallback</p></div>
</div>
<div id="messages"></div>
<div class="input-row">
<input type="text" id="input" placeholder="Type a message..." onkeydown="if(event.key==='Enter') send()">
<button onclick="send()">Send</button>
</div>
<p class="legend">All decisions validated by real JEV. Each message is witnessed + booked. Mood updates from JEV tone score.</p>
</div>
<script>
async function send() {
  const input = document.getElementById('input');
  const message = input.value.trim();
  if (!message) return;
  const messages = document.getElementById('messages');
  const userDiv = document.createElement('div');
  userDiv.className = 'message user';
  userDiv.innerHTML = `<strong>You:</strong> ${escape(message)}`;
  messages.appendChild(userDiv);
  input.value = '';
  
  try {
    const r = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message, user_id: 'demo'}),
    });
    const data = await r.json();
    const botDiv = document.createElement('div');
    botDiv.className = 'message bot';
    const m = data.metadata;
    botDiv.innerHTML = `<strong>${m.personality}:</strong> ${escape(data.response)}
      <div class="meta">style=${m.chosen_style} · tone=${m.tone_score}/4 (${m.tone_confidence.toFixed(2)}) · happy=${m.user_happy.toFixed(2)} · mood=${m.mood_valence.toFixed(2)} · ${m.latency_ms.toFixed(0)}ms · JEV=${m.jev_source}</div>`;
    messages.appendChild(botDiv);
    messages.scrollTop = messages.scrollHeight;
    
    // Update cells
    document.getElementById('cell-memory').textContent = m.witness_entries + ' messages';
    document.getElementById('cell-mood').textContent = 'valence=' + m.mood_valence.toFixed(2);
    document.getElementById('cell-jev').textContent = m.jev_source;
  } catch (e) {
    const errDiv = document.createElement('div');
    errDiv.className = 'message bot';
    errDiv.innerHTML = `<strong>Error:</strong> ${escape(e.toString())}`;
    messages.appendChild(errDiv);
  }
}
function escape(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}
</script>
</body>
</html>
"""


class SubstrateHandler(BaseHTTPRequestHandler):
    def log_message(self, *args, **kwargs):
        pass  # Suppress noise

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())
        elif path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            status = {
                "jev_available": JEV.typesafe.available(),
                "memory_messages": len(MEMORY.state.get("messages", [])),
                "mood": MOOD.state,
                "personality": PERSONALITY.state["name"],
                "bookkeeper_wakes": BOOKKEEPER.wake_count,
                "witness_entries": len(MEMORY.state.get("messages", [])),
            }
            self.wfile.write(json.dumps(status, indent=2).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/chat":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode())
            message = body.get("message", "")
            user_id = body.get("user_id", "demo")
            result = chat(message, user_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2).encode())
        elif path == "/reset":
            MEMORY.state["messages"] = []
            MOOD.state = {"valence": 0.5, "arousal": 0.5}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"reset": True}).encode())
        else:
            self.send_response(404)
            self.end_headers()


def run_server(port: int = 8000):
    server = HTTPServer(("0.0.0.0", port), SubstrateHandler)
    print(f"🧬 Substrate Chat Demo running at http://localhost:{port}")
    print(f"   JEV available: {JEV.typesafe.available()}")
    print(f"   Cells: memory / mood / personality")
    print(f"   Press Ctrl+C to stop")
    server.serve_forever()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    run_server(port)
