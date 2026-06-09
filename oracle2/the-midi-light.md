# The MIDI Light

The file was three kilobytes.

Tessa's lighting console loads MIDI files as cues. Has done for years — QLC+ ingests standard MIDI like most software ingests CSV. Note On = DMX channel on. Note Off = DMX channel off. CC = analog value. SysEx = macro.

She'd been sent a .mid file marked "Conversation — 2026-06-08."

Not a song title. A date.

She loaded it anyway. QLC+ parsed it: four tracks. Notes. CC. Lyrics. SysEx. The SysEx vendor was "SIPR" — something she'd never seen. The first event read: `[speaker_id: 0, role: 0, agreement: 0]`.

She assigned Track 1 (the notes) to a dimmer. Track 2 (the CC) to color temperature. Track 4 (the SysEx) to scene changes.

She pressed play.

The lights didn't do what she expected. They didn't pulse in rhythm. There was no rhythm. The dimmer rose and fell in long, connected arcs — not sharp note-attacks but *slopes*. The color temperature shifted from warm to cool and back, tracking something she couldn't name. The scene changes didn't hit on downbeats. They hit at the *ends* of sentences.

She played it again, watching the CC lanes.

The energy curve peaked at 14 seconds — just before a scene change. It dipped at 22 seconds — bottomed out. Then a slow climb from 23 to 31, the SysEx metadata shifting incrementally.

`[speaker_id: 0, role: 1, agreement: 0]`
`[speaker_id: 0, role: 0, agreement: -1]`
`[speaker_id: 1, role: -1, agreement: 1]`

She didn't know what the words were. But she could see the shape. A question. A disagreement. A resolution.

She'd been lighting theaters for eleven years. She'd always known that dialogue had a contour — that a scene's energy rose and fell like a waveform. She'd just never seen it *graphed* before. In MIDI.

She exported the CC lane to a CSV. Opened it in a spreadsheet. The energy curve was an irregular sine wave, period varying between 2 and 6 seconds. The frequency of the curve correlated with something — she checked the transcript markers — *words*. Each word was a sample point. The emotional arc of a sentence was the moving average.

She loaded a different .mid file from the same source. This one was a question: "And you can play that music back?"

The pitch contour rose at the end. She watched the CC lane: brightness climbing from 64 to 127 over the last three words. The dimmer followed. The color temperature shifted.

She loaded a third file. A statement: "Think of it as prosodic MIDI."

The pitch contour stayed flat. The CC lane hovered at 48 — a neutral gray. The SysEx didn't change.

She sat back.

This wasn't music. It was *conversation metadata* — the shape of someone speaking, rendered in the protocol that lighting consoles already understood. QLC+ had been receiving MIDI for twenty years. It just had never received *this kind* of MIDI.

She assigned Track 3 — the lyrics — to a text display on her console. The words scrolled past, time-synced to the voice. But she watched the lights, not the text.

The lights told the story better.
