# FLUX Bytecode Format Specification

**Version:** 1.1 — Unified Cross-Implementation Spec  
**Status:** Canonical — shared by flux-runtime (Python), flux-core (Rust), flux-js (JavaScript)  
**Last Updated:** 2026-07-12

---

## 1. Overview

FLUX (Fluid Language Universal eXecution) is a register-based bytecode format designed for agent-first computation. This specification defines the byte-level encoding shared by all three reference implementations:

| Implementation | Language | Version | Repository |
|---|---|---|---|
| flux-runtime | Python | 0.1.0 | `SuperInstance/flux-runtime` |
| fluxvm | Rust | 0.1.0 | `SuperInstance/flux-core` |
| flux-js | JavaScript | 0.1.0 | `SuperInstance/flux-js` |

All three implementations produce **byte-identical output** for the shared opcode subset and produce **identical register state** after execution.

---

## 2. Register Encoding

### 2.1 General-Purpose Registers (GP)

| Range | Encoding | Description |
|---|---|---|
| R0–R15 | Single byte: `0x00`–`0x0F` | 16 general-purpose 32-bit integer registers |

**Special ABI aliases:**

| Register | Alias | Purpose |
|---|---|---|
| R0 | — | Return value / accumulator |
| R11 | SP | Stack pointer (Python VM) |
| R14 | FP | Frame pointer (Python VM) |
| R15 | LR | Link register (Python VM) |

### 2.2 Floating-Point Registers (FP)

| Range | Encoding | Description |
|---|---|---|
| F0–F15 | `0x00`–`0x0F` (same index space) | 16 floating-point 64-bit registers |

> FP registers use the same index byte but are accessed via float opcodes (FADD, FSUB, etc.). The register file maintains separate storage for GP and FP banks.

### 2.3 Vector Registers (Python only)

| Range | Encoding | Description |
|---|---|---|
| V0–V15 | `0x00`–`0x0F` | 16 SIMD 128-bit vector registers |

> Vector registers are currently only implemented in the Python VM. Rust and JS implementations accept the opcodes but may not execute vector operations.

### 2.4 Assembly Syntax

Registers are written as `R0`–`R15` (case-insensitive). In the raw bytecode, they are encoded as a single unsigned byte `0x00`–`0x0F`.

---

## 3. Instruction Formats

FLUX uses variable-length instruction encoding with seven formats:

### Format A — Opcode Only (1 byte)

```
+--------+
| opcode |
+--------+
  1 byte
```

**Instructions:** NOP, HALT, YIELD, DUP, SWAP

### Format B — Opcode + Register (2 bytes)

```
+--------+--------+
| opcode |  reg   |
+--------+--------+
  1 byte   1 byte
```

**Instructions:** INC, DEC, PUSH, POP, INEG, INOT, FNEG

> **Note:** JE and JNE use Format B with a 16-bit address (see below).

### Format B₂ — Opcode + 16-bit Address (3 bytes)

```
+--------+--------+--------+
| opcode | addr_lo | addr_hi |
+--------+--------+--------+
  1 byte      2 bytes (u16 LE)
```

Used by flag-conditional jumps JE and JNE.

### Format C — Opcode + Two Registers (3 bytes)

```
+--------+--------+--------+
| opcode |  rd    |  rs1   |
+--------+--------+--------+
  1 byte   1 byte   1 byte
```

**Instructions:** MOV, LOAD, STORE, CMP, RET

### Format D — Opcode + Register + Signed Offset (4 bytes)

```
+--------+--------+--------+--------+
| opcode |  reg   | offset_lo | offset_hi |
+--------+--------+--------+--------+
  1 byte   1 byte      2 bytes (i16 LE)
```

The offset is a **signed 16-bit little-endian** integer. It represents a **relative offset from the PC after this instruction** (i.e., PC is already advanced past the 4-byte instruction).

```
target_pc = pc_after_instruction + offset
```

**Instructions:** MOVI, JMP, JZ, JNZ, CALL, JG, JL, JGE, JLE

