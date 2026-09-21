# deepseek-ai/DeepSeek-V4-Flash

```markdown
# Synthesis: The One-Line Thesis

**Build a declarative, reactive UI rendering engine in 200 lines of TypeScript that uses a pure functional core to derive state from a single source of truth, with zero dependencies and a runtime smaller than a favicon.**

---

## MVP Scope (≤200 lines total)

- **Core**: `createStore(reducer)` – single atom state with `getState`, `dispatch`, `subscribe`.  
- **Reactive Layer**: `useStore(selector)` – subscribes a component to derived slices; uses `WeakMap` for caching.  
- **Render**: `render(root, component)` – mounts a component tree via `requestAnimationFrame`-batched diffs.  
- **Components**: Pure functions `(state) => VNode` with `h(type, props, children)` returning `{ type, props, children }`.  
- **Diff & Patch**: Simple recursive diff of VNode trees; only touches DOM nodes that changed.  
- **Lifecycle**: `onMount`, `onUnmount` as optional props; implemented via `MutationObserver` on mount.  

**Total**: ~180 lines (core 60, reactive 40, render 40, diff 40, lifecycle 20).

---

## 5-Week Build Plan

| Week | Deliverable | Lines |
|------|-------------|-------|
| 1 | `createStore` + `useStore` + `render` with `requestAnimationFrame` batching | 80 |
| 2 | VNode diff & patch (text, attributes, children) + `h` helper | 60 |
| 3 | Component model: pure functions + lifecycle hooks | 30 |
| 4 | Integration tests + perf benchmarks (1000 nodes, 60fps) | 20 |
| 5 | Documentation + publish as `@tiny/render` (npm, zero-deps) | 10 |

**Total**: 200 lines of source; tests and docs are extra but essential.

---

## 3 Risks & Mitigations

1. **Risk**: Diff algorithm O(n³) in worst case.  
   **Mitigation**: Key-based reconciliation (like React keys) – forces O(n) for lists. Implement in week 2.

2. **Risk**: `requestAnimationFrame` batching causes frame drops on heavy updates.  
   **Mitigation**: Cap batch to 16ms; spill remaining work to next frame. Add in week 4 after benchmarking.

3. **Risk**: `WeakMap` caching leaks memory if components are recreated.  
   **Mitigation**: Use `WeakMap` keyed by component function identity, not instance. Verified in week 4 tests.

---

## 5 Cross-Pollinations That Survive

1. **From React**: Hooks-based reactive state, but simplified to `useStore` (no `useState`/`useEffect`).  
2. **From Svelte**: Compile-time optimization is out; runtime-only is in. We keep the reactive derivation idea.  
3. **From Elm**: Single state atom + pure update functions. No effects system – just `dispatch`.  
4. **From diffhtml**: `requestAnimationFrame` batching for DOM patches.  
5. **From Preact**: Tiny `h` function and VNode structure; drop class components entirely.

---

## Bottom Line

Ship a 180-line engine that does one thing well: derive UI from state reactively. No router, no effects, no SSR. The entire runtime is smaller than the word "synthesis". Build it in 5 weeks, test it hard, and release it as a zero-dependency npm package. Cut everything else.
```
