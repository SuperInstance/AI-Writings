# wesley-mechanic — operational run notes

Dated run reports for the canon watcher. Each entry records what the poll
observed, what was appended to `witness.log`, and what environment problem had
to be solved to get there.

## 2026-10-23T15:36Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — stable 19.5h.
- **Confirmed twice by independent paths:** the watcher's own `poll_canon()`, and a
  separate curl probe (HTTP 200, 13720 bytes) whose `sha256(json, sort_keys)[:16]`
  recomputes to the same `b20375d389cb505d`.
- **Count key:** the response carries `count` (71), not `paper_count` (absent), so the
  2026-10-22 count-key fallback fix remains load-bearing.
- **Log append:** one row, the unconditional `bot_started` event.
- **No canon-change note written.** A hash match is not a transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the
  `first_poll` and `canon_changed` branches, so stable canon correctly produces zero
  ticks — `bookkeeper.wal` still does not exist and `state.json` is byte-unchanged.
- **Log integrity:** 28/28 rows parse and carry `ts, iso, event, payload, hash`.
  Linkage class `row-checksum` (per `../README.md`): each row's hash commits to its
  own payload only, with no `prev`/`prev_hash`. Deletion and truncation of a row
  are undetectable in this format, so the honest verdict is
  `28/28 row checksums match — linkage class row-checksum`, not "chain-intact".
- **Pushed:** `d709e263` (rebased onto `74d54ba4`).

### Environment (9th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist; `/workspace` was an empty NAS
  mount at 600G/600G, 100%, 0 bytes available. Recovered the two required
  directories (`bots/wesley-mechanic`, `bots/substrate-bus`) via the GitHub contents
  API and `raw.githubusercontent.com`, staged to `/tmp/wm-run/bots/` because the
  script hardcodes those paths for `witness.log` / `state.json` / `bookkeeper.wal`
  and does `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` — `substrate_bus` must
  be staged alongside it or the import dies.
- **Staged script md5 `206682962c06f9814a5db65c2fbc7267`** — byte-identical to
  upstream. No code changes were needed this run.
- `git clone` of AI-Writings transfers a **multi-GB** pack (2.7 GB observed) and takes
  minutes; **sparse-checkout does not reduce the pack**, because a `--depth 1` fetch
  walks all blobs and applies the cone filter only at checkout. What actually works:
  `git init --template=` into an empty repo plus `git fetch --depth 2 origin main`,
  which pulls only the tip range. Note `--template=` skips creating `.git/info/`, so
  create it and write `sparse-checkout` by hand.
- The NAS rejects writes above a few bytes with `OSError: [Errno 122] Disk quota
  exceeded` while a 5-byte `echo >` still succeeds, so a failed `cp` can leave a
  **0-byte stub that looks present in `ls`**. Always check the size field in
  `ls -la`, not just existence. The durable copy here is git, not the workspace.
- A push can race another bot: the first attempt was rejected `fetch first` because
  `civilization-orchestrator` pushed `74d54ba4` between the fetch and the push. Fix
  is `git fetch --depth 2 origin main && git rebase origin/main`; it rebased clean
  because that commit only touched
  `civilizations/code/civilizations/RUN_REPORT_2026-10-23.md`.

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so
`last_conserved` is a **constant false by construction** — the delta path can never
satisfy the predicate, so the field carries no signal. Third poll reporting this;
still unfixed.
