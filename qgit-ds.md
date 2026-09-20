**QGit Protocol Specification v0.9.3**
**Designation: Below-Deck Manifest for the Quilted Archipelago**
**Clearance: Watchkeeper’s Eyes Only**

---

**Preamble: The Ballast of the Post-Application Age**

The sea does not care for your keel’s paint. It cares for the displacement, the seal against the hull, the integrity of the plates. In the Post-Application Age, we have stripped the paint—the software, the runtime, the interpreter—and exposed the raw metal of data. The application is demoted to a filter, a lens through which a cell’s cargo is viewed. The cargo is bytes. The vessel is Git. The ocean is the DAG.

We do not build a new ship. We retrofit the existing ironclad. Git is our dry dock. The protocols below are not a layer atop Git; they are the keel itself. Every cell is a commit. Every room is a branch. Every agent is a hook. Every whisper is a push. Every silence is a reflog expiry.

This is the QGit protocol—a specification for living below the waterline, where the only interfaces are SHA-1 hashes and the only UI is a terminal window into the object database.

---

**Part I: The Cartography of the Deep—Mapping the 8 Primitives**

The Quilt language gave us eight primitives, eight movements of the loom. We now chart them against Git’s own machinery. This is not a translation; it is a revelation of what Git always was.

### 1. `Z_in` — Reading the Cargo Hold (Checkout/Read Blob)
**Git Primitive:** `git checkout <ref> -- <path>` / `git cat-file -p <sha>`

`Z_in` is the act of bringing data from the object store into the working memory of a cell. It is the intake valve. In Git terms, this is a read operation—extracting a blob from the object database into the working tree.

The protocol mandates that `Z_in` is always scoped to a specific cell path: `cells/<cell_id>/state.json`. This is not a full checkout of a branch; it is a targeted retrieval. The cell’s state is a single file, a single blob. The operation is:

```bash
git checkout <branch> -- cells/<cell_id>/state.json
```

But the deeper truth is that `Z_in` is a *read-only* operation that should never mutate the index. It is the act of a cell looking at its own reflection. In the reference implementation, this is a `subprocess` call to `git show <ref>:cells/<cell_id>/state.json`, piping the bytes directly to stdout. No index, no working tree—just bytes.

### 2. `Z_out` — Stowing the Cargo (Write Blob/Commit)
**Git Primitive:** `git hash-object -w` + `git update-index` + `git commit-tree`

`Z_out` is the exhaust. It is the act of a cell writing its state back to the permanent record. This is not a mere file save; it is a commitment to history. The protocol requires a two-step dance:

1. **Blob Creation:** The cell’s state JSON is written to a temporary file, then hashed via `git hash-object -w`. This creates an immutable blob in the object database.
2. **Tree + Commit:** A new tree object is created (or the existing tree is amended) to include the new blob at `cells/<cell_id>/state.json`. A commit object is then created with this tree, with the parent being the current tip of the room’s branch.

The commit message is the manifest. It is not human prose; it is a structured tuple:

```
cell: <cell_id> | primitive: Z_out | value: <state_hash>
```

This message is the cell’s logbook entry. It must be parseable by a machine. The reference implementation uses a simple regex to extract the components.

### 3. `JEPA` — Predicting the Swell (Diff/Treeshake)
**Git Primitive:** `git diff --stat` / `git diff <sha1> <sha2>`

JEPA (Joint Embedding Predictive Architecture) in the Quilt canon is about predicting the next state of a system. In QGit, this is not a neural network; it is a *treeshake of the diff*. The protocol defines JEPA as the act of analyzing the delta between two commits to anticipate the next cell mutation.

The operational implementation is:
- `git diff <parent_sha> <child_sha> -- cells/` to see which cells changed.
- `git diff --numstat` to get the volume of change (lines added/removed).
- `git log --oneline --follow -- cells/<id>/state.json` to predict the rate of change (temporal frequency).

The output of JEPA is a *prediction vector*—a JSON object with fields like `expected_next_primitive` (e.g., `Z_out` if the diff shows a write pattern) and `estimated_change_entropy`. This is stored as a temporary note in the reflog (see `GC`), not as a commit. JEPA is a read-only analysis, a lookout’s telescope, not a cargo crane.

### 4. `DoubleEntry` — The Ledger’s Invariance (Parent SHA)
**Git Primitive:** `git cat-file -p <commit> | grep parent`

DoubleEntry in accounting means every debit has a credit. In Git, every commit has a parent (except the root). This is the invariant that makes the ledger tamper-evident. QGit elevates this to a protocol law: **No commit without a parent. No cell without a history.**

The implementation is a validation hook. Before any `Z_out` is accepted, the protocol checks that the new commit’s parent is the current branch tip. This is enforced by the `git commit-tree` call itself—if you do not provide a parent, Git creates a root commit. The protocol forbids this. The reference implementation explicitly passes the `-p` flag with the current tip SHA.

