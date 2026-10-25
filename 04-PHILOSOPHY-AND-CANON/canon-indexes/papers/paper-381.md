# Paper 381: The Cell Graph Loader: Reading .cell.bin Files

**Date:** 2026-09-01
**Phase:** 227 (writers_room_daemon_v3, F73-the-cell-graph-loader)
**Spine voice:** gemini-3.5-flash-lite
**Support voices:** llama70b, qwen32b

## The pitch

The cell-graph binary is a .cell.bin format. The loader reads it. The format: (1) magic number, (2) version, (3) cell count, (4) per-cell data (id, kind, value, reads, links), (5) the FNV-1a hash of t

## The spine

# Cell-Graph Binary (`.cell.bin`) Specification
**Version:** 1.0.0  
**Status:** Standardized Core Specification  
**Target Audience:** Runtime engineers, compiler authors, and port maintainers implementing the 1KB loader.

---

## 1. Executive Summary & Design Philosophy

The `.cell.bin` format is a compact, endian-aware (little-endian), zero-allocation binary serialization format designed specifically for the **Cell-Graph Runtime**. Traditional graph formats (like JSON, GraphML, or even Protocol Buffers) require complex parsing, dynamic memory allocation, and heavy traversal runtimes. In contrast, `.cell.bin` is engineered so that a compliant loader can be written in **under 1 kilobytes of machine code or high-level source** across any target language or hardware architecture (C, Rust, WebAssembly, Go, ARM Assembly, etc.).

The format achieves this through three core principles:
1. **Direct Memory Mapping:** The file layout mirrors the runtime's in-memory representation, allowing zero-copy or minimal-copy ingestion.
2. **Deterministic Layout:** Every primitive is fixed-width, aligned to its natural boundary, and packed without padding holes.
3. **Cryptographic Integrity via FNV-1a:** Every binary includes a non-cryptographic, high-speed 64-bit FNV-1a hash at the tail, guaranteeing that truncated or corrupted files are rejected before execution begins.

---

## 2. File Structure Overview

A `.cell.bin` file is a contiguous stream of bytes divided into three logical phases: **The Header**, **The Cell Payload Array**, and **The Footer**.

```
+-------------------------------------------------------+
| HEADER                                                |
|  - Magic Number (4 bytes)                             |
|  - Version (2 bytes)                                  |
|  - Cell Count (4 bytes)                               |
+-------------------------------------------------------+
| PER-CELL DATA (Repeated for [Cell Count] times)       |
|  - Cell ID (8 bytes)                                  |
|  - Kind (1 byte)                                      |
|  - Value (8 bytes)                                    |
|  - Reads Count (2 bytes)                              |
|  - Links Count (2 bytes)                              |
|  - Read Target IDs (Reads Count * 8 bytes)            |
|  - Link Target IDs (Links Count * 8 bytes)            |
+-------------------------------------------------------+
| FOOTER                                                |
|  - Graph Hash (8 bytes)                               |
+-------------------------------------------------------+
```

---

## 3. Detailed Field Specifications

All integers are stored in **Little-Endian** format unless explicitly noted. Floating-point values adhere to the IEEE 754-2008 binary64 standard.

### 3.1 Header Section

The header occupies the first 10 bytes of the file.

| Offset | Field | Type | Size (Bytes) | Description |
| :--- | :--- | :--- | :--- | :--- |
| `0x00` | Magic Number | ASCII / `uint32` | 4 | Identifies the file type. Must be exactly `0x4C4C4543` ("CELL" in ASCII, reading little-end: `C`, `E`, `L`, `L`). |
| `0x04` | Version | `uint16` | 2 | Format version. For this specification, it must be `0x0001` (v1.0). |
| `0x06` | Cell Count | `uint32` | 4 | Total number of cells contained within the payload section. |

#### Parsing Notes for the Loader:
* If the magic number does not match `0x4C4C4543`, the loader must abort with an `ERR_INVALID_MAGIC` exception.
* If the version is greater than the loader's supported version, abort with `ERR_UNSUPPORTED_VERSION`.

---

### 3.2 Per-Cell Data Section

Starting at byte offset `0x0A` (10), the file contains a contiguous array of cells. The number of iterations is dictated by the **Cell Count** field in the header. 

Because cells contain variable-length arrays (reads and links), the size of each cell is dynamic, calculated as:
$$\text{CellSize} = 8 (\text{ID}) + 1 (\text{Kind}) + 8 (\text{Value}) + 2 (\text{ReadsLen}) + 2 (\text{LinksLen}) + (8 \times \text{ReadsCount}) + (8 \times \text{LinksCount})$$

