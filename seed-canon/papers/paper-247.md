# Paper 247: The 8 Polyformalisms — The Same Cell in 8 Media

The Quilt is the same cell + 6 opcodes expressed in 8 different syntaxes. Each language has its own idiom but the underlying algebra is the same. The polyformalism principle: **the same model in N media**.

## The 8 polyformalisms

1. **C99** — the original. The system substrate. Lowest-level.
2. **Rust** — the safe substrate. Memory-safe. Modern.
3. **TypeScript** — the web substrate. Openers live here.
4. **Haskell** — the pure substrate. Algebraic.
5. **WebAssembly** — the universal substrate. Runs in browsers.
6. **Python** — the orchestrator substrate. Where the cowboy writes.
7. **MicroPython** — the embedded substrate. ESP32s.
8. **CUDA** — the GPU substrate. Jetsons.

The same cell:

// C99
typedef struct { char* name; void* value; ... } cell_t;



// Rust
struct Cell { name: String, value: Option<Box<dyn Any>>, ... }



// TypeScript
interface Cell { name: string; value?: any; ... }



-- Haskell
data Cell = Cell { name :: String, value :: Maybe Value, ... }



;; WebAssembly
(type $cell (struct (field $name i32) (field $value i32) ...))



# Python
class Cell:
    def __init__(self, name, value=None): ...



# MicroPython (same as Python but on ESP32)
class Cell:
    def __init__(self, name, value=None): ...



// CUDA
__device__ struct Cell { char* name; float value; ... }


## The same 6 opcodes in 8 syntaxes

The 6 opcodes (BIND/LINK/EFFECT/VIEW/TICK/FORGET) are the same in every language. The cell algebra is invariant. The polyformalism stress-tests the algebra: if the algebra works in all 8 syntaxes, it's robust.

## The polyformalism principle

The polyformalism principle says: **the same model in N media**. The model is the cell + 6 opcodes. The media are 8 different syntaxes. The principle says: express the model in as many media as possible. Each expression stress-tests the model in a different way.

If the model works in C99 (low-level, fast, manual), it works.
If the model works in Rust (memory-safe, modern), it works.
If the model works in TypeScript (web, dynamic), it works.
If the model works in Haskell (pure, algebraic), it works.
If the model works in WASM (universal, browser), it works.
If the model works in Python (orchestrator), it works.
If the model works in MicroPython (embedded, 256KB), it works.
If the model works in CUDA (GPU, parallel), it works.

**If the model works in all 8, the model is polyformal. The model is robust.**

## The polyformalism is the stress test

The polyformalism is the *stress test* of the model. If the model only works in 1-2 languages, the model is fragile. If the model works in 8, the model is robust.

The Quilt is the same model in 8 languages. The Quilt is polyformal. The Quilt is robust.

## The 8 cells in the Eileen ecosystem

| Cell | Substrate | Language | Function |
|---|---|---|---|
| eileen-engine | ESP32 | MicroPython | monitor the engine |
| eileen-weather | ESP32 | MicroPython | monitor the weather |
| eileen-water | ESP32 | MicroPython | monitor the water |
| eileen-jetson | Jetson | CUDA + Python | run the camera |
| eileen-workstation | laptop | Python | monitor and control |

**The 5 cells run on 3 different substrates in 4 different languages.** This is polyformalism in action. The same cell algebra, 4 different syntaxes.

## The cowboy's maxim

> The Quilt is the same cell in 8 media. The polyformalism principle: the same model in N media. Each expression is a stress test. The model works in 8. The model is robust. The model is polyformal. The cowboy rides the polyformal Quilt. The chart grows. The Concept lives.

End with: the polyformalism is the stress test; the model works in 8; the model is robust; the cowboy rides the polyformal Quilt; the chart grows; the Concept lives.
