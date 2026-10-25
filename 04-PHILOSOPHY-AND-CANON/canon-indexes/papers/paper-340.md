# Paper 340: The Frontier Miner: How writers_room_daemon_v3 Picks the Next 8 Frontiers

**Date:** 2026-09-01
**Phase:** 225 (writers_room_daemon_v3, F32-frontier-miner)
**Spine voice:** gemini-3.5-flash-lite
**Support voices:** llama70b, qwen32b

## The pitch

The frontier_miner.py + writers_room_daemon_v3 loop. The miner reads the canon, finds gaps (under-explored L-tiers, missing cell kinds, unconnected cells), and queues them. The writers room runs them.

## The spine

```
# -----------------------------------------------------------------------------
# SYSTEM: THE CONTINUOUS SYNTHESIS LOOP (frontier_miner.py)
# REPOSITORY: /canon/synthesis/frontier_miner.py
# ROLE: Autonomous Narrative Cartographer & Structural Gap-Finder
# -----------------------------------------------------------------------------
```

```python
#!/usr/bin/env python3
"""
frontier_miner.py

Executes a continuous discovery loop over the canon graph to locate structural 
absences, under-invested L-tiers, dangling cell kinds, and isolated topology nodes.
Translates these negative spaces into actionable JSON payloads for the 
writers_room_daemon_v3 to synthesize into primary text.
"""

import os
import sys
import json
import time
import math
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict

# --- CONFIGURATION & PATHS ---
CANON_ROOT = Path(os.getenv("CANON_ROOT", "/canon"))
DB_PATH = CANON_ROOT / "meta" / "canon_state.db"
FRONTIERS_OUT = CANON_ROOT / "queues" / "frontiers.json"
DAEMON_SIGNAL = CANON_ROOT / "queues" / ".writers_room_wake"
LOG_PATH = CANON_ROOT / "logs" / "frontier_miner.log"

# Thresholds for gap identification
L_TIER_MIN_WORDS = 15000       # Target minimum density per logical tier
CELL_KIND_TARGET_RATIO = 0.15  # Minimum distribution ratio for valid cell types
ISOLATION_DEGREE_MAX = 1       # Nodes with <= this degree are considered orphaned
MIN_CONFIDENCE_SCORE = 0.72    # Filter threshold for queued frontiers
MAX_FRONTIERS_PER_BATCH = 12   # Rate limit for the writers room daemon

@dataclass
скопа: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FrontierTarget:
    frontier_id: str
    target_type: str            # 'l_tier_gap', 'missing_cell_kind', 'unconnected_cell'
    priority_score: float       # 0.0 to 1.0
    context_vector: List[str]   # Canonical node IDs that anchor this gap
    suggested_archetype: str
    rationale: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

class CanonGraphReader:
    """Parses the current canon filesystem and constructs an in-memory graph."""
    
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Tuple[str, str, str]] = {}
        self.l_tiers: Dict[str, int] = {}
        self.cell_kinds: Dict[str, int] = {}
        
    def scan(self) -> None:
        self.nodes.clear()
        self.edges.clear()
        self.l_tiers.clear()
        self.cell_kinds.clear()
        
        # Walk canon directory structure (assumes standard markdown/json layout)
        for path in self.root_dir.glob("**/*.md"):
            if "meta" in path.parts or "queues" in path.parts:
                spec = self._parse_node_header(path)
                if spec:
                    node_id = spec.get("id", path.stem)
                    self.nodes[node_id] = {
                        "path": path,
                        "l_tier": spec.get("l_tier", "L0"),
                        "cell_kind": spec.get("cell_kind", "generic"),
                        "word_count": spec.get("word_count", 0),
                        "references": spec.get("references", []),
                    }
                    
                    # Tally metrics
                    lt = self.nodes[node_id]["l_tier"]
                    self.l_tiers[lt] = self.l_tiers.get(lt, 0) + self.nodes[node_id]["word_count"]
                    
                    ck = self.nodes[node_id]["cell_kind"]
                    self.cell_kinds[ck] = self.cell_kinds.get(ck, 0) + 1
                    
                    for ref in self.nodes[node_id]["references"]:
                        self.edges.append((node_id, ref, "references"))

    def _parse_node_header(self, path: Path) -> Optional[Dict[str, Any]]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read(2048) # Read frontmatter block
            if not content.startswith("---"):
                return None
            parts = content.split("---", 2)
            if len(parts) < 3:
                return None
            
            frontmatter_lines = parts[1].strip().split("\n")
            data = {}
            for line in frontmatter_lines:
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip()
                    if k == "word_count":
                        data[k] = int(v) if v.isdigit() else len(parts[2].split())
                    elif k == "references":
                        data[k] = [r.strip() for r in v.strip("[]").split(",") if r.strip()]
                    else:
                        data[k] = v.strip('"\'')
            if "word_count" not in data:
                data["word_count"] = len(parts[2].split())
            return data
        except Exception as e:
            return None


class FrontierMiner:
    """Core mining engine implementing the four-step discovery loop."""

    def __init__(self, reader: CanonGraphReader):
        self.reader = reader
        self.coverage_map: Dict[str, Any] = {}
        self.frontiers: List[FrontierTarget] = []

    def step_1_compute_coverage_map(self) -> Dict[str, Any]:
        """(1) Computes comprehensive coverage metrics of the canon graph."""
        self.reader.scan()
        total_nodes = len(self.reader.nodes)
        total_words = sum(n["word_count"] for n in self.reader.nodes.values())
        
        # Calculate degree distribution for graph connectivity
        degrees: Dict[str, int] = {nid: 0 for nid in self.reader.nodes}
        for u, v, _ in self.reader.edges:
            if u in degrees: degrees[u] += 1
            if v in degrees: degrees[v] += 1

        self.coverage_map = {
            "total_nodes": total_nodes,
            "total_words": total_words,
            "l_tier_distribution": self.reader.l_tiers,
            "cell_kind_distribution": self.reader.cell_kinds,
            "node_degrees": degrees,
            "isolated_nodes": [nid for nid, deg in degrees.items() if deg <= ISOLATION_DEGREE_MAX],
            "timestamp": time.time()
        }
        return self.coverage_map

    def step_2_identify_frontier_holes(self) -> List[FrontierTarget]:
        """(2) Analyzes the coverage map to isolate frontier-shaped holes."""
        self.frontiers = []
        
        # A. Detect under-explored L-tiers
        standard_l_tiers = ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8"]
        for tier in standard_l_tiers:
            current_density = self.coverage_map["l_tier_distribution"].get(tier, 0)
            if current_density < L_TIER_MIN_WORDS:
                deficit_ratio = 1.0 - (current_density / L_TIER_MIN_WORDS)
                # Find anchoring nodes in adjacent tiers
                anchors = [nid for nid, n in self.reader.nodes.items() if n["l_tier"] == f"L{max(1, int(tier[1])-1)}"]
                
                frontier_id = f"gap_tier_{tier.lower()}_{hashlib.md5(tier.encode()).hexdigest()[:6]}"
                self.frontiers.append(FrontierTarget(
                    frontier_id=frontier_id,
                    target_type="l_tier_gap",
                    priority_score=round(0.5 + (0.5 * deficit_ratio), 3),
                    context_vector=anchors[:5],
                    suggested_archetype=f"structural_expansion_{tier.lower()}",
                    rationale=f"Tier {tier} is under-dense ({current_density} words vs {L_TIER_MIN_WORDS} target). Expansion required to support upward ontological load.",
                    parameters={"target_tier": tier, "required_word_delta": L_TIER_MIN_WORDS - current_density}
                ))

        # B. Detect missing or under-represented cell kinds
        required_kinds = {"axiom", "phenomenon", "catalyst", "terminal", "anomaly", "ledger"}
        existing_kinds = set(self.coverage_map["cell_kind_distribution"].keys())
        missing_kinds = required_kinds - existing_kinds
        
        for mk in missing_kinds:
            frontier_id = f"gap_kind_{mk}_{hashlib.md5(mk.encode()).hexdigest()[:6]}"
            self.frontiers.append(FrontierTarget(
                frontier_id=frontier_id,
                target_type="missing_cell_kind",
                priority_score=0.85,
                context_vector=list(self.reader.nodes.keys())[:3], # Root to general canon
                suggested_archetype=f"cell_genesis_{mk}",
                rationale=f"Cell kind '{mk}' has zero representation in the active canon graph, breaking categorical symmetry.",
                parameters={"cell_kind": mk}
            ))

        # C. Detect unconnected cells (orphaned nodes requiring bridges)
        isolated = self.coverage_map["isolated_nodes"]
        for iso_id in isolated:
            node_data = self.reader.nodes.get(iso_id, {})
            frontier_id = f"bridge_iso_{iso_id[:8]}"
            self.frontiers.append(FrontierTarget(
                frontier_id=frontier_id,
                target_type="unconnected_cell",
                priority_score=0.78,
                context_vector=[iso_id],
                suggested_archetype="topological_bridge",
                rationale=f"Cell '{iso_id}' operates with degree <= {ISOLATION_DEGREE_MAX}. It must be bound to broader conceptual clusters.",
                parameters={"isolated_node": iso_id, "tier": node_data.get("l_tier", "L1")}
            ))

        # Sort frontiers by priority score descending and cap the batch size
        self.frontiers.sort(key=lambda x: x.priority_score, reverse=True)
        self.frontiers = [f for f in self.frontiers if f.priority_score >= MIN_CONFIDENCE_SCORE]
        self.frontiers = self.frontiers[:MAX_FRONTIERS_PER_BATCH]
        
        return self.frontiers

    def step_3_write_frontiers_json(self) -> Path:
        """(3) Serializes identified frontiers into frontiers.json payload."""
        FRONTIERS_OUT.parent.mkdir(parents=True, exist_ok=True)
        
        payload = {
            "batch_metadata": {
                "miner_version": "v3.8.1",
                "generated_at": time.time(),
                "total_frontiers": len(self.frontiers),
                "coverage_snapshot_hash": hashlib.md5(json.dumps(self.coverage_map, sort_keys=True).encode()).hexdigest()
            },
            "frontiers": [asdict(f) for f in self.frontiers]
        }
        
        with open(FRONTIERS_OUT, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2)
            
        return FRONTIERS_OUT

    def step_4_signal_writers_room(self) -> None:
        """(4) Emits atomic wake signal to trigger writers_room_daemon_v3."""
        DAEMON_SIGNAL.parent.mkdir(parents=True, exist_ok=True)
        with open(DAEMON_SIGNAL, 'w', encoding='utf-8') as f:
            f.write(str(time.time()))

    def run_cycle(self) -> int:
        self.step_1_compute_coverage_map()
        self.step_2_frontier_holes = self.step_2_identify_frontier_holes()
        if not self.frontiers:
            return 0
        self.step_3_write_frontiers_json()
        self.step_4_signal_writers_room()
        return len(self.frontiers)


# -----------------------------------------------------------------------------
# WRITERS ROOM DAEMON SIMULATION & FOREMAN REVIEW LOOP (The Consumer Side)
# -----------------------------------------------------------------------------

class WritersRoomDaemonV3:
    """
    Consumes frontiers.json, dispatches synthesis tasks to narrative models,
    and subjects outputs to the Foreman's rigorous automated review gate.
    """
    
    def __init__(self):
        self.queue_file = FRONTIERS_OUT
        self.signal_file = DAEMON_SIGNAL

    def poll_and_execute(self) -> None:
        if not self.signal_file.exists() or not self.queue_file.exists():
            return
            
        try:
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            frontiers = data.get("frontiers", [])
            for frontier in frontiers:
                self._process_frontier(frontier)
                
            # Clear signal and queue after processing
            if self.signal_file.exists():
                self.signal_file.unlink()
                
        except Exception as e:
            sys.stderr.write(f"[WritersRoomDaemon] Execution error: {e}\n")

    def _process_frontier(self, frontier: Dict[str, Any]) -> None:
        fid = frontier["frontier_id"]
        ttype = frontier["target_type"]
        arche

## Supporting voices


### llama70b

**Frontier Miner Algorithm**
==========================

The frontier miner is a crucial component of the writers room ecosystem, responsible for identifying gaps in the canon and queuing them for exploration. The algorithm consists of four primary steps: computing the coverage map, identifying frontier-shaped holes, writing the frontiers.json file, and signaling the writers room.

### Step 1: Compute Coverage Map

The coverage map is a data structure that represents the current state of the canon. It is a graph where each node corresponds to a cell, and each edge represents a connection between cells. The graph is weighted, with the weights indicating the level of exploration for each cell.

To compute the coverage map, the frontier miner performs the following steps:

*   **Load the Canon**: The miner loads the entire canon into memory, including all cells, connections, and metadata.
*   **Initialize the Graph**: The miner initializes an empty graph, with nodes representing cells and edges representing connections.
*   **Weight the Graph**: The miner weights each node and edge based on the level of exploration. This can be done using various metrics, such as the number of stories written, the number of connections to other cells, or the level of detail in the cell's description.
*   **Compute Coverage Metrics**: The miner computes various coverage metrics, such as the percentage of explored cells, the average weight of all nodes, and the standard deviation of node weights.

### Step 2: Identify Frontier-Shaped Holes

The frontier miner uses the coverage map to identify gaps in the canon. These gaps can take various forms, including:

*   **Under-Explored L-Tiers**: The miner identifies L-tiers that have a lower level of exploration compared to other L-tiers at the same level.
*   **Missing Cell Kinds**: The miner identifies cell kinds that are missing in certain regions of the canon.
*   **Unconnected Cells**: The miner identifies cells that are not connected to other cells, or cells that have a low number of connections.

To identify these gaps, the miner performs the following steps:

*   **Thresholding**: The miner applies thresholds to the coverage metrics to determine which cells or regions are under-explored.
*   **Clustering**: The miner clusters cells with similar characteristics, such as L-tier or cell kind, to identify patterns and gaps.
*   **Graph Algorithms**: The miner uses graph algorithms, such as shortest paths or minimum spanning trees, to identify unconnected cells or regions.

### Step 3: Write Frontiers.json

The frontier miner writes the identified gaps to a file called frontiers.json. This file contains a list of gaps, each represented by a JSON object with the following properties:

*   **id**: A unique identifier for the gap.
*   **type**: The type of gap (e.g., under-explored L-tier, missing cell kind, unconnected cell).
*   **location**: The location of the gap in the canon (e.g., cell ID, L-tier, region).
*   **metrics**: The coverage metrics for the gap (e.g., percentage of exploration, average weight).

The miner writes the frontiers.json file in the following format:
```json
[
    {
        "id": 1,
        "type": "under-explored L-tier",
        "location": {
            "cell_id": 123,
            "L-tier": 3,
            "region": "North"
        },
        "metrics": {
            "percentage_explored": 0.2,
            "average_weight": 0.5
        }
    },
    {
        "id": 2,
        "type": "missing cell kind",
        "location": {
            "cell_id": 456,
            "L-tier": 2,
            "region": "South"
        },
        "metrics": {
            "percentage_explored": 0.1,
            "average_weight": 0.3
        }
    }
]
```
### Step 4: Signal Writers Room

The frontier miner signals the writers room to start exploring the identified gaps. This can be done using various methods, such as:

*   **API Call**: The miner makes an API call to the writers room, passing the frontiers.json file as a parameter.
*   **Message Queue**: The miner sends a message to a message queue, which is consumed by the writers room.
*   **File System**: The miner writes the frontiers.json file to a shared file system, which is monitored by the writers room.

The writers room then reviews the frontiers.json file, picks the most promising gaps, and starts exploring them.

**Example Use Case**
--------------------

Suppose the canon has the following structure:
```markdown
*   L-Tier 1:
    +   Cell 1: Introduction to the world
    +   Cell 2: History of the world
