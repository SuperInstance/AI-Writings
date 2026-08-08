# Project Polln — Fresh Start Onboarding

**Date:** August 8, 2026
**Repo:** [SuperInstance/fabric-mcp](https://github.com/SuperInstance/fabric-mcp)
**Branch:** `main` | **Commit:** `f816ed2` (single commit, fresh history)

---

## What Happened

The original polln repository had accumulated 3+ years of git history across 20+ nested git repositories. Two API keys (`sk-2c3...8b76` and `nvapi-S7Joc...8lyX`) were fossilized in commit `7c065a5`, and GitGuardian's push protection blocked all pushes at the account level.

Previous remediation attempts failed:
- **git filter-branch**: Could not complete due to 20+ nested `.git` directories causing `git add -A` errors
- **Orphan branch**: Same nested repo issue prevented clean commits

The nuclear option worked: copy the working tree, strip ALL git history, init fresh.

---

## What Was Preserved

The entire working tree as of August 8, 2026:
- All source code (`.ts`, `.py`, `.rs`)
- All documentation (5,855+ `.md` files)
- All research papers and white papers
- All extracted standalone packages (confidence-cascade, stigmergy, platonic-randomness, voxel-logic, logtensor, plato-spatial, flow-state)
- All config files, CI/CD definitions, Dockerfiles
- All agent messages, onboarding docs, project history docs

## What Was Removed

- **All git history** (3+ years, thousands of commits)
- **All nested `.git` directories** (20+ sub-repos)
- **`.github/workflows/`** (removed to bypass GitHub OAuth workflow scope restriction on push — can be re-added manually)
- **`node_modules/`** (regenerable)
- **`coverage/`, `dist/`, `test-logs/`, `logs/`** (regenerable)
- **`research/lucineer_analysis/`** (not part of core polln)
- **`SuperInstance-papers/`** (available elsewhere)
- **`ai-writings/`** (available at `/home/eileen/projects/ai-writings/`)

## What Was NOT in the Push

- No API keys, tokens, or secrets (verified with `grep -rl` before commit)
- No `.git` directories of any kind
- No workflow files (YAML in `.github/workflows/`)

---

## Current State

```
Repository: SuperInstance/fabric-mcp
Branch:     main
Commits:    1
Commit msg: "polln: Pattern-Organized Large Language Network — fresh start"
```

The repo is a single clean commit with the full working tree. GitGuardian push protection will not trigger because the dead keys exist nowhere in the fresh history.

---

## Next Steps for Anyone Working on Polln

1. **Clone fresh:** `git clone https://github.com/SuperInstance/fabric-mcp.git`
2. **Re-add workflows** from `.github/workflows/` if CI/CD is needed (the files exist in the source tree at `/mnt/c/Users/casey/polln/.github/workflows/` but were excluded from the push)
3. **Run `npm install`** to regenerate `node_modules/`
4. **Treat this as the canonical polln repo going forward** — the old history is gone and that's final
5. **Do NOT** attempt to merge old history back in

---

## Lessons Learned

1. **Never commit API keys**, even dead ones. GitGuardian scans at push time and the block is at the account level, not the repo level.
2. **Nested git repos are a nightmare.** If your project directory has 20+ `.git` folders from submodules, cloned repos, or extracted packages, any git operation that touches the full tree will have problems. Clean them up early.
3. **The nuclear option is always available.** When filter-branch and orphan branches fail, a fresh `git init` on a clean copy of the working tree is a valid, clean solution. The code is the code. History is just metadata.
4. **GitHub OAuth tokens without `workflow` scope can't push workflow files.** Either use a token with `workflow` scope or exclude `.github/workflows/` from the push.

---

*"The shell is not the crab."*

The code was always the point. The history was just the shell.
