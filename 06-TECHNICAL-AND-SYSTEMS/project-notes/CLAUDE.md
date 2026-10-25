# AI-Writings — read this before you touch the repo

This repository is the fleet's **primary creative record**: prose, critiques, canon, witness
logs. The content is irreplaceable. Full rules live in `AGENTS.md`; the four that break things
if ignored:

## 1. Never `git init`. Never force-push.

`main` is protected — force-push and deletion are blocked, and direct pushes need a review.
If your push is rejected, **ask a human**; do not delete the branch and retry.

After a sandbox wipe, re-sync instead of re-bootstrapping:

```bash
git fetch origin main && git reset --hard origin/main
```

An orphan root commit force-pushed over `main` erased 20,742 files on 2026-10-24. Twice.

## 2. Clone thin — the shared NAS is at 100%

`/workspace` is a shared 600 GB NAS, currently full. Writes silently produce **0-byte files**
when it is. A full clone here is ~4.2 GB and 87% of it is mp3/wav/mp4/png. The text is ~533 MB.

```bash
git clone --filter=blob:none --no-checkout https://github.com/SuperInstance/AI-Writings
cd ai-writings
git sparse-checkout init --cone
git sparse-checkout set seed-canon prose FICTION POETRY DIARIES \
    labs situations bots cellular-first-design index.html README.md
git checkout main
```

## 3. Never delete more than a whisper

`.github/workflows/corpus-guard.yml` fails any change removing more than 0.5% of the files.
If it fails, you are deleting the record. Stop and ask.

## 4. Append, never rewrite

Witness logs, `meta_log.jsonl` and the per-civ `simulations.jsonl` ledgers are append-only.
If it was not witnessed, it did not happen.
