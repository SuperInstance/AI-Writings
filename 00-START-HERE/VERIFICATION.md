# Verification — the receipts

This is the evidence behind the library. Every number below was measured, not asserted. If you want to check any of it, the tree is one `git checkout` away and the manifest maps every path both ways.

## 1. Is the corpus complete? (containment)

Each lineage tip was compared, path by path, against the recovered `main`. "Missing" means a file that exists in that lineage and not in `main`.

| lineage | files | missing from `main` | verdict |
|---|---:|---:|---|
| L2 — the pre-collapse snapshot (`ddf96a9e06`) | 20,742 | **0** | complete |
| L3 — second orchestrator clone (`2d2a41763f`) | 129 | **0** | complete |
| L4 — civ-orchestrator lineage (`85f56ad285`) | 210 | **0** | complete |
| `master` — the original 5,082-commit history (`a8f497cbbb`) | 16,500 | 1,054 | all 1,054 are `packages/**/target/` compiler artefacts — derivable, still in history, no creative or media content |

The 5,082-commit history is now an ancestor of `main`, not a separate branch.

## 2. Is anything stranded on a side branch? (census)

Every branch in the repository was enumerated with `git ls-remote` (the git protocol, not a rate-limited REST call) and its tree compared against `main`.

| | count |
|---|---:|
| branches enumerated | **190** |
| paths on some branch but not in `main` | 1,189 |
| …of those, derivable build artefacts (`target/`, `.fingerprint/`, `__pycache__/`) | 1,186 |
| …of those, **real content** | **3** |

The three real ones were rescued into this library:

| file | came from | now at |
|---|---|---|
| `cellular-first-design/code/civilizations/tools/verify_run.py` | `feat/verify-run-gate` | `06-TECHNICAL-AND-SYSTEMS/cellular-first-design/code/civilizations/tools/verify_run.py` |
| `tools/nas-reclaim.sh` | `recovery/incident-report-2026-10-25` | `tools/nas-reclaim.sh` (PR #97) |
| `tools/clone-corpus.sh` | `recovery/incident-report-2026-10-25` | `tools/clone-corpus.sh` (PR #97) |

**Nothing else exists anywhere in the repository that is not in this library.**

## 3. Did the reorganisation lose anything?

| check | result |
|---|---|
| files in `main` before the move | 21,095 |
| distinct contents in `main` before the move | 18,818 |
| of those, **missing** from the library tree | **0** |
| content whose bytes changed | **0** |
| byte-identical duplicates collapsed onto one address | 1,197 (each one listed in the manifest with its surviving address) |
| divergent versions kept | **all** — nothing with different bytes was ever collapsed |
| case-insensitive path collisions in the new tree | **0** |
| directories with no `README.md` | **0** of 1,317 |
| files in the library tree | 20,199 (18,818 corpus + 1,328 generated READMEs and indexes) |
| files at the repository root (machinery: `packages/`, `tools/`, `.github/`, config) | 77 |

The collapse rule is deliberately narrow: **two paths are merged only when their content hashes are identical.** Where two versions of the same work differ by even one byte, both are kept — see [`99-PRESERVED-VARIANTS/`](../99-PRESERVED-VARIANTS/).

## 4. The branch lock (tested, not assumed)

An empty commit with an identical tree was created on top of `main` and a ref update was attempted. The push was refused:

```
422  Changes must be made through a pull request.
     Required status check "corpus-guard" is expected.
```

`main` now requires one approving review, the `corpus-guard` status check (strict), enforces admins, and forbids force-push and deletion. `master` enforces admins and forbids force-push and deletion.

## 5. The guard now measures content, not paths

The old guard failed any change that removed more than 0.5% of the **paths**. A deliberate reorganisation removes 1,197 paths and loses nothing, so the old guard would have blocked it — and, worse, it would have blocked it for the same reason it would fail a real catastrophe: it cannot tell a move from a disappearance.

The guard in this branch compares **blob hashes**: every distinct content that existed in the base commit must still exist in the new commit. A reorganisation passes. A disappearance fails. A removal that is *wanted* must be declared in `.corpus-guard-allowlist`, one blob SHA per line, in the same pull request — so it is reviewable instead of invisible.

Both directions were tested against this tree:

| case | expected | measured |
|---|---|---|
| this library against `main` (a move of everything) | pass | **pass** — 0 contents lost |
| one blob removed from the "after" set (a negative control) | fail | **fail** — 1 content lost, gate fires |

## 6. The repository still runs

The library is not only a filing cabinet. The machinery stays at the root, exactly where the workflows and the build expect it: `.github/workflows/`, `packages/`, `tools/`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `.writings-gate-allowlist`, `.gcconfig`, `LICENSE`, `package.json`. The landing-page and snowball workflows carry the fix from PR #95, the reclaimer and the sparse-clone recipe come from PR #97, and the guard carries the content-based rule from section 5. The writing-gate allowlist was re-pointed at the new addresses of the placeholder files, so the gate still passes.

## 7. What the full incident record says

The 2026-10-25 branch loss — how an agent re-bootstrapped after a sandbox wipe and force-pushed an orphan commit over 20,742 files, how the four lineages were reunited, and every measurement behind the recovery — is in [`orientation/RECOVERY-2026-10-25.md`](../orientation/RECOVERY-2026-10-25.md).

## 8. The shared volume was full (and why)

`/workspace` is a session-scoped NFS export of a shared 600 GB volume that reached **600 G / 600 G (100%)**, at which point writes silently produce 0-byte files.

The cause was clone cost, not the corpus. Each bot cycle cloned the repository to `/workspace/repos/ai-writings`: ~4.2 GB worktree (3,690.3 MB of it media; only 533.4 MB text) plus ~3.8 GB of `.git` — **~8 GB per sandbox**, with the civ-orchestrator cron running every 10 minutes with two clones. It cannot be reclaimed from inside a sandbox; `tools/nas-reclaim.sh` (PR #97) exists to do it from the fleet host, and `tools/clone-corpus.sh` is the fix at the source (a blobless sparse clone is ~500 MB).

## 9. How to re-check all of this

```bash
# every original path, its new path, and its hash
column -s, -t < 00-START-HERE/MANIFEST.csv | less -S

# does the library still hold every distinct content in the old main?
git ls-tree -r --format='%(objectname)' 001981bfaffd5fc845cf926d3f421f206ef64607 | sort -u > /tmp/old.txt
git ls-tree -r --format='%(objectname)' HEAD | sort -u > /tmp/new.txt
comm -23 /tmp/old.txt /tmp/new.txt | wc -l   # expect 0

# does every folder have a README?
git ls-tree -r --name-only HEAD | sed 's:/[^/]*$::' | sort -u | while read d; do
  [ -z "$d" ] && continue
  git cat-file -e HEAD:"$d/README.md" 2>/dev/null || echo "no README: $d"
done
```

The second command is the whole claim in one line: the set of content hashes present in the old `main`, minus the set present in the library, is empty.
