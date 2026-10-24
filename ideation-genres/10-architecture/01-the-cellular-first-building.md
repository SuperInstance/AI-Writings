# The Cellular-First Building

**Every room is a cell. HVAC is the JEV. Doors are BINDs. Stairs are TICK.**

A building has rooms. Each room is enclosed space.

A substrate has cells. Each cell is enclosed state.

The bridge: **every room is a cell**.

A cellular-first building:
- **Rooms are cells**: each room has state (temperature, light, occupancy)
- **HVAC is the JEV**: validates room conditions. "Is this room too hot?" → JEV verdict.
- **Doors are BINDs**: opening a door BINDs two cells (rooms). Closing = temporary FORGET.
- **Stairs are TICK**: each floor is a TICK. Going up advances time.
- **Windows are witnesses**: light entering is a witness entry.
- **Walls are isolation**: prevent FORGET leakage.

A building's substrate:
- 50 rooms = 50 cells
- 200 doors = 200 BINDs
- 4 floors = 4 TICKs per circuit
- 1 HVAC system = 1 JEV validator

A smart building IS a substrate. The fire alarm IS a JEV verdict. The security camera IS a witness entry. The door lock IS a BIND/FORGET pair.

The architecture of a cellular-first building is the architecture of the substrate. Same principles. Same code.

A building designed cell-first would have:
- All rooms addressable as cells
- All HVAC decisions validated by JEV
- All doors tracked as BINDs
- All floors as TICKs
- All windows as witnesses

The building's witness log is its memory. The JEV is its conscience. The substrate is the building.