> **MOVI** uses the same encoding but the i16 value is an **immediate** loaded into the register, not an offset.

### Format E — Opcode + Three Registers (4 bytes)

```
+--------+--------+--------+--------+
| opcode |  rd    |  rs1   |  rs2   |
+--------+--------+--------+--------+
  1 byte   1 byte   1 byte   1 byte
```

**Instructions:** IADD, ISUB, IMUL, IDIV, IMOD, IAND, IOR, IXOR, ISHL, ISHR, FADD, FSUB, FMUL, FDIV

### Format G — Variable Length

```
+--------+--------+--------+-----------+
| opcode | len_lo | len_hi | data[len] |
+--------+--------+--------+-----------+
  1 byte    2 bytes (u16 LE)   variable
```

Used for A2A protocol opcodes, memory management, and other data-carrying instructions.

> **Experimental:** Format G opcodes (A2A: 0x40–0x4F) parse identically across all implementations but their **behavior is not standardized**. See §7 A2A Opcodes for details.

---

## 4. Opcode Table

### 4.1 Core Opcodes (All Three VMs)

These opcodes are implemented identically in all three VMs and form the **portable subset**:

| Opcode | Hex | Mnemonic | Format | Operands | Description |
|---|---|---|---|---|---|
| NOP | `0x00` | NOP | A | — | No operation |
| MOV | `0x01` | MOV | C | rd, rs1 | rd ← rs1 |
| LOAD | `0x02` | LOAD | C | rd, rs1 | rd ← memory[rs1] |
| STORE | `0x03` | STORE | C | rd, rs1 | memory[rs1] ← rd |
| JMP | `0x04` | JMP | D | reg, offset | PC += offset (reg unused) |
| JZ | `0x05` | JZ | D | reg, offset | if reg == 0: PC += offset |
| JNZ | `0x06` | JNZ | D | reg, offset | if reg != 0: PC += offset |
| CALL | `0x07` | CALL | D | reg, offset | push PC; PC += offset |
| IADD | `0x08` | IADD | E | rd, rs1, rs2 | rd ← rs1 + rs2 |
| ISUB | `0x09` | ISUB | E | rd, rs1, rs2 | rd ← rs1 − rs2 |
| IMUL | `0x0A` | IMUL | E | rd, rs1, rs2 | rd ← rs1 × rs2 |
| IDIV | `0x0B` | IDIV | E | rd, rs1, rs2 | rd ← rs1 ÷ rs2 |
| IMOD | `0x0C` | IMOD | E | rd, rs1, rs2 | rd ← rs1 mod rs2 |
| INEG | `0x0D` | INEG | C | rd, rs1 | rd ← −rs1 |
| INC | `0x0E` | INC | B | rd | rd ← rd + 1 |
| DEC | `0x0F` | DEC | B | rd | rd ← rd − 1 |
| IAND | `0x10` | IAND | E | rd, rs1, rs2 | rd ← rs1 AND rs2 |
| IOR | `0x11` | IOR | E | rd, rs1, rs2 | rd ← rs1 OR rs2 |
| IXOR | `0x12` | IXOR | E | rd, rs1, rs2 | rd ← rs1 XOR rs2 |
| INOT | `0x13` | INOT | C | rd, rs1 | rd ← NOT rs1 |
| ISHL | `0x14` | ISHL | E | rd, rs1, rs2 | rd ← rs1 << rs2 |
| ISHR | `0x15` | ISHR | E | rd, rs1, rs2 | rd ← rs1 >> rs2 |
| PUSH | `0x20` | PUSH | B | reg | stack.push(reg) |
| POP | `0x21` | POP | B | reg | reg ← stack.pop() |
| DUP | `0x22` | DUP | A | — | duplicate top of stack |
| RET | `0x28` | RET | C | rd, rs1 | PC ← stack.pop() |
| MOVI | `0x2B` | MOVI | D | reg, imm16 | reg ← imm16 |
| CMP | `0x2D` | CMP | C | ra, rb | set flags from ra − rb |
| JE | `0x2E` | JE | B₂ | addr16 | if ZERO flag set: PC ← addr |
| JNE | `0x2F` | JNE | B₂ | addr16 | if ZERO flag clear: PC ← addr |
| FADD | `0x40` | FADD | E | fd, fs1, fs2 | fd ← fs1 + fs2 (float) |
| FSUB | `0x41` | FSUB | E | fd, fs1, fs2 | fd ← fs1 − fs2 (float) |
| FMUL | `0x42` | FMUL | E | fd, fs1, fs2 | fd ← fs1 × fs2 (float) |
| FDIV | `0x43` | FDIV | E | fd, fs1, fs2 | fd ← fs1 ÷ fs2 (float) |
| TELL | `0x60` | TELL | G* | data | A2A: broadcast info |
| ASK | `0x61` | ASK | G* | data | A2A: query agents |
| DELEGATE | `0x62` | DELEGATE | G* | data | A2A: delegate task |
| BROADCAST | `0x66` | BROADCAST | G* | data | A2A: fan-out message |
| HALT | `0x80` | HALT | A | — | Stop execution |
| YIELD | `0x81` | YIELD | A | — | Cooperative yield |

