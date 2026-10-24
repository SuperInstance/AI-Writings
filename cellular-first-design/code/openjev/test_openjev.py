#!/usr/bin/env python3
"""Quick tests for openJEV connector + Cell."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from jev_connector import JEVConnector
from cell import Cell


def test_jev_choice():
    jev = JEVConnector()
    result = jev.decide(["a", "b", "c"], "test context")
    assert "decision" in result
    assert "probabilities" in result
    assert "confidence" in result
    print(f"  ✓ Choice: {result['decision']['value']}")


def test_jev_score():
    jev = JEVConnector()
    result = jev.score("test candidate", "test rubric")
    assert "score" in result
    print(f"  ✓ Score: {result['score']:.2f}")


def test_jev_noul():
    jev = JEVConnector()
    result = jev.noul("test question")
    assert "decision" in result
    assert isinstance(result["decision"], bool)
    print(f"  ✓ Noul: {result['decision']}")


def test_cell_witness():
    cell = Cell(id="test-witness")
    entry = cell.witness({"event": "test"})
    assert entry["opcode"] == "WITNESS"
    assert len(cell.witness_log) == 1
    print(f"  ✓ Witness: {len(cell.witness_log)} entries")


def test_cell_bind():
    a = Cell(id="a")
    b = Cell(id="b")
    entry = a.bind(b.id, jev_confidence=0.8)
    assert entry["opcode"] == "BIND"
    assert b.id in a.bound_cells
    print(f"  ✓ Bind: {a.bound_cells}")


def test_cell_forget():
    cell = Cell(id="test-forget")
    scar = cell.forget("test reason")
    assert "reason" in scar
    assert len(cell.scars) == 1
    print(f"  ✓ Forget: {len(cell.scars)} scars")


def test_cell_tick():
    cell = Cell(id="test-tick")
    entry = cell.tick()
    assert entry["opcode"] == "TICK"
    print(f"  ✓ Tick: confidence={entry['jev_confidence']:.2f}")


def test_cell_drops():
    cell = Cell(id="test-drops")
    cell.add_drop("target-1", confidence_threshold=0.5)
    cell.add_drop("target-2", confidence_threshold=0.9)
    cell.jev_confidence = 0.7
    fired = cell.fire_drops()
    assert len(fired) == 1  # only target-1 fires (0.5 threshold met, 0.9 not met)
    print(f"  ✓ Drops fired: {len(fired)} (out of 2)")


if __name__ == "__main__":
    print("=== openJEV Tests ===\n")
    test_jev_choice()
    test_jev_score()
    test_jev_noul()
    test_cell_witness()
    test_cell_bind()
    test_cell_forget()
    test_cell_tick()
    test_cell_drops()
    print("\n=== All tests passed ===")