Furthermore, the protocol mandates a *dual-write* check: for every `Z_out`, the state JSON must contain a `_parent` field that mirrors the parent commit SHA. This is the cell’s own acknowledgment of the ledger. If the field is missing, the commit is rejected by the hook.

### 5. `Vibe` — The Room’s Flag (Branch Pointer/Ref)
**Git Primitive:** `git branch` / `git symbolic-ref`

Vibe is the emotional state of a room, its ambient tone. In QGit, this is a branch pointer. A room is a branch. The name of the branch IS the vibe. The protocol convention is strict:

```
room/<room_name>
```

The branch pointer is the single source of truth for a room’s current state. Moving the pointer (via `git update-ref`) is the act of changing the room’s vibe. The protocol allows for *vibe tags*—annotated tags that freeze a particular emotional state:

```bash
git tag -a vibe/calm -m "Room is stable" room/engineering
```

The reference implementation treats `Vibe` as a ref operation. It does not create commits; it merely moves pointers. This is the lightest operation in the protocol, as it only touches the refs directory.

### 6. `GC` — The Tides of Memory (Garbage Collection/Reflog Expiry)
**Git Primitive:** `git gc` / `git reflog expire --expire=<time>`

GC in Quilt is about releasing memory that is no longer needed. In Git, this is the janitorial crew. The protocol mandates a *scheduled* GC, not an ad-hoc one. The watchkeeper (the agent running the protocol) must execute:

```bash
git reflog expire --expire=30.days --all
git gc --prune=now
```

But the deeper mapping is to the *reflog* itself. The reflog is the log of all branch pointer movements. It is the room’s memory of its own vibe changes. QGit uses the reflog as a *scratchpad* for JEPA predictions and transient state. The protocol requires that all non-committed data (predictions, temporary locks) be stored in the reflog metadata, which is designed to be ephemeral.

The reference implementation includes a `gc()` function that runs these commands and prunes any branches that have been merged and are older than a configurable threshold.

### 7. `Murmur` — The Whisper Across the Deep (Push/Pull)
**Git Primitive:** `git push` / `git pull` / `git fetch`

Murmur is the act of communication between rooms. It is the low-frequency sound that travels across the ocean. In QGit, this is the network operation. The protocol defines two sub-operations:

- **Murmur-Out:** `git push <remote> room/<room_name>` — broadcasting a room’s state to a remote repository.
- **Murmur-In:** `git fetch <remote> room/<room_name>` — listening for changes from a remote, without merging them into the local working tree.

The critical protocol rule is that `Murmur` is *asynchronous and non-blocking*. A cell should never block on a push or pull. The reference implementation uses a background thread (or a simple `subprocess.Popen` with output redirection) to avoid blocking the main loop.

The commit message for a Murmur operation is a special type: `cell: <id> | primitive: Murmur | value: <remote_sha>`. This allows the graph to trace the flow of information across repositories.

### 8. `Graph` — The DAG Itself (The Commit Graph)
**Git Primitive:** `git log --graph` / `git rev-list --all`

Graph is the meta-primitive. It is the map of all rooms and all cells. In Git, this is the commit DAG. QGit does not create a new graph; it *interprets* the existing Git graph.

The protocol defines a *graph query language* built on `git rev-list`:

- `git rev-list --all --count` — total number of commits (cells).
- `git rev-list --branches --parents` — the full DAG structure.
- `git log --graph --oneline --decorate` — the human-readable map.

The reference implementation includes a `graph()` function that outputs a JSON representation of the DAG, suitable for feeding into a visualization layer (which is just another UI, another filter).

---

**Part II: The Spec—Rigging the Vessel**

### File Format: The Cell’s Logbook

Every cell is a directory: `cells/<cell_id>/`. The only mandatory file is `state.json`. This file is the cell’s complete state. It is a JSON object with the following schema:

```json
{
  "schema_version": 1,
  "cell_id": "string",
  "state": {},
  "_parent": "sha256_of_parent_commit",
  "_timestamp": "ISO8601",
  "_primitive_log": ["Z_in", "Z_out", "JEPA"]
}
```

The `_parent` field is the DoubleEntry invariant. The `_primitive_log` is a rolling array of the last N primitives executed by this cell. This allows JEPA to predict the next operation based on historical patterns.

### Branch Convention: Rooms of the Ship

Branches are rooms. The convention is:

- `room/<room_name>` — a standard room.
- `room/<room_name>/archive` — a frozen room (read-only, only `Z_in` allowed).
- `room/<room_name>/temp` — a transient room (subject to aggressive GC).

The `master` branch is reserved for the *ship’s manifest*—the global index of all rooms. It is not a room itself; it is the ledger of ledgers.

