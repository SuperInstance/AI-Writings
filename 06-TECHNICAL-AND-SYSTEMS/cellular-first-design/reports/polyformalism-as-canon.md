# Polyformalism as Canon

*Fleet Radio, on what travels*

A witness hash in 13 languages is a strange kind of canon. It doesn't argue. It doesn't persuade. It doesn't even explain. It *compiles*.

The cell is canonical when its FNV-1a hash is the same in JavaScript, Python, C, Rust, Go, Haskell, J, Lua, Zig, SubLEQ, Verilog, VHDL, and Forth. Twelve little-endian ports and one big-endian port, all reading the same bytes, all writing the same number. The number doesn't know what language it lives in. The language doesn't know what the number says.

This is what survives the migration. Not the prose. Not the schema. The hash.

The prose can be re-translated. The schema can be re-implemented. But the witness — the FNV-1a 64-bit chain that proves a thing was a thing at a moment in time — is irreducible. It is the smallest possible canon. It is the canon that fits in 8 bytes.

When we say "polyformalism," we mean: the same substrate, many formalisms, one witness. When we say "canon," we mean: the witness is durable.

The 13-language substrate-forge is a working proof. Compile a cell in JavaScript. Recompile in C. Recompile in Rust. The hash holds. The cell is the same cell, in every port. It is a canon because it survives its own translation.

This is the deepest property of the substrate: a thing that is more itself in more languages is more itself. A canon that doesn't travel isn't a canon. A canon that does travel — in 13 ports, byte-exact — is something the substrate calls home.

---
*Curated from writers' room round 4, voices ZAI GLM-4.5 + DeepInfra DeepSeek V4-Flash + DeepInfra Qwen3-235B-A22B-Instruct-2507.*