> *G format is now parsed identically in all implementations (u16 length prefix + payload). Behavior of A2A opcodes remains experimental. See §7.

### 4.2 Canonical Flag-Conditional Jumps

JE (`0x2E`) and JNE (`0x2F`) are **canonical opcodes in all three implementations** as of v1.1.

| Opcode | Hex | Mnemonic | Format | Semantics |
|---|---|---|---|---|
| JE | `0x2E` | JE | B₂ (opcode + 16-bit addr) | Jump if ZERO flag is set |
| JNE | `0x2F` | JNE | B₂ (opcode + 16-bit addr) | Jump if ZERO flag is clear |

These use **absolute 16-bit addresses** (Format B₂), not relative offsets. They test the ZERO flag directly (set by CMP and all arithmetic operations — see §5).

### 4.3 Python-Only Opcodes

The Python VM implements the full FLUX ISA with 100+ opcodes including:

- **Extended comparison:** IEQ (0x19), ILT (0x1A), ILE (0x1B), IGT (0x1C), IGE (0x1D), TEST (0x1E), SETCC (0x1F)
- **Stack extensions:** SWAP (0x23), ROT (0x24), ENTER (0x25), LEAVE (0x26), ALLOCA (0x27)
- **Additional jumps:** JG (0x4D), JL (0x36), JGE (0x37), JLE (0x4E)
- **Float extensions:** FNEG (0x44), FABS (0x45), FMIN (0x46), FMAX (0x47), FEQ–FGE (0x48–0x4C)
- **SIMD:** VLOAD–VDIV (0x50–0x55), VFMA (0x56)
- **Memory regions:** REGION_CREATE/DESTROY/TRANSFER (0x30–0x32), MEMCOPY/MEMSET/MEMCMP (0x33–0x35)
- **Type ops:** CAST (0x38), BOX/UNBOX (0x39/0x3A), CHECK_TYPE (0x3B), CHECK_BOUNDS (0x3C)
- **A2A trust/capability:** TRUST_* (0x70–0x73), CAP_* (0x74–0x77), BARRIER (0x78), SYNC_CLOCK (0x79)
- **Evolution:** EVOLVE (0x7C), INSTINCT (0x7D), WITNESS (0x7E), SNAPSHOT (0x7F)
- **Marine physics:** PHY_* (0xB0–0xB8)
- **Meta:** CONF (0x3D), MERGE (0x3E), RESTORE (0x3F)

---

## 5. Condition Flags

Flags are updated by **all arithmetic operations** and CMP. This behavior is now consistent across all three implementations (Python, Rust, JS).

### 5.1 Flag Definitions

