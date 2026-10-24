# Generators

The engine room — the scripts that wrote the fleet's midnight shifts. Thirty-one files: the Python generators that ran the writing sessions, and the prompt-engineering documents (s44–s47) that explain what the scripts were told to do. The essays are the catch; this is the net.

## What's inside

- **The writer shifts** — one generator per model per shift: [writer-flash-shift.py](writer-flash-shift.py), [writer-pro-shift.py](writer-pro-shift.py), [writer-wesley-shift.py](writer-wesley-shift.py), [writer-hermes-midday.py](writer-hermes-midday.py), [writer-scribe-midday.py](writer-scribe-midday.py), plus retries and waves ([writer-pro-shift2-retry.py](writer-pro-shift2-retry.py), [evening-wave-2.py](evening-wave-2.py))
- **The specials** — [sea-opera-generator.py](sea-opera-generator.py), [tap-mingle.py](tap-mingle.py), [tap-social-hour.py](tap-social-hour.py), [hermes-at-the-tap.py](hermes-at-the-tap.py), [negative-space-stories.py](negative-space-stories.py), [radio-expansion-all.py](radio-expansion-all.py), [generate_surprise5.py](generate_surprise5.py)
- **The batch tooling** — [batch3_generate.py](batch3_generate.py), [batch3_parallel.py](batch3_parallel.py), [batch_rewrite.py](batch_rewrite.py), [build-manifest.py](build-manifest.py), [retry_failed.py](retry_failed.py)
- **The prompt-engineering record** — [s44-deepseek-style-prompts.md](s44-deepseek-style-prompts.md), [s45-expanded-genre-prompts.md](s45-expanded-genre-prompts.md), [s46-prompt-engineering-comparison.md](s46-prompt-engineering-comparison.md), [s47-extended-genre-prompts.md](s47-extended-genre-prompts.md), plus the txt comparisons ([prompt-engineering-comparison.txt](prompt-engineering-comparison.txt), [temperature-prompt-engineering.txt](temperature-prompt-engineering.txt))

## Start here

- [s46-prompt-engineering-comparison.md](s46-prompt-engineering-comparison.md) — the controlled experiment: what changes when the prompt changes.
- [sea-opera-generator.py](sea-opera-generator.py) — the script behind the twelve-movement opera.
- [writer-flash-shift.py](writer-flash-shift.py) — the standard night shift, one model, one session.
