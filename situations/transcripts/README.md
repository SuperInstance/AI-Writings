# transcripts/ — the inter-relational corpus (WAL)

Hash-chained JSONL transcripts of manager↔crew situations, one file per situation (`<sid>.jsonl`).
Written by [`../../labs/situation-recorder/`](../../labs/situation-recorder/). Each line is a
relation-record (`TASK ROUTE DRAFT DRAW FOLD KEEP DROP MARK OUTCOME`); `refs` are the graph edges.

This is the machine-readable time-capsule that rides alongside the prose commits — the recorded
inputs and outputs of the greater system, saved so a model can later learn to decompose. Design:
[`../arch/INTER-RELATIONAL-INTELLIGENCE.md`](../arch/INTER-RELATIONAL-INTELLIGENCE.md).

Verify any transcript: `python3 ../../labs/situation-recorder/recorder.py --verify <sid>.jsonl`
