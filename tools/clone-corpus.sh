#!/usr/bin/env bash
# clone-corpus.sh — clone AI-Writings for a bot cycle WITHOUT eating the NAS.
#
# A full clone of this repo is ~4.2 GB of worktree (87% of it media: mp3/wav/mp4/png)
# plus ~3.8 GB of .git packfiles. The cron bots did that every 10-15 minutes, which is
# what filled the shared 600 GB volume.
#
# This does a blobless, sparse clone: no media blobs are downloaded, and only the
# text lanes the bots actually read are materialised on disk.
#
#   ./clone_corpus.sh /workspace/repos/ai-writings   -> ~500 MB instead of ~8 GB
#
# Fall back to a full clone only when you genuinely need the media (landing page,
# FICTION with embedded assets, etc.) — and never on a shared cron schedule.
set -euo pipefail

REPO="${AI_WRITINGS_REPO:-https://github.com/SuperInstance/AI-Writings.git}"
DEST="${1:-/workspace/repos/ai-writings}"
BRANCH="${2:-main}"

# Lanes the bots read. Widen only with a reason.
PATHS=(
  seed-canon
  prose
  FICTION
  POETRY
  DIARIES
  labs
  situations
  bots
  cellular-first-design
  tools
  skills
  index.html
  index.json
  README.md
  AGENTS.md
  CLAUDE.md
  .github
)

mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"

git clone --filter=blob:none --no-checkout --depth 50 --branch "$BRANCH" "$REPO" "$DEST"
cd "$DEST"
git sparse-checkout init --cone
git sparse-checkout set "${PATHS[@]}"
git checkout "$BRANCH"

# git-lfs content is not needed for text lanes; skip the LFS smudge to save bandwidth.
export GIT_LFS_SKIP_SMUDGE=1

echo
echo "clone ready: $DEST"
du -sh "$DEST" 2>/dev/null | awk '{print "  worktree+git: " $1 " (a full clone is ~8 GB)"}'
echo
echo "REMINDER: this is a cache. Never 'git init' here, never force-push, never"
echo "'git push origin HEAD' (that created a branch literally named HEAD in this repo)."
echo "Commit to a feature branch and open a PR — main requires one approving review"
echo "and the corpus-guard status check."