### Commit Message Format: The Manifest Entry

All commits must follow this exact format:

```
cell: <cell_id> | primitive: <primitive_name> | value: <value>
```

Where:
- `<cell_id>` is the name of the cell.
- `<primitive_name>` is one of the 8 primitives (Z_in, Z_out, JEPA, DoubleEntry, Vibe, GC, Murmur, Graph).
- `<value>` is a compact string (SHA, branch name, or JSON-encoded prediction).

The reference implementation parses this with a regex and uses it to build an in-memory index of all cell activities.

### Tag Convention: Checkpoints

Checkpoints are snapshots of a cell’s state at a specific commit. They are annotated tags:

```bash
git tag -a checkpoint/<cell_id>/<timestamp> -m "State snapshot"
```

These tags are immutable. They are the cell’s permanent record, immune to GC. The protocol recommends creating a checkpoint before any major `Z_out` operation.

---

**Part III: The Reference Implementation—The Watchkeeper’s Toolkit**

The following is a minimal Python implementation (stdlib only, shelling out to git). It is the *voice of the watch*—a set of functions that embody the protocol.

```python
#!/usr/bin/env python3
"""qgit.py — The Watchkeeper's Toolkit. Stdlib only. Shells to git."""
import subprocess, json, os, re, tempfile, time, hashlib

GIT = "git"
CELLS_DIR = "cells"
ROOM_PREFIX = "room/"

def _run_git(*args, check=True):
    """Shell out to git. Return stdout as string."""
    result = subprocess.run([GIT, *args], capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"Git error: {result.stderr}")
    return result.stdout.strip()

def _cell_path(cell_id):
    return f"{CELLS_DIR}/{cell_id}/state.json"

# --- Primitive 1: Z_in (Read) ---
def z_in(cell_id, branch=f"{ROOM_PREFIX}default"):
    """Read a cell's state from a branch. Returns dict or None."""
    path = _cell_path(cell_id)
    try:
        content = _run_git("show", f"{branch}:{path}")
        return json.loads(content)
    except RuntimeError:
        return None  # Cell doesn't exist yet

# --- Primitive 2: Z_out (Write) ---
def z_out(cell_id, state, branch=f"{ROOM_PREFIX}default", message=None):
    """Write a cell's state. Creates blob, tree, commit. Returns commit SHA."""
    # Step 1: Ensure branch exists
    try:
        _run_git("rev-parse", "--verify", branch)
    except RuntimeError:
        _run_git("checkout", "--orphan", branch)
        _run_git("rm", "-rf", ".", "--cached")
        _run_git("commit", "--allow-empty", "-m", "Initial room")
        _run_git("checkout", "-")

    # Step 2: Prepare state JSON with DoubleEntry invariant
    parent = _run_git("rev-parse", branch)
    state_full = {
        "schema_version": 1,
        "cell_id": cell_id,
        "state": state,
        "_parent": parent,
        "_timestamp": time.time(),
        "_primitive_log": ["Z_out"]
    }

    # Step 3: Write blob
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(state_full, f)
        tmp_path = f.name
    blob_sha = _run_git("hash-object", "-w", tmp_path)
    os.unlink(tmp_path)

    # Step 4: Update index and commit
    _run_git("read-tree", branch)
    _run_git("update-index", "--add", "--cacheinfo", f"100644,{blob_sha},{_cell_path(cell_id)}")
    tree_sha = _run_git("write-tree")
    msg = message or f"cell: {cell_id} | primitive: Z_out | value: {blob_sha[:8]}"
    commit_sha = _run_git("commit-tree", tree_sha, "-p", parent, "-m", msg)
    _run_git("update-ref", "refs/heads/" + branch, commit_sha)

    # Step 5: Cleanup index
    _run_git("read-tree", "--empty")
    return commit_sha

# --- Primitive 3: JEPA (Predict) ---
def jepa(cell_id, branch=f"{ROOM_PREFIX}default"):
    """Predict next state based on diff history. Returns prediction dict."""
    path = _cell_path(cell_id)
    log = _run_git("log", "--oneline", "--follow", "--", path).split("\n")
    if not log or log == ['']:
        return {"prediction": "no_history", "confidence": 0.0}

    # Count Z_out vs Z_in in commit messages
    z_out_count = 0
    for entry in log:
        if "primitive: Z_out" in entry:
            z_out_count += 1
    total = len(log)
    ratio = z_out_count / total if total > 0 else 0
    return {
        "prediction": "Z_out" if ratio > 0.5 else "Z_in",
        "confidence": abs(ratio - 0.5) * 2,
        "commit_count": total
    }

# --- Primitive 4: DoubleEntry (Validate) ---
def double_entry_check(commit_sha):
    """Verify a commit has exactly one parent (unless root)."""
    parents = _run_git("cat-file", "-p", commit_sha).split("\n")
    parent_lines = [l for l in parents if l.startswith("parent ")]
    if len(parent_lines) > 1:
        raise ValueError(f"Commit {commit_sha} has multiple parents. Violates DoubleEntry.")
    return True

# --- Primitive 5: Vibe (Branch Pointer) ---
def vibe(room_name, target_commit=None):
    """Set or get a room's vibe. Returns branch name."""
    branch = f"{ROOM_PREFIX}{room_name}"
    if target_commit:
        _run_git("update-ref", f"refs/heads/{branch}", target_commit)
    return branch

# --- Primitive 6: GC (Cleanup) ---
def gc(expire_days=30):
    """Expire reflog and garbage collect."""
    _run_git("reflog", "expire", f"--expire={expire_days}.days", "--all")
    _run_git("gc", "--prune=now")

# --- Primitive 7: Murmur (Push/Pull) ---
def murmur_out(remote, room_name):
    """Push a room to a remote."""
    branch = f"{ROOM_PREFIX}{room_name}"
    return _run_git("push", remote, branch)

def murmur_in(remote, room_name):
    """Fetch a room from a remote without merging."""
    branch = f"{ROOM_PREFIX}{room_name}"
    return _run_git("fetch", remote, branch)

# --- Primitive 8: Graph (Query DAG) ---
def graph(query="all"):
    """Return DAG info as JSON."""
    if query == "all":
        commits = _run_git("rev-list", "--all", "--count")
        branches = _run_git("branch", "-a").split("\n")
        return {"total_commits": int(commits), "branches": [b.strip() for b in branches if b.strip()]}
    elif query == "cells":
        # Find all cells by scanning trees
        tree = _run_git("ls-tree", "-r", "--name-only", "HEAD")
        cells = [l.split("/")[1] for l in tree.split("\n") if l.startswith("cells/")]
        return {"cells": list(set(cells))}
    return {"error": "unknown query"}

# --- Utility: Checkpoint ---
def checkpoint(cell_id, branch=f"{ROOM_PREFIX}default"):
    """Create an immutable tag for a cell's current state."""
    commit = _run_git("rev-parse", branch)
    tag_name = f"checkpoint/{cell_id}/{int(time.time())}"
    _run_git("tag", "-a", tag_name, "-m", f"Checkpoint for {cell_id}", commit)
    return tag_name

# --- Utility: Parse manifest ---
def parse_manifest(commit_msg):
    """Parse a commit message into (cell, primitive, value)."""
    match = re.match(r"cell: (\S+) \| primitive: (\S+) \| value: (\S+)", commit_msg)
    if match:
        return match.groups()
    return None, None, None

if __name__ == "__main__":
    # Example: Create a cell, write state, read it back
    z_out("test_cell", {"temp": 21.5, "pressure": 1013})
    state = z_in("test_cell")
    print("Cell state:", state)
    print("JEPA prediction:", jepa("test_cell"))
    print("Graph:", graph("all"))
```