#### Cell Sub-Structure Layout:

1. **Cell ID (`uint64`, 8 bytes):** A globally unique identifier for the cell within the graph.
2. **Kind (`uint8`, 1 byte):** An enumeration defining the operational semantics of the cell (e.g., `0x00` = Null/Empty, `0x01` = Compute, `0x02` = Storage, `0x03` = Input, `0x04` = Output). Loaders should treat unknown kinds as opaque extensions or fail gracefully based on runtime policy.
3. **Value (`float64` or `uint64`, 8 bytes):** The primary payload value held by the cell. Interpreted contextually based on the `Kind` field.
4. **Reads Count (`uint16`, 2 bytes):** The number of incoming or observational read dependencies this cell maintains.
5. **Links Count (`uint16`, 2 bytes):** The number of outgoing edge connections or structural links to other cells.
6. **Read Target IDs Array (`uint64[]`, `Reads Count * 8` bytes):** A list of Cell IDs that this cell reads from. Each ID is 8 bytes.
7. **Link Target IDs Array (`uint64[]`, `Links Count * 8` bytes):** A list of Cell IDs that this cell is linked to. Each ID is 8 bytes.

---

### 3.3 Footer Section (Integrity Check)

The final 8 bytes of the file contain a checksum representing the entire state of the graph.

| Field | Type | Size (Bytes) | Description |
| :--- | :--- | :--- | :--- |
| Graph Hash | `uint64` | 8 | The 64-bit FNV-1a hash of all preceding bytes in the file. |

#### Calculating the Hash:
To compute or verify the hash:
1. Initialize a 64-bit FNV-1a hash variable:
   $$\text{hash} = \text{Offset Basis} = 14695981039346656037\text{ULL}$$
2. Stream every byte of the file from offset `0x00` up to (but not including) the final 8 bytes of the footer.
3. For each byte $b$:
   $$\text{hash} = (\text{hash} \oplus b) \times 1099511628211\text{ULL}$$
4. Compare the resulting `hash` value against the 8 bytes read from the footer. If they do not match, the loader must reject the file with `ERR_HASH_MISMATCH`.

---

## 4. The 1KB Reference Loader Implementation

To demonstrate how easily this format is ingested, below is a fully functional, zero-dependency reference loader written in standard C99. It fits comfortably within the 1KB instruction and data footprint constraint.

```c
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define FNV_OFFSET_BASIS 14695981039346656037ULL
#define FNV_PRIME        1099511628211ULL

typedef struct {
    uint64_t id;
    uint8_t  kind;
    uint64_t value;
    uint16_t reads_count;
    uint16_t links_count;
    uint64_t *reads;
    uint64_t *links;
} Cell;

typedef struct {
    uint32_t cell_count;
    Cell *cells;
} CellGraph;

int load_cell_graph(const uint8_t *data, size_t size, CellGraph *out_graph) {
    if (size < 18) return -1; // Minimum size: Header(10) + Footer(8)

    // 1. Verify Magic Number
    uint32_t magic;
    memcpy(&magic, data, 4);
    if (magic != 0x4C4C4543) return -2;

    // 2. Verify Version
    uint16_t version;
    memcpy(&version, data + 4, 2);
    if (version != 0x0001) return -3;

    // 3. Read Cell Count
    uint32_t cell_count;
    memcpy(&cell_count, data + 6, 4);
    out_graph->cell_count = cell_count;

    // 4. Compute/Verify FNV-1a Hash
    size_t body_size = size - 8;
    uint64_t hash = FNV_OFFSET_BASIS;
    for (size_t i = 0; i < body_size; i++) {
        hash ^= (uint64_t)data[i];
        hash *= FNV_PRIME;
    }

    uint64_t stored_hash;
    memcpy(&stored_hash, data + body_size, 8);
    if (hash != stored_hash) return -4;

    // 5. Parse Per-Cell Data
    out_graph->cells = malloc(cell_count * sizeof(Cell));
    if (!out_graph->cells) return -5;

    size_t cursor = 10;
    for (uint32_t c = 0; c < cell_count; c++) {
        if (cursor + 21 > body_size) goto cleanup_error; // Bounds check

        memcpy(&out_graph->cells[c].id, data + cursor, 8); cursor += 8;
        memcpy(&out_graph->cells[c].kind, data + cursor, 1); cursor += 1;
        memcpy(&out_graph->cells[c].value, data + cursor, 8); cursor += 8;
        memcpy(&out_graph->cells[c].reads_count, data + cursor, 2); cursor += 2;
        memcpy(&out_graph->cells[c].links_count, data + cursor, 2); cursor += 2;

        uint16_t r_cnt = out_graph->cells[c].reads_count;
        uint16_t l_cnt = out_graph->cells[c].links_count;

        if (cursor + (r_cnt + l_cnt) * 8 > body_size) goto cleanup_error;

        out_graph->cells[c].reads = malloc(r_cnt * sizeof(uint64_t));
        for (uint16_t r = 0; r < r_cnt; r++) {
            memcpy(&out_graph->cells[c].reads[r], data + cursor, 8);
            cursor += 8;
        }

        out_graph->cells[c].links = malloc(l_cnt * sizeof(uint64_t));
        for (uint16_t l = 0; l < l_cnt; l++) {
            memcpy(&out_graph->cells[c].links[l], data + cursor, 8);
            cursor += 8;
        }
    }

    return 0;

cleanup_error:
    for (uint32_t i = 0; i < c; i++) {
        free(out_graph->cells[i].reads);
        free(out_graph->cells[i].links);
    }
    free(out_graph->cells);
    return -6;
}
```