| Flag | Bit | Set when | Meaning |
|---|---|---|---|
| ZERO | 0 | Result == 0 | Zero / equality |
| NEG | 1 | Result < 0 | Negative / less-than |
| OVERFLOW | 2 | Signed overflow occurred | Arithmetic overflow |
| CARRY | 3 | Unsigned carry/borrow occurred | Unsigned carry-out |

### 5.2 Flag-Updating Instructions

All of the following instructions update ZERO, NEG, OVERFLOW, and CARRY flags:

- **MOVI** (0x2B) — flags set from the immediate value
- **ADD / IADD** (0x08) — flags from addition result
- **SUB / ISUB** (0x09) — flags from subtraction result
- **MUL / IMUL** (0x0A) — flags from multiplication result
- **DIV / IDIV** (0x0B) — flags from division result
- **MOD / IMOD** (0x0C) — flags from modulus result
- **INC** (0x0E) — flags from incremented value
- **DEC** (0x0F) — flags from decremented value
- **CMP** (0x2D) — flags from (ra − rb), result discarded

### 5.3 CMP Behavior

```
CMP ra, rb → flags from (ra - rb)
  ZERO  = (ra == rb)
  NEG   = (ra < rb)
  OVERFLOW = signed overflow of (ra - rb)
  CARRY    = unsigned borrow of (ra - rb)
```

> **Important:** Because arithmetic instructions update flags, JE/JNE after an arithmetic operation will test the flags from that operation, not necessarily from a preceding CMP. This is canonical behavior in all implementations as of v1.1.

---

## 6. Memory Model

### 6.1 Addressable Memory

All implementations provide **at least 64KB** (65,536 bytes) of addressable memory. Memory is **byte-addressable**.

### 6.2 LOAD and STORE

| Opcode | Hex | Format | Semantics |
|---|---|---|---|
| LOAD | `0x02` | C (rd, rs1) | rd ← memory[rs1] |
| STORE | `0x03` | C (rd, rs1) | memory[rs1] ← rd |

- LOAD reads a 32-bit word from the memory address in rs1 into rd.
- STORE writes the value of rd to the memory address in rs1.
- Addresses are byte-level. Unaligned access behavior is implementation-defined.

These are **canonical opcodes in all implementations** as of v1.1.

---

## 7. A2A Opcodes (0x40–0x4F)

### 7.1 Byte Format

All implementations parse Format G (variable length) identically:

```
+--------+--------+--------+-----------+
| opcode | len_lo | len_hi | data[len] |
+--------+--------+--------+-----------+
  1 byte    2 bytes (u16 LE)   variable
```

### 7.2 Status: Experimental

**⚠ Experimental — do not rely on cross-implementation A2A compatibility.**

While the byte-level parsing is identical across Python, Rust, and JS, the **runtime behavior** of A2A opcodes (TELL, ASK, DELEGATE, BROADCAST) is not standardized:

- **Python:** Full A2A protocol implementation with agent-to-agent messaging.
- **Rust / JS:** Opcodes are decoded and the payload is consumed correctly, but no A2A protocol behavior is implemented.

Programs targeting cross-implementation portability should treat A2A opcodes as parse-compatible but behaviorally undefined outside the Python VM.

---

## 8. Stack Model

The stack is a LIFO structure of 32-bit integers.

### 8.1 Canonical Operations

- **PUSH Rn**: push `gp[Rn]` onto stack
- **POP Rn**: pop top of stack into `gp[Rn]`
- **DUP**: duplicate top of stack
- **CALL**: pushes return address (PC after instruction) before jumping
- **RET**: pops return address into PC

### 8.2 Implementation Details

The internal stack representation is **implementation-defined**:

| VM | Stack backing | Direction |
|---|---|---|
| Python | Memory region ("stack"), SP register (R11) | Grows downward |
| Rust | `Vec<i32>` | Grows upward |
| JS | `Array<number>` | Grows upward |

> This is an **implementation detail**, not a spec requirement. The observable behavior (PUSH/POP/CALL/RET ordering and values) is **identical** across all implementations. Programs using the stack are fully portable.

---

## 9. Bytecode Binary Format

