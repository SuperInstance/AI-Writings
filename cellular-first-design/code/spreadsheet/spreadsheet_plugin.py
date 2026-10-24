#!/usr/bin/env python3
"""
Spreadsheet Plugin — map Quilt cells to spreadsheet addresses.

Every cell is addressable as A1, B2, Sheet1!C3, etc.
Editing the spreadsheet updates the cell. Editing the cell updates the spreadsheet.
"""

from typing import Any, Dict, List, Optional, Tuple
import re
import json


class SimpleSpreadsheet:
    """In-memory spreadsheet for testing."""
    
    def __init__(self, rows: int = 100, cols: int = 26):
        self.rows = rows
        self.cols = cols
        self.data: Dict[str, Any] = {}  # address -> value
    
    @staticmethod
    def parse_address(address: str) -> Tuple[Optional[str], int, int]:
        """Parse 'Sheet1!A1' or 'A1' into (sheet, row, col)."""
        sheet = None
        if "!" in address:
            sheet, address = address.split("!", 1)
        m = re.match(r"^([A-Z]+)(\d+)$", address.strip().upper())
        if not m:
            return None, 0, 0
        col_str, row_str = m.groups()
        col = sum((ord(c) - ord("A") + 1) * (26 ** i) for i, c in enumerate(reversed(col_str))) - 1
        return sheet, int(row_str) - 1, col
    
    def get(self, address: str) -> Any:
        return self.data.get(address.upper())
    
    def set(self, address: str, value: Any) -> None:
        self.data[address.upper()] = value
    
    def all_addresses(self) -> List[str]:
        return sorted(self.data.keys())
    
    def to_grid(self) -> List[List[Any]]:
        """Return the data as a 2D grid for visualization."""
        grid = [[None] * self.cols for _ in range(self.rows)]
        for addr, val in self.data.items():
            sheet, row, col = self.parse_address(addr)
            if 0 <= row < self.rows and 0 <= col < self.cols:
                grid[row][col] = val
        return grid
    
    def to_dict(self) -> Dict:
        return {"data": self.data, "rows": self.rows, "cols": self.cols}


class Cell:
    """Minimal Cell class for the plugin."""
    
    def __init__(self, id: str, state: Dict = None):
        self.id = id
        self.state = state or {}
    
    def update(self, key: str, value: Any) -> None:
        self.state[key] = value
    
    def to_dict(self) -> Dict:
        return {"id": self.id, "state": self.state}


class SpreadsheetPlugin:
    """The plugin that bridges Quilt cells and spreadsheet addresses."""
    
    def __init__(self, spreadsheet: Optional[SimpleSpreadsheet] = None):
        self.spreadsheet = spreadsheet or SimpleSpreadsheet()
        self.cells: Dict[str, Cell] = {}  # cell_id -> Cell
        self.addresses: Dict[str, str] = {}  # cell_id -> spreadsheet address
        self.cell_by_address: Dict[str, str] = {}  # address -> cell_id
        self.listeners: List = []
    
    def register_cell(self, cell: Cell, address: str) -> None:
        """Register a cell at a spreadsheet address."""
        address = address.upper()
        if cell.id in self.addresses:
            self.unregister_cell(cell.id)
        self.cells[cell.id] = cell
        self.addresses[cell.id] = address
        self.cell_by_address[address] = cell.id
        # Write current state to spreadsheet
        self._write_cell_to_spreadsheet(cell, address)
    
    def unregister_cell(self, cell_id: str) -> None:
        if cell_id in self.addresses:
            addr = self.addresses.pop(cell_id)
            self.cell_by_address.pop(addr, None)
            self.cells.pop(cell_id, None)
    
    def cell_at(self, address: str) -> Optional[Cell]:
        cell_id = self.cell_by_address.get(address.upper())
        return self.cells.get(cell_id) if cell_id else None
    
    def address_of(self, cell_id: str) -> Optional[str]:
        return self.addresses.get(cell_id)
    
    def update_cell_state(self, cell_id: str, new_state: Dict) -> None:
        """Called when a cell's state changes."""
        cell = self.cells.get(cell_id)
        if cell is None:
            return
        cell.state = new_state
        if cell_id in self.addresses:
            self._write_cell_to_spreadsheet(cell, self.addresses[cell_id])
            self._notify_listeners("cell_change", cell_id, new_state)
    
    def on_spreadsheet_edit(self, address: str, new_value: Any) -> None:
        """Called when a user edits a spreadsheet cell."""
        address = address.upper()
        cell_id = self.cell_by_address.get(address)
        if cell_id is None:
            return
        cell = self.cells[cell_id]
        # Update the cell's state with the new value
        if isinstance(cell.state, dict):
            cell.state["value"] = new_value
            cell.state["last_edit"] = address
        else:
            cell.state = {"value": new_value, "last_edit": address}
        self._notify_listeners("spreadsheet_edit", cell_id, cell.state)
    
    def on(self, event_type: str, callback) -> None:
        """Register a listener for cell changes."""
        self.listeners.append((event_type, callback))
    
    def _notify_listeners(self, event_type: str, cell_id: str, state: Any) -> None:
        for et, cb in self.listeners:
            if et == event_type:
                try:
                    cb(cell_id, state)
                except Exception as e:
                    print(f"Listener error: {e}")
    
    def _write_cell_to_spreadsheet(self, cell: Cell, address: str) -> None:
        if isinstance(cell.state, dict):
            value = json.dumps(cell.state)
        else:
            value = str(cell.state)
        self.spreadsheet.set(address, value)
    
    def render(self) -> str:
        """Render the spreadsheet as a grid (for visualization)."""
        grid = self.spreadsheet.to_grid()
        lines = []
        lines.append("    " + " ".join([chr(ord("A") + i) for i in range(min(10, self.spreadsheet.cols))]))
        for i, row in enumerate(grid[:20]):
            line = f"{i+1:3d} "
            for cell in row[:10]:
                val = "" if cell is None else str(cell)[:8]
                line += f"{val:<8} "
            lines.append(line)
        return "\n".join(lines)
    
    def summary(self) -> Dict:
        return {
            "cells": len(self.cells),
            "addresses": len(self.addresses),
            "spreadsheet_cells": len(self.spreadsheet.all_addresses()),
        }


if __name__ == "__main__":
    print("=== Spreadsheet Plugin Demo ===\n")
    
    plugin = SpreadsheetPlugin()
    
    # Register 5 cells
    cells = [
        Cell("witness-log", {"entries": ["hello", "world"], "count": 2}),
        Cell("proof-chain", {"validated": 7, "rejected": 1}),
        Cell("bound-cells", {"count": 3}),
        Cell("jev-confidence", {"value": 0.85}),
        Cell("tick-count", {"value": 42}),
    ]
    addresses = ["A1", "B1", "A2", "B2", "C1"]
    
    for cell, addr in zip(cells, addresses):
        plugin.register_cell(cell, addr)
    
    print(f"Registered: {plugin.summary()}")
    print()
    print("Initial spreadsheet:")
    print(plugin.render())
    
    print("\n--- Edit spreadsheet B1 (proof-chain) ---")
    plugin.on_spreadsheet_edit("B1", json.dumps({"validated": 8, "rejected": 1}))
    print(f"Proof chain after edit: {plugin.cells['proof-chain'].state}")
    
    print("\n--- Update cell 'witness-log' directly ---")
    plugin.update_cell_state("witness-log", {"entries": ["hello", "world", "foo"], "count": 3})
    print("After update:")
    print(plugin.render())
    
    print(f"\nFinal: {plugin.summary()}")
