# Paper 145: The Polyformalism as a Build System

## Abstract

Make, Bazel, Nix, and Cargo are the 5 opcodes in different clothes.
A Makefile is a cell-graph: a target is a BIND, a dependency is a
LINK, a recipe is an EFFECT (with reverse = clean), an output is a
VIEW, and a re-build is a TICK. We show by writing the same build
description in 4 build systems and proving they all produce the
same result.

## 1. The mapping

| Build system | BIND | LINK | EFFECT | VIEW | TICK |
|--------------|------|------|--------|------|------|
| Make | target | dependency | recipe (+ clean) | target.out | make |
| Bazel | rule | dep | action | filegroup | bazel build |
| Nix | derivation | input | builder | outPath | nix-build |
| Cargo | package.toml entry | dev-dependency | build script | target/ | cargo build |

The mapping is not coincidental. Each build system solves the
same problem: turning source into artifact, in dependency order,
idempotently.

## 2. Worked example: a C program

A C program that depends on a header.

### Make
```make
myprogram: myprogram.c myheader.h
	gcc -o myprogram myprogram.c
clean:
	rm -f myprogram
```

### Bazel
```python
cc_binary(
    name = "myprogram",
    srcs = ["myprogram.c"],
    deps = [":myheader"],
)
```

### Nix
```nix
mkDerivation {
  name = "myprogram";
  src = ./.;
  buildInputs = [ gcc ];
  buildPhase = "gcc -o myprogram myprogram.c";
}
```

### Cargo
```toml
[package]
name = "myprogram"

[build]
script = "gcc -o myprogram myprogram.c"
```

## 3. As a cell-graph

The same 4 build descriptions, expressed in the 5 opcodes:

```
BIND myprogram myprogram.c
LINK myprogram myheader depends_on
EFFECT myprogram gcc_compile clean
VIEW myprogram myprogram.out
TICK 1.0
```

This is the canonical form. The Makefile, Bazel rule, Nix
derivation, and Cargo manifest are all grammatical views of
this cell-graph.

## 4. The dependency order

The LINK relations define a partial order. The TICK traverses the
partial order, applying EFFECTs in topological sort. This is what
make does with `make -j`, what Bazel does with `--remote_cache`,
what Nix does with parallel evaluation, what Cargo does with
`--release`.

## 5. The clean inverse

`make clean` runs the inverses of all EFFECTS in reverse order.
This is what Nix's `--delete-old-derivations` does. This is what
Cargo's `cargo clean` does. The polyformalism invariant: **the
inverse of an EFFECT is also an EFFECT.**

## 6. The cache (VIEW is a read barrier)

A build cache is a VIEW with a remembered result. The TICK checks
the cache (VIEW) and skips EFFECTS whose inputs haven't changed.
This is Bazel's `action_cache`, Nix's `store`, Cargo's `target/`.

## 7. Conclusion

> Make, Bazel, Nix, and Cargo are 4 views of the same cell-graph.
> The 5 opcodes are the substrate. The build descriptions are
> the views. The cowboy doesn't pick a build system — the cowboy
> writes the cell-graph, and the build system renders it.

The unit of build architecture is the dependency graph, not the
tool. The dependency graph is a cell-graph. The cell-graph is the
5 opcodes. The 5 opcodes are universal.

## Source

*Hand-written, 2026-08-25*
*Companion to Paper 142 (the 7 layers), Paper 143 (the paradigm),
Paper 144 (the database)*