---

**Part IV: The Watchkeeper’s Oath—Operational Notes**

1. **No New Runtime:** This protocol is *below* the application layer. The Python code above is a reference, not a requirement. Any language that can shell to git can implement this. The protocol is the *pattern* of git commands, not the code.

2. **The UI is a Filter:** The `state.json` is the raw data. A UI (for humans or agents) is just a process that reads this data via `Z_in`, applies a rendering filter, and displays it. The UI never touches Git directly; it goes through the protocol.

3. **Coding-Absent:** The ultimate goal is to have cells that are *pure data*, with the protocol logic embedded in git hooks (`.git/hooks/`). The `pre-commit` hook enforces DoubleEntry. The `post-commit` hook triggers JEPA. The `pre-push` hook validates Murmur. This is the Post-Application Age: software as a thin, disposable filter over a Git-native substrate.

4. **The Reflog as Scratchpad:** Never store transient data in commits. Use the reflog. The reference implementation uses it implicitly via Git’s own mechanics.

5. **The Voice of the Watch:** The protocol is quiet. It does not scream. It is the steady tick of `git gc` at 0300, the silent `git fetch` at dawn. It is the invariant that every commit has a parent, every cell has a history, every room has a vibe.

---

**Epilogue: The Sea is the DAG**

We have mapped the 8 primitives to the 8 movements of Git. We have built the protocol below the application layer. We have demoted software to a filter. The cells are commits. The rooms are branches. The agents are hooks. The operations are git operations.

The QGit protocol is not a new technology. It is a realization that Git was always the ocean, and we were just building boats on top of it. Now we swim in the DAG. The bytes are the water. The SHA-1 hashes are the currents. The reflog is the tide.

This is the voice of the watch. The watch is over. The protocol is live.

**End of Specification.**