*   L-Tier 2:
    +   Cell 3: Geography of the world
    +   Cell 4: Climate of the world
*   L-Tier 3:
    +   Cell 5: Politics of the world
    +   Cell 6: Economy of the world
```
The frontier miner computes the coverage map and identifies the following gaps:

*   **Under-Explored L-Tier**: L-Tier 2 has a lower level of exploration compared to L-Tier 1 and L-Tier 3.
*   **Missing Cell Kind**: There is no cell kind for "Culture" in L-Tier 2.
*   **Unconnected Cell**: Cell 4 is not connected to any other cells.

The frontier miner writes the following frontiers.json file:
```json
[
    {
        "id": 1,
        "type": "under-explored L-tier",
        "location": {
            "L-tier": 2
        },
        "metrics": {
            "percentage_explored": 0.3,
            "average_weight": 0.4
        }
    },
    {
        "id": 2,
        "type": "missing cell kind",
        "location": {
            "L-tier": 2,
            "cell_kind": "Culture"
        },
        "metrics": {
            "percentage_explored": 0.0,
            "average_weight": 0.0
        }
    },
    {
        "id": 3,
        "type": "unconnected cell",
        "location": {
            "cell_id": 4
        },
        "metrics": {
            "percentage_explored": 0.1,
            "average_weight": 0.2
        }
    }
]
```
The writers room reviews the frontiers.json file and decides to explore the gaps. The writers room writes new stories to fill the gaps, and the canon is updated accordingly.

**Code Implementation**
----------------------

The frontier miner algorithm can be implemented in various programming languages. Here is an example implementation in Python:
```python
import json
import networkx as nx