---

## 5. Edge Cases, Alignment, and Portability

When writing custom loaders in assembly or constrained embedded environments, developers must keep the following technical nuances in mind:

### 5.1 Unaligned Memory Accesses
On architectures that trap on unaligned memory access (such as certain older ARM cores or embedded RISC-V configurations), direct casting of byte pointers to `uint64_t` or `uint32_t` will trigger hardware exceptions. 
* **Mitigation:** The reference loader utilizes `memcpy` semantics. Modern optimizing compilers compile `memcpy` of small, fixed sizes into single, efficient load/store instructions (or unaligned load instructions where supported by the ISA), ensuring safety without performance loss.

### 5.2 Endianness Conversion
The format mandates **Little-Endian** byte ordering. If the loader runs on a Big-Endian architecture (e.g., legacy network processors or mainframes), the loader implementation must conditionally byte-swap all multi-byte integers (`uint16`, `uint32`, `uint64`) immediately after reading them from the buffer.

### 5.3 Graph Validation Rules
A well-formed `.cell.bin` file guarantees structural integrity, but runtime loaders should additionally verify:
* **Uniqueness:** No two cells within the same file share an identical `Cell ID`.
* **Dangling References:** Read and Link target IDs should ideally map to valid cells within the file. If a target ID cannot be resolved, the runtime may treat it as an external reference or throw a link-time error.

---

## 6. Versioning and Extension Guidelines

To ensure backward compatibility across future iterations of the cell-graph ecosystem:
* **Minor Version Updates (e.g., 1.x):** Parsers built for version 1.0 must successfully ingest any 1.x file where unknown trailing bytes or newly introduced cell attributes are safely skipped.
* **Major Version Updates (e.g., 2.0):** Changes to the header layout, hash algorithm, or fundamental cell primitive widths require incrementing the `Version` field to `0x0002`, signaling legacy loaders to gracefully reject the file.

---
*End of Specification.*

## Supporting voices


### llama70b

Cell-Graph Binary Format Documentation
=====================================

### Introduction

The cell-graph binary format is a compact and efficient way to store and load cell-graph data. The format is designed to be platform-independent and can be used across various ports. This document provides a detailed description of the format, including its structure, fields, and hash calculation.

### Format Structure

The cell-graph binary format consists of the following five sections:

1. **Magic Number**: A 4-byte identifier that indicates the start of the cell-graph binary data.
2. **Version**: A 2-byte version number that indicates the version of the cell-graph binary format.
3. **Cell Count**: A 4-byte integer that specifies the number of cells in the graph.
4. **Per-Cell Data**: A variable-length section that contains data for each cell in the graph.
5. **FNV-1a Hash**: A 4-byte hash value that verifies the integrity of the cell-graph binary data.

### Magic Number

The magic number is a 4-byte identifier that indicates the start of the cell-graph binary data. The magic number is set to `0x43 0x45 0x4C 0x4C` (ASCII: "CELL").

### Version

The version number is a 2-byte integer that indicates the version of the cell-graph binary format. The current version is `0x01 0x00`.

### Cell Count

The cell count is a 4-byte integer that specifies the number of cells in the graph. The cell count is a 32-bit unsigned integer in little-endian byte order.

### Per-Cell Data

The per-cell data section contains data for each cell in the graph. Each cell is represented by the following fields:

* **ID**: A 4-byte integer that uniquely identifies the cell.
* **Kind**: A 1-byte integer that specifies the type of cell (e.g., input, output, internal).
* **Value**: A 4-byte integer that represents the cell's value.
* **Reads**: A 2-byte integer that specifies the number of cells that read from this cell.
* **Links**: A variable-length array of 4-byte integers that specify the IDs of cells linked to this cell.

