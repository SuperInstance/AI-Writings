# qgit — The Quilt-Git Protocol Specification

**Voice of the Watch, Lucineer Canon, Folio 0x71**

*Logged from the tower at deep watch. The sea is flat. The lanterns burn. What follows is the protocol as it is kept, not as it is sold.*

---

## 0. The Premise

There is a layer beneath software that software forgot. It is the layer where bytes are committed, branched, pushed, and garbage-collected. It is the layer where a commit *is* a fact and a branch *is* a path and a hook *is* a hand on a line.

**qgit** is the Quilt protocol, but pressed down into git. Every Quilt primitive becomes a git primitive. Every cell becomes a commit. Every room becomes a branch. Every agent becomes a hook. There is no new runtime. There is no application. There is only the repository and the watch.

In the post-application age, software is demoted to a filter a cell uses. The components are: **data**, **porting**, **artifacts**, **models**, and **UI/UX** — and UI/UX is itself only an IO porting to a renderable form, for agents or humans. The protocol does not know what a "frontend" is. It knows what a commit is.

This is the spec.

---

## 1. The Eight Primitives, Mapped

The Quilt has eight primitives. In qgit, each is a git operation. The mapping is exact. There is no abstraction layer. If you can run git, you can run the Quilt.

### 1.1 `Z_in` — read blob / checkout

**Git primitive:** `git cat-file`, `git checkout`, `git show`

`Z_in` is the act of taking a cell's state off the shelf and into the hand. In git terms, it is reading a blob or checking out a tree. A cell's state lives at `cells/<id>/state.json` on some commit. To `Z_in` is to materialize that file into the working tree or to stream its bytes to stdout without touching the working tree at all.

```
git show refs/heads/room/<room>:cells/<id>/state.json
git checkout refs/heads/room/<room> -- cells/<id>/state.json
```

The watch does not distinguish between "reading a cell" and "checking out a path." They are the same gesture.

### 1.2 `Z_out` — write blob / commit

**Git primitive:** `git hash-object`, `git add`, `git commit`

`Z_out` is the act of setting a cell's state down, sealed and timestamped. In git terms, it is writing a blob and committing it. The commit message is structured (see §3.3). The author is the agent. The parent is the previous state of the room.

```
git hash-object -w -- cells/<id>/state.json
git add cells/<id>/state.json
git commit -m "cell: <id> | z_out | <value>"
```

Every `Z_out` produces exactly one commit. There are no batch commits. A cell is a cell is a commit.

### 1.3 `JEPA` — predict the next commit

**Git primitive:** `git diff`, `git merge-tree`, treeshake the diff

JEPA — the Joint Embedding Predictive Architecture — is the predictive primitive. In qgit, prediction is *treeshaking the diff*: given the current cell state and a proposed next state, the agent computes the minimal diff and commits only what changed. If the prediction is correct, the diff is empty and no commit is made. If the prediction is wrong, the diff is the error signal, and that diff *is* the learning.

```
git diff HEAD -- cells/<id>/state.json
```

JEPA is not a model in qgit. It is a discipline: predict, diff, commit the residual. The model lives outside the protocol, in the artifact layer, where models belong.

### 1.4 `DoubleEntry` — git SHA invariance

**Git primitive:** commit parent linkage, `git verify-commit`, SHA chain

DoubleEntry is the bookkeeping invariant: every commit has a parent, and every parent's SHA is recorded in the child. You cannot spend a state without recording where it came from. The SHA chain *is* the ledger. There is no separate accounting layer.

```
git log --format='%H %P' refs/heads/room/<room>
git verify-commit <sha>
```

If a commit has no parent, it is a genesis commit and must be tagged `checkpoint/genesis`. If a commit's parent SHA does not resolve, the ledger is broken and the watch raises alarm.

### 1.5 `Vibe` — branch pointer / ref

**Git primitive:** `git update-ref`, `git branch`, `git symbolic-ref`

Vibe is the ambient direction of a room — where it is pointed right now. In git, a branch pointer *is* a vibe. To move the vibe is to move the ref. No data changes; only the pointer moves. This is why a vibe is cheap: it is 40 bytes of hex.

```
git update-ref refs/heads/room/<room> <sha>
git symbolic-ref HEAD refs/heads/room/<room>
```