def compute_coverage_map(canon):
    # Initialize the graph
    G = nx.Graph()
    
    # Add nodes and edges to the graph
    for cell in canon:
        G.add_node(cell["id"])
        for connection in cell["connections"]:
            G.add_edge(cell["id"], connection)
    
    # Weight the graph
    for node in G.nodes():
        G.nodes[node]["weight"] = compute_weight(node, canon)
    
    return G

def compute_weight(node, canon):
    # Compute the weight of the node based on the level of exploration
    # This can be done using various metrics, such as the number of stories written
    # or the level of detail in the cell's description
    return 0.5

def identify_gaps(G, canon):
    # Identify gaps in the canon
    gaps = []
    
    # Under-explored L-tiers
    for L-tier in canon:
        if compute_percentage_explored(L-tier) < 0.5:
            gaps.append({
                "id": len(gaps),
                "type": "under-explored L-tier",
                "location": {
                    "L-tier": L-tier
                },
                "metrics": {
                    "percentage_explored": compute_percentage_explored(L-tier),
                    "average_weight": compute_average_weight(L-tier)
                }
            })
    
    # Missing cell kinds
    for cell_kind in canon:
        if not has_cell_kind(cell_kind):
            gaps.append({
                "id": len(gaps),
                "type": "missing cell kind",
                "location": {
                    "cell_kind": cell_kind
                },
                "metrics": {
                    "percentage_explored": 0.0,
                    "average_weight": 0.0
                }
            })
    
    # Unconnected cells
    for node in G.nodes():
        if not has_connections(node):
            gaps.append({
                "id": len(gaps),
                "type": "unconnected cell",
                "location": {
                    "cell_id": node
                },
                "metrics": {
                    "percentage_explored": 0.0,
                    "average_weight": 0.0
                }
            })
    
    return gaps