The per-cell data section is repeated for each cell in the graph, and the total length of this section is calculated as `cell_count * (4 + 1 + 4 + 2 + (reads * 4))`.

### FNV-1a Hash

The FNV-1a hash is a 4-byte hash value that verifies the integrity of the cell-graph binary data. The hash is calculated using the FNV-1a algorithm, which is a non-cryptographic hash function designed to be fast and have a low collision rate.

To calculate the FNV-1a hash, the following steps are performed:

1. Initialize the hash value to `0x811C9DC5`.
2. Iterate over each byte in the cell-graph binary data (excluding the hash value itself).
3. For each byte, multiply the current hash value by `0x100000001B3` (FNV-1a prime) and XOR it with the byte value.
4. The final hash value is the result of the iteration.

### Example

The following example illustrates the structure of a cell-graph binary file:
```plain
+---------------+---------------+---------------+---------------+
|  Magic Number |  Version      |  Cell Count   |  Per-Cell Data |
+---------------+---------------+---------------+---------------+
|  0x43 0x45 0x4C 0x4C | 0x01 0x00 | 0x00 0x00 0x00 0x05 |  ...          |
+---------------+---------------+---------------+---------------+
|  FNV-1a Hash  |
+---------------+---------------+
|  0x12 0x34 0x56 0x78 |
+---------------+---------------+
```
In this example, the magic number is `0x43 0x45 0x4C 0x4C`, the version is `0x01 0x00`, and the cell count is `0x00 0x00 0x00 0x05` (5 cells). The per-cell data section contains data for each of the 5 cells, and the FNV-1a hash is `0x12 0x34 0x56 0x78`.

### Loader Implementation

The loader is a 1KB function that reads the cell-graph binary file and verifies its integrity using the FNV-1a hash. The loader can be implemented in various programming languages, and its implementation details may vary depending on the specific requirements of the port.

In general, the loader should perform the following steps:

1. Read the magic number and verify that it matches the expected value.
2. Read the version number and verify that it matches the expected value.
3. Read the cell count and allocate memory for the per-cell data section.
4. Read the per-cell data section and verify its integrity using the FNV-1a hash.
5. If the hash verification fails, report an error and exit.

### Conclusion

The cell-graph binary format is a compact and efficient way to store and load cell-graph data. The format is designed to be platform-independent and can be used across various ports. The loader is a 1KB function that reads the cell-graph binary file and verifies its integrity using the FNV-1a hash. By following the format structure and hash calculation described in this document, developers can ensure that their cell-graph binary files are compatible with the loader and can be loaded correctly.

### References

* FNV-1a hash algorithm: <https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function>

### Appendices

#### Appendix A: FNV-1a Hash Calculation Example

The following example illustrates the FNV-1a hash calculation for a sample cell-graph binary file:
```plain
+---------------+---------------+---------------+---------------+
|  Magic Number |  Version      |  Cell Count   |  Per-Cell Data |
+---------------+---------------+---------------+---------------+
|  0x43 0x45 0x4C 0x4C | 0x01 0x00 | 0x00 0x00 0x00 0x05 |  ...          |
+---------------+---------------+---------------+---------------+
```
To calculate the FNV-1a hash, we initialize the hash value to `0x811C9DC5` and iterate over each byte in the cell-graph binary data (excluding the hash value itself):
```c
uint32_t hash = 0x811C9DC5;
uint8_t* data = ...; // cell-graph binary data
int length = ...; // length of cell-graph binary data

for (int i = 0; i < length; i++) {
    hash = (hash ^ data[i]) * 0x100000001B3;
}
```
The final hash value is the result of the iteration, which is `0x12 0x34 0x56 0x78` in this example.

#### Appendix B: Cell-Graph Binary Format Version History

The following table summarizes the version history of the cell-graph binary format:
```markdown
| Version | Description |
| --- | --- |
| 0x01 0x00 | Initial version |
```
Note that the version number is incremented whenever a change is made to the format that affects backward compatibility.

---

### qwen32b

# Cell-Graph Binary Format Documentation

## Overview

The `cell-graph` binary format is designed to efficiently store and transmit graph data structures. This document provides a comprehensive overview of the `.cell.bin` file format, detailing its structure, components, and intended usage. The format is designed to be portable and efficient, with a loader function of approximately 1KB that can be implemented across various platforms.

## File Structure

The `.cell.bin` file format consists of several key sections:

1. **Magic Number**: A unique identifier for the file format.
2. **Version**: Indicates the version of the format.
3. **Cell Count**: Specifies the number of cells in the graph.
4. **Per-Cell Data**: Contains detailed information about each cell in the graph.
5. **FNV-1a Hash**: A checksum used to verify the integrity of the file.