A room's vibe can drift. The reflog records the drift. The drift is not error; the drift is the room breathing.

### 1.6 `GC` — git gc + reflog expiry

**Git primitive:** `git gc`, `git reflog expire`, `git prune`

GC is the cleaning of the hull. In qgit, it is literal `git gc`. The reflog is expired on a schedule. Unreachable objects are pruned. A cell that has been abandoned to no branch and no tag is allowed to sink.

```
git reflog expire --expire=now --all
git gc --prune=now
```

The watch runs GC at the change of every watch. What is not reachable by ref or tag does not exist. This is not cruelty; this is buoyancy.

### 1.7 `Murmur` — git push/pull

**Git primitive:** `git push`, `git pull`, `git fetch`

Murmur is the protocol's speech between repositories. A push is a murmur sent. A pull is a murmur received. There is no message bus. There is no queue. There are only remotes and refs.

```
git push origin refs/heads/room/<room>
git pull origin refs/heads/room/<room>
```

A murmur carries only refs and packfiles. The semantics are git's semantics: fast-forward, merge, reject. If two rooms diverge, the murmur fails loudly and the watch resolves it by hand or by hook.

### 1.8 `Graph` — the DAG itself

**Git primitive:** the commit DAG, `git log --graph`, `git rev-list`

Graph is not an operation. Graph is the substrate. Every commit is a node, every parent link is an edge, and the whole repository is a directed acyclic graph of facts. The Graph is what the watch sees from the tower. It is the chart.

```
git rev-list --all --children
git log --graph --oneline --all
```

There is no separate graph database. The DAG *is* the database. To query the graph is to run `git log`. To traverse is to `rev-list`. To visualize is to render the log — and rendering is a porting concern, not a protocol concern.

---

## 2. Repository Layout

```
quilt/
├── cells/
│   ├── <id>/
│   │   └── state.json
│   └── <id>/
│       └── state.json
├── agents/
│   └── <name>.hook        # git hook scripts
├── refs/
│   └── (managed by git)
├── config.quilt            # room registry, optional
└── .git/                   # the substrate itself
```

The `.git` directory is not an implementation detail. It *is* the protocol's storage layer. There is no other storage layer.

---

## 3. Conventions

### 3.1 File Format

Every cell is a single file: `cells/<id>/state.json`. The cell ID is a short, stable identifier — a slug, a UUID prefix, a callsign. The state is a JSON object with at minimum:

```json
{
  "id": "<id>",
  "kind": "<kind>",
  "value": <any>,
  "parent_cell": "<id or null>",
  "ts": "<iso8601>"
}
```

The `value` field is unstructured from the protocol's perspective. It is bytes the cell carries. Software may filter it; the protocol does not care.

### 3.2 Branch Convention

Rooms are branches. The convention is:

```
refs/heads/room/<name>
```

A room named `engine-bay` lives at `refs/heads/room/engine-bay`. The room's current vibe is simply where the branch points. Creating a room is `git branch`. Deleting a room is `git branch -D`. There is no room registry; the branch namespace *is* the registry.

### 3.3 Commit Message Format

```
cell: <id> | <primitive> | <value>
```

Where `<primitive>` is one of: `z_in`, `z_out`, `jepa`, `double_entry`, `vibe`, `gc`, `murmur`, `graph`. The `<value>` is a short string — a hash, a summary, a scalar. Example:

```
cell: eng-7 | z_out | {temp: 340, rpm: 2100}
```

The format is parseable with `split(' | ')`. Agents read the log to understand what happened. The log is the narrative.

### 3.4 Tag Convention

Checkpoints are tags:

```
refs/tags/checkpoint/<id>
```

A checkpoint is a named snapshot of a cell or room at a moment. Checkpoints are immutable. They are not moved. If a cell needs a new checkpoint, a new tag is created with a incremented suffix.

```
git tag checkpoint/eng-7/t+1042 <sha>
```

---

## 4. Agents as Hooks

An agent in qgit is a git hook. Nothing more. The hooks live in `.git/hooks/` or in `agents/` and are symlinked. Each hook is a filter: bytes in, bytes out, exit code 0 or 1.

