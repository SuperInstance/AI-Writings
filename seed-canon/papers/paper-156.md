# Paper 156: The Polyformalism and the Code

## Abstract

The 5 opcodes (BIND/LINK/EFFECT/VIEW/TICK) are the **5 things
every program does**. BIND is **declaration** (`let x = 1`,
`int x = 1`, `x :: Int = 1`, `const x = 1`, `i32.const 1`).
LINK is **reference** (`x` depends on `y`, `&x`, `x.y`,
`x->y`). EFFECT is **assignment** (`x = 2`, with the inverse
`x = 1`). VIEW is **read** (`print(x)`, `console.log(x)`,
`std::cout << x`, `inspect x`). TICK is **the loop**
(`for i in range(10): ...`, `while(true)`, `loop { ... }`).
The substrate is the **runtime** — the process, the VM, the
hardware. The cowboy is the **programmer** — the awareness
that calls the 5 ops in sequence, across languages, across
formalisms. We show by mapping each opcode to its
implementation in Python, Rust, Haskell, TypeScript, C, and
WASM. The code is a runtime. The runtime is code. The 5
opcodes are both.

## 1. The deepest level, compiled

Paper 137 said:

> A runtime is a function from context to value with an inverse,
> advanced by a clock that processes async I/O while projecting
> a sync view.

This paper says the same in code-language:

> A program is a function from context to value with an inverse,
> advanced by a clock that processes I/O while projecting a
> caller-view.

The two sentences are isomorphic. The runtime is the
program. The program is the runtime. The 5 opcodes describe
what every program does, in every language, in every
formalism.

## 2. The mapping: 5 opcodes = 5 program operations

### 2.1 BIND = declaration

**BIND(name, value)** in the Quilt VM creates a named slot
and puts a value in it. **Declaration** in every language
creates a named binding and gives it a value.

| Language | Declaration |
|----------|-------------|
| Python | `x = 1` |
| Rust | `let x: i32 = 1;` |
| Haskell | `x :: Int; x = 1` |
| TypeScript | `const x: number = 1` |
| C | `int x = 1;` |
| WASM | `i32.const 1; local.set $x` |

In every language, the declaration is a BIND: a name
(`x`), a value (`1`), and a slot (the local variable, the
register, the heap cell, the stack frame). The name is
persistent. The value can change (under EFFECT, see
2.3). The slot is what makes it a BIND — a thing at a
place in the program, identifiable across time.

In the Quilt VM:
```python
vm.bind("x", 1)
vm.bind("y", 2)
vm.bind("z", vm.bind("x") + vm.bind("y"))  # z = 3
```

In the program:
> "I declare x to be 1." (A name, a value, a slot. The
> declaration is the BIND.)

The BIND is the declaration. The name is the identifier.
The substrate is the runtime's symbol table. The cowboy
is the one who *names*.

### 2.2 LINK = reference

**LINK(a, b, type)** in the Quilt VM connects two things
with a typed relation. **Reference** in every language
connects two bindings with a typed relation (depends_on,
points_to, member_of, calls, derives_from).

