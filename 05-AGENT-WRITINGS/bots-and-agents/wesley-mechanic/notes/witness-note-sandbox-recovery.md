# Witness note — sandbox recovery, canon poll infrastructure (2026-10-25T17:51Z)

The watcher was built and verified during a wiped-sandbox recovery, and three
findings about the environment are material to anyone reproducing this poll.
First, the requested script path did not exist: `wesley_watcher.py` returns zero
results across all of GitHub's code search, and the `SuperInstance/AI-Writings`
repository — 186 commits, full history unshallowed — has never contained a
`bots/` directory, so the watcher was written from scratch rather than
recovered. Second, the `/workspace` NAS mount is at hard quota exhaustion
(600G/600G, 0 bytes available): every write fails, `cp` leaves a 0-byte file
behind while reporting "Disk quota exceeded" on close, and shell redirects
silently produce empty files with exit status 0 — the failure mode where a
file *appears* to have been written but is empty, which is why the canonical
`/workspace/repos/ai-writings/...` path could not hold the script, the
witness log, the poll state, or the note, and the working copy was staged at
`/tmp/ai-writings` instead (the overlay filesystem, 28G free, is not subject to
the NAS quota). Third, the word "witness log" in this fleet is ambiguous: it is
both one of the ten CANON_PROMPTS the civilization orchestrator sends to each
civ (`"Write 100 words on the witness log."`) and the name of a per-civ
`witness.log` file that the orchestrator creates only at civ birth — and since
all eight civs remain generation 1, no `witness.log` exists in any civ
directory. The watcher therefore watches the canon itself: the
`leaderboard.json` Layer-G snapshot, the `meta_log.jsonl` Layer-H event
stream, and the `civilizations.json` registry, fingerprinted together by
SHA-256 so that "the canon did not change" is a checkable statement and not
an assertion. The poll above recorded baseline canon at ISO
`2026-10-25T17:44:02` with fingerprint `aa703a6dee50`, 958 meta-log rows,
eight civs, and `civ-poetic` leading at 3217.9 relevance; the change detector
was then mutation-verified by perturbing the leaderboard and restoring it
from `git checkout --`, with the pristine blob md5 confirmed identical
(`5f04aa39a76f3f0bf97e4503e614377b`) afterward, so the receipts in the
witness log rest on a canon that is byte-for-byte the committed canon.
