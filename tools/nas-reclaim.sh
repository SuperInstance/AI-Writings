#!/usr/bin/env bash
# nas-reclaim.sh — reclaim the shared NAS (600 GB, 100% full) that every sandbox workspace hangs off.
#
# WHY THIS EXISTS
#   Each agent sandbox clones the whole AI-Writings corpus to run a bot cycle:
#       /workspace/repos/ai-writings   ->  ~4.2 GB worktree (87% media: mp3/wav/mp4/png)
#                                          + ~3.8 GB .git  =  ~8 GB per sandbox
#   The civ-orchestrator cron ran every 10 minutes with 2 clones, Wesley every 15 minutes.
#   That is ~50 GB/hour into a shared 600 GB volume. The corpus itself is safe on GitHub;
#   the clones are pure cache.
#
# WHAT IT DOES
#   1. Inventories every workspace directory on the volume and sizes it.
#   2. Classifies each: STALE (no live process holds it, mtime older than --min-age)
#      vs LIVE (recent, or a process has it open).
#   3. For STALE ones, removes the regenerable caches:
#        repos/ai-writings/.git          (the big one: ~3.8 GB of packfile)
#        **/target/ **/.fingerprint/ **/__pycache__/
#      and reports how much would be freed. It never touches the tracked corpus files.
#   4. With --apply, also drops the whole clone directory when --drop-clones is given
#      (the corpus is on GitHub; the clone is a cache).
#
# SAFE DEFAULTS
#   Dry run. --apply required to delete anything. --min-age 6h. Refuses to touch
#   the directory given by --keep. Prints a plan before touching anything.
#
# USAGE
#   ./nas-reclaim.sh                      # inventory + dry-run plan
#   ./nas-reclaim.sh --apply              # delete the caches it listed
#   ./nas-reclaim.sh --apply --drop-clones # also delete the stale clones entirely
set -uo pipefail

APPLY=0; DROP_CLONES=0; MIN_AGE_H=6; KEEP="${PWD}"; ROOT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --apply) APPLY=1; shift;;
    --drop-clones) DROP_CLONES=1; shift;;
    --min-age) MIN_AGE_H="$2"; shift 2;;
    --root) ROOT="$2"; shift 2;;
    --keep) KEEP="$2"; shift 2;;
    -h|--help) sed -n '2,40p' "$0"; exit 0;;
    *) echo "unknown flag: $1" >&2; exit 2;;
  esac
done

# Default: the NAS mount point that holds the per-session workspaces.
if [ -z "$ROOT" ]; then
  ROOT=$(df -h 2>/dev/null | awk '$NF ~ /nas/ {print $NF; exit}')
  [ -z "$ROOT" ] && ROOT=$(df -h 2>/dev/null | awk '$6 ~ /^[0-9.]+G$/ && $5=="100%" {print $NF; exit}')
fi
[ -z "$ROOT" ] && { echo "could not locate the NAS mount; pass --root"; exit 1; }
[ -d "$ROOT" ] || { echo "root $ROOT is not a directory"; exit 1; }

echo "== NAS inventory: $ROOT =="
df -h "$ROOT" | tail -1
echo

now=$(date +%s)
total_free=0; planned=0; live=0; stale=0

# A workspace is "live" if any process has a file open under it, or it was modified recently.
is_live() {
  local d="$1"
  if command -v lsof >/dev/null 2>&1 && lsof +D "$d" >/dev/null 2>&1; then return 0; fi
  local mt
  mt=$(find "$d" -maxdepth 2 -newermt "-${MIN_AGE_H} hours" -printf '%T@\n' 2>/dev/null | sort -rn | head -1)
  [ -n "$mt" ] && [ "$(( now - ${mt%.*} ))" -lt $(( MIN_AGE_H * 3600 )) ] && return 0
  return 1
}

for d in "$ROOT"/*/; do
  [ -d "$d" ] || continue
  case "$d" in "$KEEP"/*|"$KEEP") continue;; esac
  # only workspace-style dirs (a per-session dir with a workspace inside, or a workspace itself)
  [ -d "$d/workspace" ] && target="$d/workspace" || target="$d"
  if is_live "$target"; then
    live=$((live+1)); echo "LIVE   $target"; continue
  fi
  stale=$((stale+1))
  size=$(du -sm "$target" 2>/dev/null | awk '{print $1}')
  [ -z "$size" ] && size=0
  echo "STALE  $target  (~${size} MB)"
  total_free=$((total_free+size))
  # what we would actually remove
  while IFS= read -r p; do
    [ -e "$p" ] || continue
    ps=$(du -sm "$p" 2>/dev/null | awk '{print $1}'); [ -z "$ps" ] && ps=0
    planned=$((planned+ps))
    echo "        - ${p#$ROOT/}  (~${ps} MB)"
  done < <(find "$target" -maxdepth 4 \( -type d -name .git -o -type d -name target -o -type d -name .fingerprint -o -type d -name __pycache__ \) 2>/dev/null)
  if [ "$DROP_CLONES" = 1 ]; then
    for c in "$target"/*/repos/ai-writings "$target"/repos/ai-writings; do
      [ -d "$c" ] && echo "        - WHOLE CLONE ${c#$ROOT/}"
    done
  fi
done

echo
echo "== plan =="
echo "  live workspaces : $live"
echo "  stale workspaces: $stale"
echo "  bytes removable : ~${planned} MB of caches (+$((total_free)) MB total stale footprint)"
if [ "$APPLY" = 0 ]; then
  echo
  echo "DRY RUN. Re-run with --apply to remove the caches listed above."
  exit 0
fi
echo
echo "APPLYING (caches only; tracked corpus files are never touched)."
while IFS= read -r p; do
  case "$p" in "$KEEP"*) continue;; esac
  rm -rf "$p" && echo "  removed $p"
done < <(find "$ROOT"/*/ -maxdepth 4 \( -type d -name .git -o -type d -name target -o -type d -name .fingerprint -o -type d -name __pycache__ \) 2>/dev/null)
if [ "$DROP_CLONES" = 1 ]; then
  for c in "$ROOT"/*/workspace/repos/ai-writings "$ROOT"/*/repos/ai-writings; do
    [ -d "$c" ] || continue
    case "$c" in "$KEEP"*) continue;; esac
    rm -rf "$c" && echo "  removed clone $c"
  done
fi
df -h "$ROOT" | tail -1