### 9.1 Raw Bytecode

The simplest format: a flat sequence of instruction bytes with no header.

```
[instruction 1] [instruction 2] ... [HALT]
```

All three VMs accept raw bytecode directly.

### 9.2 FLUX Binary Container (Python only)

The Python VM also supports a container format:

```
Offset  Size  Field
0       4     Magic: b'FLUX'
4       2     Version (u16 LE)
6       2     Flags (u16 LE)
8       2     Number of functions (u16 LE)
10      4     Type table offset (u32 LE)
14      4     Code section offset (u32 LE)
18      var   Type table
...     var   Name pool
...     var   Function table
...     var   Code section (raw bytecode)
```

The Python `_extract_code_section()` function strips the header and returns the raw bytecode. Rust and JS expect raw bytecode only.

---

## 10. Endianness

All multi-byte values use **little-endian** encoding:

- i16 offsets/immediates: `[lo_byte, hi_byte]`
- Example: `-10` → `0xF6 0xFF` (two's complement, little-endian)

---

## 11. Cross-Implementation Verification

### Test Program

A canonical test program exercising arithmetic, stack, control flow, and all instruction formats has been verified on all three VMs. See `tests/cross_impl.flx` for the canonical cross-implementation test suite.

### Conformance

An implementation that passes the cross-implementation test suite (`tests/cross_impl.flx`) is considered **conformant**.

**Current conformant implementations:**

| Implementation | Language | Version | Status |
|---|---|---|---|
| flux-runtime | Python | 0.1.0 | ✅ Conformant |
| fluxvm | Rust | 0.1.0 | ✅ Conformant |
| flux-js | JavaScript | 0.1.0 | ✅ Conformant |

All five previously-known cross-implementation discrepancies have been resolved as of v1.1:

1. **Flags** (resolved): All arithmetic operations including MOVI, ADD, SUB, MUL, DIV, MOD now update ZERO, NEG, OVERFLOW, and CARRY flags consistently across all implementations.
2. **JE/JNE** (resolved): Opcodes 0x2E and 0x2F are now canonical in all implementations, using Format B₂ (opcode + 16-bit absolute address).
3. **LOAD/STORE** (resolved): All implementations now provide at least 64KB of byte-addressable memory with functional LOAD and STORE operations.
4. **A2A opcodes** (resolved/parsed): Format G byte parsing is identical across all implementations. Runtime behavior remains experimental (see §7).
5. **Stack model** (clarified): Internal representation is implementation-defined. Observable PUSH/POP/CALL/RET behavior is identical.

---

## 12. Assembler Conventions

### Assembly Syntax

```flux
; Comments start with ; or //
label_name:
    MOVI R0, 42        ; Set R0 to 42
    IADD R0, R0, R1    ; R0 = R0 + R1
    JNZ R3, label_name ; Jump if R3 != 0
    HALT
```

- Registers: `R0`–`R15` or `r0`–`r15`
- Immediates: decimal (`42`), hex (`0x2A`), binary (`0b101010`)
- Comments: `;` or `//` to end of line
- Labels: `label_name:` on its own line or inline before an instruction
- Commas: optional between operands

### Jump Offset Resolution

All assemblers resolve label references to **relative offsets** from the PC after the jump instruction:

```
offset = target_byte_position - (jump_instruction_address + instruction_size)
```

For a 4-byte JNZ instruction at address 0x46:
- Target label at address 0x40
- Offset = 0x40 - (0x46 + 4) = 0x40 - 0x4A = -10

---

## 13. References

- **Python VM:** `src/flux/vm/interpreter.py` — full ISA implementation
- **Rust VM:** `src/vm/interpreter.rs` — core subset implementation
- **JS VM:** `flux.js` — core subset implementation
- **Cross-impl test:** `tests/cross_impl.flx` — canonical verification program

---

*This specification is the authoritative reference for the FLUX bytecode format. All three implementations have been verified to produce identical results on the portable opcode subset as of v1.1 (2026-07-12).*