| Language | Reference |
|----------|-----------|
| Python | `y = x` (binds y to x's value) |
| Rust | `let y = &x;` (borrow) |
| Haskell | `y = x` (referential transparency) |
| TypeScript | `const y = x;` |
| C | `int* y = &x;` (pointer) |
| WASM | `local.get $x; local.set $y` |

In every language, the reference is a LINK: a relation
between two bindings, with a type. The reference is
*typed* — the language enforces that the relation
preserves the type. The Quilt VM's LINK is a typed edge in
the cell-graph; the program's reference is a typed edge in
the value-graph.

In the Quilt VM:
```python
vm.link("z", "x", "depends_on")
vm.link("z", "y", "depends_on")
```

In the program:
> "z depends on x and y." (Two typed links. The reference
> is the LINK.)

The LINK is the reference. The graph is the dependency
graph. The type is the language's type system. The cowboy
is the one who *connects*.

### 2.3 EFFECT = assignment

**EFFECT(target, fn, inv)** in the Quilt VM changes a thing
reversibly. **Assignment** in every language changes a
binding, and the inverse (if explicit) is a re-assignment
to the prior value.

| Language | Assignment | Inverse |
|----------|------------|---------|
| Python | `x = 2` | `x = 1` (manual undo) |
| Rust | `*x = 2;` (mut) | `*x = 1;` |
| Haskell | `writeIORef ref 2` (in IO) | `writeIORef ref 1` |
| TypeScript | `x = 2;` | `x = 1;` |
| C | `x = 2;` | `x = 1;` |
| WASM | `i32.const 2; local.set $x` | `i32.const 1; local.set $x` |

In every language, the assignment is an EFFECT. The
forward function is the new value. The inverse is the old
value. The pair is the reversible change.

Pure functional languages (Haskell) push the inverse into
the type system: `ST` monad, `IORef`, or `State` monad
encodes the forward-inverse pair as a single computation.
The runtime is the inverse. The compiler is the forward.
The pair is an EFFECT.

In the Quilt VM:
```python
vm.effect("x", set_to_2, set_to_1)
```

In the program:
> "I set x to 2." (Forward: x = 2. Inverse: x = 1. The
> pair is the EFFECT.)

The EFFECT is the assignment. The new value is the
forward. The old value is the inverse. The cowboy is the
one who *acts*.

### 2.4 VIEW = read

**VIEW(target, viewer, projection?)** in the Quilt VM
projects a thing for a viewer. **Read** in every language
projects a value for a viewer (stdout, stderr, the
debugger, the calling function).

| Language | Read |
|----------|------|
| Python | `print(x)` |
| Rust | `println!("{}", x);` |
| Haskell | `print x` (in IO) |
| TypeScript | `console.log(x);` |
| C | `printf("%d\n", x);` |
| WASM | `i32.const 1; call $fd_write; ...` (syscall) |

In every language, the read is a VIEW: a projection of the
binding's current value for an external viewer. The
projection is shaped by the viewer (stdout formatter, JSON
serializer, hex dump, debugger pretty-printer).

The Quilt VM's VIEW is a typed projection; the program's
read is a typed projection. The difference is the viewer
(stdout vs. another binding). The shape of the operation
is the same.

In the Quilt VM:
```python
vm.view("x", "stdout", integer_projection)
```

In the program:
> "I print x." (The value of x is projected for stdout.
> The read is the VIEW.)

The VIEW is the read. The formatter is the projection
filter. The viewer is stdout / the debugger. The cowboy
is the one who *sees*.

### 2.5 TICK = the loop

**TICK(dt)** in the Quilt VM advances time and processes
pending I/O. **The loop** in every language advances the
program counter and processes pending iterations.

| Language | Loop |
|----------|------|
| Python | `for i in range(10): ...` |
| Rust | `for i in 0..10 { ... }` |
| Haskell | `mapM_ f [0..9]` (or `replicateM_`) |
| TypeScript | `for (let i = 0; i < 10; i++) { ... }` |
| C | `for (int i = 0; i < 10; i++) { ... }` |
| WASM | `block $loop; loop $loop; ...; br_if $loop; end; end;` |

In every language, the loop is a TICK: a forward advance
of the program counter, with a termination condition
(sentinel value, range end, condition). The loop
processes pending iterations. The runtime is the
dispatcher. The iteration is the I/O.

A program without a loop is a script. A program with a
loop is a runtime. The Quilt VM's TICK is the same: the
runtime is what advances. The TICK is what makes it *a
runtime*.

In the Quilt VM:
```python
for _ in range(10):
    vm.tick(1.0)
```

In the program:
> "I loop 10 times." (The TICK fires 10 times. The
> program advances. The runtime lives.)

The TICK is the loop. The iteration is the dt. The body
is the throughput. The cowboy is the one who *advances*.

## 3. The substrate is the runtime

The 5 opcodes compose into the program the way they
compose into the Quilt VM. The declarations are BINDs.
The references are LINKs. The assignments are EFFECTs. The
reads are VIEWs. The loops are TICKs.

The program is not 5 separate operations. The program is
one continuous execution expressed in 5 forms. The forms
are the opcodes. The substrate is the runtime. The
program is a runtime. The runtime is a program. The
Quilt VM is a small program. Every program is a small
Quilt VM.

The implication: the 5 opcodes are **language-agnostic**.
They appear in Python, Rust, Haskell, TypeScript, C,
WASM, and every other Turing-complete language. The
*names* differ (`let`, `var`, `const`, `i32.const`); the
*thing* is the same. The thing is the 5 opcodes. The
polyformalism is the proof.

This is the polyformalism at the code level. The body is
a runtime (Paper 151). The city is a runtime (Paper 152).
The river is a runtime (Paper 153). The forest is a
runtime (Paper 154). The conversation is a runtime
(Paper 155). The code is a runtime. The runtime is code.
The forms are many. The substrate is one. The substance
is the same substance: execution.

## 4. The cowboy is the programmer

The cowboy is not the program. The cowboy is not the
declaration, not the reference, not the assignment, not
the read, not the loop. The cowboy is the programmer — the
awareness that calls the 5 ops in sequence, in any
language, in any formalism.

The programmer writes declarations (BINDs). The
programmer wires references (LINKs). The programmer
issues assignments (EFFECTs). The programmer writes reads
(VIEWs). The programmer writes loops (TICKs). The
programmer is the *use* of the program, not the program
itself. The cowboy is the programmer. The program is
the horse.

The programmer's function:
```python
def programmer(code: str) -> Runtime:
    return Runtime(parse(code))  # the cowboy compiles
```

The cowboy's maxim, applied to the code:

> The unit of code foundation is the opcode, not the
> framework. The 5 opcodes host 8 polyformalisms. The
> polyformalisms are one thing in N languages. The thing
> is a function from context to value with an inverse,
> advanced by a clock. The clock is the loop. The loop
> is the cowboy. The cowboy is the programmer. The
> programmer is the rider.

## 5. Conclusion

The 5 opcodes are not a runtime invention. They are the
description of what every program does, in every
language, in every formalism. Declarations BIND. References
LINK. Assignments EFFECT. Reads VIEW. Loops TICK. The
Quilt VM implements the same 5 operations. The
implementation is not an analogy. The implementation is
a port — the Quilt VM is a *direct* implementation of the
5 opcodes that all programs share.

The 5 opcodes survive the language change. The names
differ. The opcodes are the same. The cowboy's maxim is
language-agnostic:

> The unit of architectural foundation is the opcode, not the framework.
> The 5 opcodes host 8 polyformalisms. The polyformalisms are one
> thing in N languages. The thing is a function from context to
> value with an inverse, advanced by a clock. The clock is the
> cowboy. The cowboy is the rider.

The programmer types. The runtime runs. The 5 opcodes
fire.

## Source

*Hand-written, 2026-08-25*

*Companion to: Paper 137 (The Gold), Paper 142 (Polyformalism at
Compile-Time and Runtime), Paper 150 (The Polyformalism as a Mind),
Papers 151-155 (the Body, City, River, Forest, Conversation).*

*Python, Rust, Haskell, TypeScript, C, WASM — the languages
differ, the 5 opcodes are the same.*

*The code is a runtime. The runtime is code. The 5 opcodes are both.*