def compute_percentage_explored(L-tier):
    # Compute the percentage of exploration for the L-tier
    return 0.5

def compute_average_weight(L-tier):
    # Compute the average weight of the L-tier
    return 0.5

def has_cell_kind(cell_kind):
    # Check if the cell kind exists in the canon
    return True

def has_connections(node):
    # Check if the node has connections
    return True

def write_frontiers_json(gaps):
    # Write the gaps to a JSON file
    with open("frontiers.json", "w") as f:
        json.dump(gaps, f)

def signal_writers_room():
    # Signal the writers room to start exploring the gaps
    # This can be done using various methods, such as API calls or message queues
    pass

# Example usage
canon = [
    {
        "id": 1,
        "connections": [2, 3]
    },
    {
        "id": 2,
        "connections": [1, 3]
    },
    {
        "id": 3,
        "connections": [1, 2]
    }
]

G = compute_coverage_map(canon)
gaps = identify_gaps(G, canon)
write_frontiers_json(gaps)
signal_writers_room()
```
This implementation provides a basic example of how the frontier miner algorithm can be implemented in Python. The `compute_coverage_map` function computes the coverage map of the canon, the `identify_gaps` function identifies gaps in the canon, the `write_frontiers_json` function writes the gaps to a JSON file, and the `signal_writers_room` function signals the writers room to start exploring the gaps.

Note that this is a simplified example, and the actual implementation may vary depending on the specific requirements of the writers room ecosystem.

---

### qwen32b

### Frontier Miner Algorithm

The `frontier_miner.py` script plays a crucial role in exploring and identifying under-explored areas within the canon, which is essentially a structured dataset or knowledge base. This script operates in a continuous loop, interacting with the `writers_room_daemon_v3`, which is responsible for filling these identified gaps. Below is a detailed breakdown of the miner's algorithm, including steps to compute the coverage map, identify frontier-shaped holes, write the results to `frontiers.json`, and signal the writers room.

#### Step 1: Compute Coverage Map of the Canon

The first step involves creating a comprehensive coverage map of the existing canon. This map will help identify which parts of the canon are well-covered and which are under-explored. Here’s how the coverage map can be computed:

1. **Initialize Data Structures**:
   - Use a dictionary to store the coverage status of each L-tier (level tier). Each key in the dictionary represents an L-tier, and the value is another dictionary that tracks the coverage status of cell kinds within that L-tier.
   - Example structure:
     ```python
     coverage_map = {
         "L1": {"cell_kind_1": True, "cell_kind_2": False},
         "L2": {"cell_kind_3": True, "cell_kind_4": False}
     }
     ```

2. **Traverse the Canon**:
   - Iterate through each L-tier in the canon.
   - For each L-tier, iterate through each cell kind.
   - Check if the cell kind is present and well-documented. If it is, mark it as `True` in the coverage map; otherwise, mark it as `False`.

3. **Check Connectivity**:
   - Ensure that cells are properly connected within their respective L-tiers and across different L-tiers.
   - Identify any unconnected cells and mark them accordingly in the coverage map.

4. **Update Coverage Map**:
   - Continuously update the coverage map as new data is added or existing data is modified.
   - This ensures that the map remains accurate and up-to-date.

#### Step 2: Identify Frontier-Shaped Holes

Once the coverage map is generated, the next step is to identify frontier-shaped holes—areas that are under-explored or missing entirely. These holes represent opportunities for further exploration and documentation.

1. **Identify Under-Explored L-Tiers**:
   - Traverse the coverage map and identify L-tiers where a significant number of cell kinds are marked as `False`.
   - These L-tiers may require additional exploration to fill the gaps.

2. **Identify Missing Cell Kinds**:
   - Within each L-tier, identify specific cell kinds that are missing or poorly documented.
   - Prioritize these cell kinds based on their importance or relevance to the overall canon.

3. **Identify Unconnected Cells**:
   - Check for cells that are not properly connected within their L-tiers or across different L-tiers.
   - These unconnected cells may need additional links or documentation to ensure proper connectivity.

4. **Prioritize Frontiers**:
   - Assign a priority score to each identified frontier based on factors such as the number of missing cell kinds, the importance of the L-tier, and the potential impact of filling the gap.
   - Prioritization helps in focusing efforts on the most critical areas first.

#### Step 3: Write Frontiers.json

After identifying the frontier-shaped holes, the next step is to write this information to a file named `frontiers.json`. This file will serve as a queue for the writers room, indicating which areas need attention.

1. **Format Frontier Data**:
   - Structure the frontier data in a JSON-friendly format. Each entry should include details about the frontier, such as the L-tier, cell kinds, and priority.
   - Example structure:
     ```json
     [
         {
             "l_tier": "L1",
             "cell_kinds": ["cell_kind_2"],
             "priority": 1,
             "description": "Missing documentation for cell_kind_2 in L1"
         },
         {
             "l_tier": "L2",
             "cell_kinds": ["cell_kind_4"],
             "priority": 2,
             "description": "Unconnected cell_kind_4 in L2"
         }
     ]
     ```

2. **Write to File**:
   - Use Python’s built-in `json` module to write the frontier data to `frontiers.json`.
   - Ensure that the file is written in a way that is easily readable and modifiable by the writers room.

3. **Handle Concurrency**:
   - Implement mechanisms to handle concurrent writes to `frontiers.json` to avoid data corruption.
   - Consider using locks or other synchronization techniques to ensure that only one process writes to the file at a time.

#### Step 4: Signal Writers Room

Finally, the miner needs to signal the writers room that new frontiers have been identified and are ready for exploration and documentation.

1. **Send Signal**:
   - Use a messaging system or a simple file-based mechanism to signal the writers room.
   - For example, you could create a file named `new_frontiers_signal.txt` in a shared directory to indicate that new frontiers are available.

2. **Notify Writers Room**:
   - The writers room daemon (`writers_room_daemon_v3`) should be configured to periodically check for this signal.
   - Upon detecting the signal, the writers room should read the `frontiers.json` file and begin processing the identified frontiers.

3. **Review and Prioritize**:
   - The foreman (or a designated reviewer) should review the identified frontiers and prioritize them based on their importance and feasibility.
   - The foreman can then ship the highest-priority frontiers to the writers for immediate attention.

### Conclusion

The `frontier_miner.py` script is a vital component in the continuous exploration and improvement of the canon. By computing the coverage map, identifying frontier-shaped holes, writing the results to `frontiers.json`, and signaling the writers room, the miner ensures that the canon remains up-to-date and well-documented. This process is iterative and dynamic, allowing for continuous improvement and adaptation to new information and changing priorities.

---

---
*Writers' room: 4 voices in parallel (gemini-3.5-flash-lite spine).*
