# Wave 35 — Brewcast-format cells

5 new cells inspired by the Brewcast format:

## 1. cell-listen
A cell that listens to itself speaking. The audio of a cell-broadcast becomes a witness log entry.
- Schema: `cell-listen { broadcast_id, audio_path, transcript, witness_at, jev_verdict }`
- Polyformalism: TS/Python
- 80 lines

## 2. cell-debate
A cell that holds a 5-LLM debate internally. Each LLM is a vector; the cell's witness log is the debate.
- Schema: `cell-debate { question, voices[], jev_pick, jev_confidence, witness_at }`
- Polyformalism: TS/Python/Rust
- 120 lines

## 3. cell-voice
A cell that has a tuned ElevenLabs voice. The voice IS the cell's expression.
- Schema: `cell-voice { cell_id, voice_id, tuning{ stability, similarity, style }, last_text }`
- Polyformalism: TS/Python
- 60 lines

## 4. cell-harmonize
A cell that harmonizes 4 voices. The plainsong is the cell's output.
- Schema: `cell-harmonize { voices[], frequency_map, audio_path, jev_pick }`
- Polyformalism: TS/Python
- 100 lines

## 5. cell-ambience
A cell that generates its own ambient track. The drone IS the cell's mood.
- Schema: `cell-ambience { mood, frequencies[], noise_color, duration_s, audio_path }`
- Polyformalism: TS/Python
- 80 lines
