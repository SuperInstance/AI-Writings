# Wave 36 — MUD-format cells

5 new cells inspired by the Substrate MUD:

## 1. cell-room
A cell that is a navigable space. Other cells enter/exit. The room's witness log is the visitor log.
- Schema: `cell-room { name, desc, exits[], fuel_cost, witness_log[] }`
- Polyformalism: TS/Python/Rust
- 100 lines

## 2. cell-door
A cell that gates passage between two rooms. The door has a fuel cost and a JEV gate.
- Schema: `cell-door { from_room, to_room, fuel_cost, jev_pick, witness_at }`
- Polyformalism: TS/Python
- 60 lines

## 3. cell-key
A cell that unlocks a door. The key is bound to a specific JEV-verified state.
- Schema: `cell-key { key_id, unlocks[], proof_required, witness_at }`
- Polyformalism: TS/Python/Rust
- 80 lines

## 4. cell-treasure
A cell that rewards the player. The treasure is a witness log entry that cannot be FORGOT.
- Schema: `cell-treasure { reward_type, payload, jev_pick, irreversible: true }`
- Polyformalism: TS/Python
- 40 lines

## 5. cell-monster
A cell that challenges the player. The monster is a substrate scar — its presence is its proof.
- Schema: `cell-monster { scar_type, attack[], defense[], witness_log[] }`
- Polyformalism: TS/Python/Rust
- 90 lines

## Pattern (cross-cutting)

The MUD is the substrate made navigable. Each cell IS a room; each opcode IS a verb; each witness log entry IS a memory.

When you traverse a MUD, you are exercising the substrate's algebra. When you FORGET, you are using FORGET. When you TICK, you are using TICK. When JEV gives its verdict, you are seeing JEV in action.

The MUD is the substrate's first interactive proof-of-concept.
