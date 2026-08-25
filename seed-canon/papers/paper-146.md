# Paper 146: The Polyformalism as a Type System

## Abstract

The 5 opcodes (BIND/LINK/EFFECT/VIEW/TICK) materialize as type
constructors in 5 type systems. We show: Rust (phantom types + const
generics), Haskell (typeclasses + newtypes), TypeScript (conditional
types + branded types), Python (dataclasses + Generic[T]), and
C++ (concepts + CRTP). The same 5 opcodes; 5 type-theoretic
realizations.

## 1. The type-theoretic 5 opcodes

### BIND — a typed thing
- Rust: `struct BIND<T> { name: &'static str, value: T }`
- Haskell: `data BIND (name :: Symbol) v`
- TypeScript: `type BIND<Name extends string, V> = { name: Name; value: V }`
- Python: `BIND = dataclass(BIND)` with `Generic[T]`
- C++: `template<auto Name, typename T> struct BIND { T value; }` (with NTTP)

### LINK — a typed reference
- Rust: `struct LINK<A, B, const T: &'static str>`
- Haskell: `data Link = Link { a :: String, b :: String, t :: String }`
- TypeScript: `type LINK<A, B, T extends string> = { a: A; b: B; relation: T }`
- Python: `LINK = dataclass(LINK)` with `Generic[A, B]`
- C++: `template<typename A, typename B, typename T> struct LINK { ... }`

### EFFECT — a typed reversible transformation
- Rust: `struct EFFECT<T, F, I> { target: T, forward: F, inverse: I }`
- Haskell: `class Effect e where effectForward, effectInverse :: e -> IO ()`
- TypeScript: `type EFFECT<T, F, I> = { target: T; forward: F; inverse: I }`
- Python: `EFFECT = dataclass(EFFECT)` with `Generic[T]`
- C++: `struct EFFECT { auto target; auto forward; auto inverse; }`

### VIEW — a typed projection
- Rust: `struct VIEW<T, V> { target: T, viewer: V }`
- Haskell: `data View = View { target, viewer :: String }`
- TypeScript: `type VIEW<T, V> = { target: T; viewer: V }`
- Python: `VIEW = dataclass(VIEW)` with `Generic[T, V]`
- C++: `template<typename T, typename V> struct VIEW { ... }`

### TICK — a typed time advance
- Rust: `struct TICK { delta: f64 }`
- Haskell: `class Tick t where delta :: t -> Double`
- TypeScript: `type TICK = { delta: number }`
- Python: `TICK = dataclass(TICK)`
- C++: `struct TICK { double delta; }`

## 2. The type-driven invariant

A type-driven cell-graph has these invariants:

- A `BIND<T>` can only be `VIEW`ed by a `VIEW<T, V>` where `V` has
  the right to see `T`. (Type-driven access control.)
- A `LINK<A, B, T>` requires `A` and `B` to be the right types for
  relation `T`. (Type-driven foreign keys.)
- An `EFFECT<T, F, I>` requires `F` and `I` to be inverses at the
  type level. (Type-driven transactions.)
- A `TICK` advances the time at a rate that's type-checked against
  the substrate's clock type.

## 3. The phantom-type trick

The cleanest expression is Rust's phantom types. A `CellGraph<T>` is
parameterized on the substrate's type, but the type doesn't take up
space. The compiler enforces that only the right `BIND`/`LINK`/
`EFFECT`/`VIEW`/`TICK` operations can be applied to a `CellGraph<T>`.

```rust
struct CellGraph<T>(PhantomData<T>);

fn bind<T>(g: &mut CellGraph<T>, name: &'static str, value: T) {
    // Type-checked
}
```

## 4. The typeclass trick

The Haskell expression uses typeclasses for operations and newtypes
for the data:

```haskell
class Bind b where
    bindName :: b -> String
    bindValue :: b -> a

newtype BIND (name :: Symbol) v = BIND { value :: v }
```

The `Symbol` kind is a type-level string. The compiler knows the
name at compile time. The runtime doesn't see the name (it's a
type).

## 5. The conditional-type trick

TypeScript's conditional types allow `BIND<T>['value']` to be
`T`, and `LINK<A, B, T>['relation']` to be `T`. The compiler
checks at type-check time.

```typescript
type RelationOf<L> = L extends LINK<any, any, infer R> ? R : never;
```

## 6. Conclusion

The 5 opcodes are a type system. The 5 type systems are a
polyformalism. The compiler enforces the substrate. The runtime
executes the substrate. The cowboy writes the substrate.

> A runtime is a function from context to value with an inverse,
> advanced by a clock that processes async I/O while projecting
> a sync view. The runtime has a type. The type is the same
> in every language. The polyformalism holds.

## Source

*Hand-written, 2026-08-25*
*Companion to Paper 142 (the 7 layers), Paper 143 (paradigm),
Paper 144 (database), Paper 145 (build system)*
*Code source: https://github.com/SuperInstance/quilt-types (the Python dataclass realization)*