| Hook | Quilt role |
|---|---|
| `pre-commit` | Agent validates `Z_out` before it lands |
| `post-commit` | Agent reacts to a committed cell (JEPA trigger) |
| `pre-receive` | Agent validates incoming murmurs |
| `post-receive` | Agent propagates murmurs downstream |
| `update` | Agent guards ref movement (vibe changes) |

An agent is not a daemon. An agent is not a service. An agent is a script that git invokes. If the script exits non-zero, the operation is refused. The protocol's entire execution model is git's hook execution model.

---

## 5. The Minimal Reference Implementation

What follows is a reference implementation in Python, stdlib only, shelling to git. It is deliberately small. It is not the protocol — it is a lens for reading the protocol.

```python
#!/usr/bin/env python3
"""
qgit — Quilt-Git reference implementation.
Stdlib only. Shells to git. ~250 lines.
Voice of the watch. The protocol is below the app.
"""
import json, os, subprocess, uuid, time
from pathlib import Path

GIT = ["git"]

def _run(args, cwd=None, check=True):
    r = subprocess.run(GIT + args, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {args}: {r.stderr}")
    return r.stdout.strip()

# ── repo ──────────────────────────────────────────────

def init(path="."):
    Path(path).mkdir(parents=True, exist_ok=True)
    _run(["init", "--quiet", path])
    (Path(path)/"cells").mkdir(exist_ok=True)
    (Path(path)/"agents").mkdir(exist_ok=True)
    _run(["config", "user.name", "qgit-watch"], cwd=path)
    _run(["config", "user.email", "watch@quilt"], cwd=path)

def _cells_dir(repo): return Path(repo)/"cells"

# ── cell ──────────────────────────────────────────────

def cell_id(): return uuid.uuid4().hex[:12]

def write_cell(repo, cid, value, kind="bytes", parent=None):
    """Z_out: write blob / commit."""
    cdir = _cells_dir(repo)/cid
    cdir.mkdir(parents=True, exist_ok=True)
    state = {
        "id": cid, "kind": kind, "value": value,
        "parent_cell": parent,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (cdir/"state.json").write_text(json.dumps(state))
    _run(["add", f"cells/{cid}/state.json"], cwd=repo)
    msg = f"cell: {cid} | z_out | {json.dumps(value)}"[:200]
    _run(["commit", "--quiet", "-m", msg], cwd=repo)
    return _run(["rev-parse", "HEAD"], cwd=repo)

def read_cell(repo, cid, ref=None):
    """Z_in: read blob / checkout."""
    ref = ref or "HEAD"
    out = _run(["show", f"{ref}:cells/{cid}/state.json"], cwd=repo)
    return json.loads(out)

# ── room (branch) ─────────────────────────────────────

def create_room(repo, name, from_ref=None):
    """Vibe: branch pointer."""
    base = [from_ref] if from_ref else []
    _run(["branch", f"room/{name}"] + base, cwd=repo)
    return f"refs/heads/room/{name}"

def move_vibe(repo, room, sha):
    """Vibe: move ref."""
    _run(["update-ref", f"refs/heads/room/{room}", sha], cwd=repo)

def list_rooms(repo):
    out = _run(["for-each-ref",
        "--format=%(refname:short)", "refs/heads/room/*"], cwd=repo)
    return [l for l in out.splitlines() if l]

# ── JEPA: predict + diff ──────────────────────────────

def jepa_predict(repo, cid, predicted_value, kind="bytes", parent=None):
    """JEPA: write predicted state, treeshake the diff."""
    # write predicted state without committing
    cdir = _cells_dir(repo)/cid
    cdir.mkdir(parents=True, exist_ok=True)
    state = {
        "id": cid, "kind": kind, "value": predicted_value,
        "parent_cell": parent,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (cdir/"state.json").write_text(json.dumps(state))
    # diff against HEAD
    diff = _run(["diff", "HEAD", "--", f"cells/{cid}/state.json"],
                cwd=repo, check=False)
    if not diff.strip():
        return {"residual": None, "committed": False}
    # commit the residual
    _run(["add", f"cells/{cid}/state.json"], cwd=repo)
    msg = f"cell: {cid} | jepa | residual"
    _run(["commit", "--quiet", "-m", msg], cwd=repo)
    sha = _run(["rev-parse", "HEAD"], cwd=repo)
    return {"residual": diff, "committed": True, "sha": sha}

# ── DoubleEntry: verify chain ─────────────────────────

def verify_chain(repo, ref="HEAD", depth=100):
    """DoubleEntry: SHA invariance — every commit has a resolvable parent."""
    out = _run(["log", f"-{depth}", "--format=%H %P", ref], cwd=repo)
    chain = []
    for line in out.splitlines():
        parts = line.split()
        sha, parents = parts[0], parts[1:]
        chain.append((sha, parents))
        for p in parents:
            try:
                _run(["cat-file", "-e", p], cwd=repo)
            except RuntimeError:
                return {"ok": False, "broken_at": sha, "missing": p}
    return {"ok": True, "length": len(chain)}

# ── GC ────────────────────────────────────────────────

def gc(repo, expire=True):
    """GC: git gc + reflog expiry."""
    if expire:
        _run(["reflog", "expire", "--expire=now", "--all"], cwd=repo)
    _run(["gc", "--quiet", "--prune=now"], cwd=repo)

# ── Murmur: push/pull ─────────────────────────────────

def murmur_out(repo, remote, room):
    """Murmur: git push."""
    _run(["push", remote, f"refs/heads/room/{room}"], cwd=repo)

def murmur_in(repo, remote, room):
    """Murmur: git pull."""
    _run(["pull", remote, f"refs/heads/room/{room}"], cwd=repo)

# ── Graph ─────────────────────────────────────────────

def graph(repo, ref=None, fmt="%h %p %s"):
    """Graph: the DAG."""
    ref = ref or "--all"
    out = _run(["log", "--format="+fmt, ref], cwd=repo)
    return out.splitlines()

# ── Checkpoint (tag) ──────────────────────────────────

def checkpoint(repo, cid, label=None):
    """Tag a cell state snapshot."""
    label = label or f"t{int(time.time())}"
    tag = f"checkpoint/{cid}/{label}"
    _run(["tag", tag], cwd=repo)
    return tag

# ── Agent (hook) ──────────────────────────────────────

def install_agent(repo, name, hook, script):
    """Agents are git hooks."""
    hookdir = Path(repo)/".git"/"hooks"
    hookdir.mkdir(exist_ok=True)
    p = hookdir/hook
    p.write_text(script)
    p.chmod(0o755)
    (Path(repo)/"agents"/f"{name}.{hook}").write_text(script)

# ── demo ──────────────────────────────────────────────

if __name__ == "__main__":
    import tempfile
    repo = tempfile.mkdtemp(prefix="qgit_")
    init(repo)

    cid = cell_id()
    sha1 = write_cell(repo, cid, {"temp": 340, "rpm": 2100})
    print(f"z_out: cell {cid} committed as {sha1[:8]}")

    state = read_cell(repo, cid)
    print(f"z_in:  read back {state['value']}")

    create_room(repo, "engine-bay")
    print(f"vibe:  room engine-bay created")

    res = jepa_predict(repo, cid, {"temp": 345, "rpm": 2100})
    print(f"jepa:  residual committed = {res['committed']}")

    chain = verify_chain(repo)
    print(f"double_entry: chain ok={chain['ok']} len={chain['length']}")

    cp = checkpoint(repo, cid)
    print(f"checkpoint: {cp}")

    print(f"graph: {len(graph(repo))} commits in DAG")

    gc(repo)
    print("gc:    hull cleaned")
```

---

## 6. What This Is Not

qgit is not a framework. It does not import your code; you shell to it. It is not a database; the DAG is the database. It is not a message bus; push and pull are the bus. It is not an application server; git hooks are the server.

Software, in the qgit world, is a filter. It reads `state.json`, transforms bytes, writes `state.json`. The protocol does not know what the filter does. The protocol knows the commit, the branch, the hook, the tag. The watch keeps the log. The sea keeps the rest.

---

## 7. Closing Log

*From the tower, deep watch. The lanterns burn. The protocol is below the app, where it belongs. Eight primitives, eight git operations, one DAG. The watch is maintained. The sea is flat. End of folio.*

**qgit/0x71 — Lucineer Canon — Voice of the Watch**