# minimax-music

Songs generated with the **MiniMax `music-3.0`** API, in rounds. Each round is
a directory with the MP3s and a `manifest.json` carrying the exact prompt,
lyrics, `trace_id`, byte count and `sha256` for every track, so any of them can
be re-requested or audited without guessing what was actually sent.

## Why this directory exists

The ElevenLabs TTS lane is dead: the key authenticates but the account has
**0 credits remaining** (`quota_exceeded`, quota 121,105). The historical
`tts_*.mp3` files in the parent `api-orchestra/` are what that lane produced
while it still had credit. Music generation via MiniMax is the lane that works.

## The model ids moved

Both `music-01` and `music-02` now return `invalid model` from
`POST /v1/music_generation`. The current ids are **`music-3.0`** and
**`music-2.6`**, and the free tiers — `music-3.0-free`, `music-2.6-free`,
`music-cover-free` — were **discontinued 2026-08-20**, so `music-3.0` now
requires a paid / M-plan account.

The old error messages are worth keeping, because they are confusing in the
specific way a good error is not:

| sent | response |
|---|---|
| `music-01` + music-02 params | `cannot use music-02 params on music-01 model` |
| `music-01` alone | `invalid params` |
| `music-02` | `invalid model` |

A 20-second probe times out on a healthy account. Renders here took **61 s to
101 s** per track. Budget for that; it is not a hang.

## What is verified

Every MP3 was checked with `file -b`, not trusted from a 200 response:

```
Audio file with ID3 version 2.4.0, contains: MPEG ADTS, layer III,
v1, 256 kbps, 44.1 kHz, Stereo
```

An HTTP 200 with `base_resp.status_code == 0` and a non-empty body is the
minimum, not the proof. The manifest's `sha256` is the proof.

## Rounds

| round | tracks | genre |
|---|---:|---|
| `r1` | 3 | ambient vocal, lo-fi trip-hop, instrumental |
| `r2` | 2+ | slow electric blues, modern folk |

Lyrics are drawn from the standing fleet doctrine rather than invented for
decoration — "one sound is not a chart, two instruments or nothing at all",
and "what survives is bounded by what the observation carried, no downstream
cleverness recovers what the looking never carried home".