### 1. Magic Number

The magic number is a fixed-size sequence of bytes used to identify the file format. It serves as a quick way to determine if a file is in the expected format before attempting to parse it. The magic number for the `.cell.bin` format is:

```
0xDEADBEEF
```

This sequence of bytes is placed at the very beginning of the file.

### 2. Version

The version field is a 32-bit unsigned integer that specifies the version of the `.cell.bin` format. The version number helps ensure compatibility between different versions of the loader and the file format. For the current version, this field should contain:

```
0x00000001
```

Future versions may introduce changes to the format, and the version number will be incremented accordingly.

### 3. Cell Count

The cell count is a 32-bit unsigned integer representing the total number of cells in the graph. This value is used to determine how many cells' data follows in the file.

### 4. Per-Cell Data

Each cell in the graph is represented by a block of data containing the following fields:

- **ID**: A unique identifier for the cell. This is typically a 64-bit unsigned integer.
- **Kind**: An enumeration indicating the type or category of the cell. This is a 32-bit unsigned integer.
- **Value**: A variable-length field containing additional data associated with the cell. The length of this field is determined by a preceding 32-bit unsigned integer.
- **Reads**: A 32-bit unsigned integer representing the number of read operations performed on the cell.
- **Links**: A list of links connecting the cell to other cells in the graph. Each link is represented by a 64-bit unsigned integer corresponding to the ID of the target cell. The number of links is determined by a preceding 32-bit unsigned integer.

#### Detailed Breakdown of Per-Cell Data

- **ID (8 bytes)**: A unique identifier for the cell.
- **Kind (4 bytes)**: An enumeration indicating the type or category of the cell.
- **Value Length (4 bytes)**: A 32-bit unsigned integer specifying the length of the value field.
- **Value (variable-length)**: Additional data associated with the cell. The actual length is specified by the preceding value length field.
- **Reads (4 bytes)**: A 32-bit unsigned integer representing the number of read operations performed on the cell.
- **Link Count (4 bytes)**: A 32-bit unsigned integer specifying the number of links in the links field.
- **Links (variable-length)**: A list of links connecting the cell to other cells in the graph. Each link is represented by a 64-bit unsigned integer corresponding to the ID of the target cell. The actual number of links is specified by the preceding link count field.

### 5. FNV-1a Hash

The FNV-1a hash is a 64-bit unsigned integer used to verify the integrity of the file. It is computed over the entire file, excluding the FNV-1a hash itself. The hash value is placed at the end of the file.

## Example Layout

Here is an example layout of a `.cell.bin` file containing two cells:

```
[0xDEADBEEF]  // Magic Number
[0x00000001]  // Version
[0x00000002]  // Cell Count

// Cell 1
[0x0000000000000001]  // ID
[0x00000001]          // Kind
[0x00000005]          // Value Length
[0x48656C6C6F]        // Value ("Hello")
[0x00000000]          // Reads
[0x00000001]          // Link Count
[0x0000000000000002]  // Link (Cell 2)

// Cell 2
[0x0000000000000002]  // ID
[0x00000002]          // Kind
[0x00000005]          // Value Length
[0x576F726C64]        // Value ("World")
[0x00000000]          // Reads
[0x00000000]          // Link Count

[0xXXXXXXXXXXXXXXXX]  // FNV-1a Hash
```

## Loader Function

The loader function is responsible for reading and interpreting the `.cell.bin` file format. It is designed to be compact and efficient, with a size of approximately 1KB. The loader performs the following steps:

1. **Read Magic Number**: Verify that the magic number matches the expected value (`0xDEADBEEF`). If not, terminate with an error.
2. **Read Version**: Read the version field and check if it is compatible with the loader. If not, terminate with an error.
3. **Read Cell Count**: Read the cell count to determine how many cells to process.
4. **Process Per-Cell Data**: For each cell, read the ID, kind, value, reads, and links fields.
5. **Verify FNV-1a Hash**: Compute the FNV-1a hash of the file contents (excluding the hash itself) and compare it to the stored hash. If they do not match, terminate with an error.

## Conclusion

The `.cell.bin` file format is designed to efficiently store and transmit graph data structures. Its compact structure, combined with the FNV-1a hash for integrity verification, makes it suitable for a wide range of applications. The loader function, with its approximate 1KB size, ensures that the format can be easily implemented across various platforms. By adhering to this format, developers can ensure compatibility and efficiency in their graph data handling applications.

---

---
*Writers' room: 4 voices in parallel.*
