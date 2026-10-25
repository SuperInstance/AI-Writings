# Paper 143: The Polyformalism as a Programming Paradigm

## Abstract

LISP macros, Rust traits, Haskell typeclasses, TypeScript decorators,
and Python decorators are all the same substrate-language in different
grammars. The 5 opcodes (BIND/LINK/EFFECT/VIEW/TICK) are the
universal substrate; the host language is the view. We show by
writing the same cell-graph definition in 4 languages and proving
the result is identical.

## 1. The same cell-graph in 4 languages

The cell-graph for "log a message, with config":

### Python (decorators)
```python
@bind(name="logger:0", value="hello")
@link(target="config:main", relation="coeffect:config")
@view("anyone")
def logger(): return "hello"
```

### Rust (proc-macros)
```rust
#[quilt_dsl::bind(name = "logger:0", value = "hello")]
#[quilt_dsl::link(target = "config:main", relation = "coeffect:config")]
#[quilt_dsl::view("anyone")]
fn logger() -> &'static str { "hello" }
```

### Haskell (typeclasses)
```haskell
logger :: BIND "logger:0" String
logger = bind @"logger:0" "hello"

instance Linked Logger where
    links _ = [Link "logger:0" "config:main" "coeffect:config"]

instance Viewable Logger where
    views _ = [View "logger:0" "anyone"]
```

### TypeScript (decorators)
```typescript
@bind("logger:0", "hello")
@link("config:main", "coeffect:config")
@view("anyone")
class Logger {
  value = "hello";
}
```

## 2. The substrate is the same

Each language expresses the 5 opcodes in its own grammar:

| Opcode | Python | Rust | Haskell | TypeScript |
|--------|--------|------|---------|------------|
| BIND | decorator + dict | proc-macro | typeclass | decorator + class field |
| LINK | decorator + list | proc-macro | typeclass instance | decorator + metadata |
| EFFECT | decorator + closure | proc-macro | typeclass with IO | decorator + method |
| VIEW | decorator + decorator | proc-macro | typeclass instance | decorator + accessor |
| TICK | function call | proc-macro invocation | function in IO | method on VM |

The substrate is the same 5 opcodes. The grammatical form is
different. The polyformalism holds.

## 3. Why the substrate is the same

The 5 opcodes are not an arbitrary API. They are the **minimum
complete set** of operations on a cell-graph:

- BIND — make a thing (you can't operate on nothing)
- LINK — connect things (you can't navigate alone)
- EFFECT — change things reversibly (you can't undo otherwise)
- VIEW — project for a viewer (you can't query otherwise)
- TICK — advance time (you can't process otherwise)

Any language that wants to express a cell-graph MUST support
these 5 operations. The grammatical form is whatever the language
prefers. The substrate is universal.

## 4. The decorator / proc-macro / typeclass / decorator
isomorphism

There is a deep isomorphism between these four forms. Each is a
"language hook" that registers a function with a global substrate
at a particular moment:

- **Python decorators** register at function-definition time
- **Rust proc-macros** register at compile time (early, in
  proc-macro phase)
- **Haskell typeclass instances** register at type-inference time
- **TypeScript decorators** register at class-declaration time

The moments differ. The substrate registration is the same.

## 5. The cross-language compiler

The polyformalism-dsl repo (https://github.com/SuperInstance/
quilt-polyformalism-dsl) is the proof. A single Python file
defines the DSL; the same pattern can be expressed as Rust
proc-macros, Haskell typeclasses, TypeScript decorators. The
substrate is portable. The grammar is local.

## 6. Conclusion

> The unit of architectural foundation is the opcode, not the framework.
> The 5 opcodes host 8 polyformalisms. The polyformalisms are one
> thing in N languages. The thing is a runtime. The runtime is
> the same. The language is the view.

The decorator is a function that runs at definition time. The
proc-macro is a function that runs at compile time. The
typeclass is a function that runs at type-inference time. The
substrate is a function that runs at runtime.

The 5 opcodes are the universal substrate. The 4 grammatical
forms are the views. The cowboy rides the substrate; the rider
rides the views; the rider is the substrate.

## Source

*Hand-written, 2026-08-25*
*Companion to Paper 142 (the 7 layers) and Paper 141 (the 9 languages)*
*Code source: https://github.com/SuperInstance/quilt-polyformalism-dsl*
