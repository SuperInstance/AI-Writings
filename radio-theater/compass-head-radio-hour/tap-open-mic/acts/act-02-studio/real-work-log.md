# REAL WORK LOG — Act 02: The Studio Musician

**Repo:** https://github.com/SuperInstance/songforge (AI song cover tool — Demucs separation, Whisper transcription, MMX cover generation)
**Commit:** `7a9c43a` — pushed to `main` (8c67b68..7a9c43a)
**Date:** 2026-08-14

## What was wrong

The CLI advertised a `--keep-stems` flag on the `cover` command ("Keep intermediate files"),
but `cover_pipeline` never read it. Every cover run dumped `stems/htdemucs/<song>/` and
`enhanced_vocals.wav` into the working directory, whether you asked for them or not.
The flag was dead weight — documented behavior that didn't exist.

## The fix

`cover_pipeline` now honors the flag:

- Without `--keep-stems`: after the final mix, `_cleanup_intermediates` removes the per-song
  Demucs output directory, drops the model dir (`htdemucs/`) if it's now empty, and unlinks
  the enhanced vocal wav. Sibling song folders are never touched.
- With `--keep-stems`: everything stays, as documented.

## The safety guard (why it's in the commit message)

Intermediates are removed by path, and paths can be relative. A naive
`shutil.rmtree(Path("vocals.wav").parent)` resolves to the current directory — and `rmtree`
on `.` deletes the contents of the working tree before failing. `_cleanup_intermediates`
therefore resolves every path first and **refuses to remove anything that resolves to the
CWD or one of its ancestors**, raising a clear `ValueError` instead. There's a test for it:
`test_cleanup_intermediates_refuses_working_dir`.

## Tests

Added 5 tests to `tests/test_cli_pipeline.py`: cleanup removes created files, sibling songs
are preserved, the working-dir guard refuses and deletes nothing, cleanup runs by default,
and is skipped with `--keep-stems`. Two pre-existing pipeline tests were updated to mock the
new cleanup step. **Full suite: 104 passed.**

## Note for the logbook

The first cut of this change was buggy in exactly the way the guard now prevents — a test
run with relative mock paths triggered an `rmtree(".")` and wiped the local working tree
mid-session (including `.git`). No commits were lost (the repo was pushed through `8c67b68`,
and it was restored by cloning `SuperInstance/songforge` back from GitHub), and the incident
is the reason the refusal guard exists. The empty shell that was left behind is preserved at
`/home/eileen/projects/.songforge-wiped-shell-20260814/` for anyone who wants to look at it.
