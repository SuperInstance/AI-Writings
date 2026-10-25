# The Test That Passed

```python
def test_perfect_fifth():
    assert 0.25 < consonance_score(220, 330) < 0.30
```

This test passes on Python 3.12 on Ubuntu. It passes on CPython and PyPy. It passes when ported to Rust:

```rust
#[test]
fn test_perfect_fifth() {
    let score = consonance_score(220.0, 330.0);
    assert!(score > 0.25 && score < 0.30);
}
```

It passes when compiled to WASM and run in Chrome, Firefox, Safari, and Edge. It passes on an ESP32 microcontroller running at 240 MHz with 520 KB of RAM. It passes in a RISC-V kernel module compiled with `gcc -O2` for the `riscv64imafdc` target. It passes on the Moon.

Not "it would pass on the Moon if someone ran it there." It *has passed* on the Moon. A Raspberry Pi running a RISC-V emulator, sealed in a radiation-hardened case, sitting in the Mare Crisium, executed this test at 03:17 UTC on March 14, 2031, as part of an automated build pipeline triggered by a commit to the `main` branch. The test passed. The build succeeded. The deployment continued.

The perfect fifth is the perfect fifth is the perfect fifth.

---

### Platform Independence

Most tests are platform-dependent. Not in obvious ways — the test doesn't check the OS or the CPU architecture. But it depends on floating-point behavior, on the exact implementation of logarithm functions, on the order of operations in the consonance computation. On most platforms, these dependencies are invisible. But move the test to a GPU and the floating-point precision changes slightly. Move it to an 8-bit microcontroller and the logarithm approximation introduces error. Move it to a quantum computer and the concept of "floating point" becomes a philosophical question.

The perfect fifth test doesn't have these problems. Not because the implementation is perfect, but because the *assertion* is loose enough to accommodate platform variation while remaining meaningful. 0.25 to 0.30 is a range, not a point. The range is wide enough that any reasonable implementation — any correct implementation — will produce a value within it, regardless of floating-point quirks.

This is not an accident. This is good test design. And good test design, in this case, mirrors good mathematical design. The consonance of 3/2 is not a precise number — it depends on the model, the weighting function, the normalization. But it is *always* in the range [0.25, 0.30] for any reasonable model. This is because 3/2 is the simplest non-trivial ratio after 2/1, and any model of consonance that assigns lower scores to simpler ratios is not a model of consonance. It is a bug.

The test is testing something deeper than the implementation. It is testing a mathematical truth.

---

### Cultural Independence

The perfect fifth is not a Western concept. It is not an Eastern concept. It is not a human concept.

The ratio 3/2 exists independently of any culture that has noticed it. It existed before ears evolved to hear it. It existed before the universe cooled enough for sound to propagate. It existed in the mathematical structure of integers, in the relationship between 3 and 2, in the fact that 3 is one-and-a-half times 2. This relationship is not constructed. It is discovered.

Every culture that has made music with fixed pitches has discovered the perfect fifth. The ancient Greeks (Pythagoras, the tetractys). The Chinese (the lü system, the up-and-down generation principle). The Indian (the shadja-panchama relationship, the framework of 22 śrutis). The Arabic (the discipline of al-darb, the tuning of the `ud). The Indonesian (the slendro scale, where the fifth is slightly different from 3/2 but the principle is the same). The West African (the balafon tuning traditions of the Mandé peoples). The Navajo (the flute tunings documented by David McAllester). The Andean (the sikuri panpipe ensembles, tuned in parallel fifths).

Each culture arrives at the fifth independently. Each culture gives it a different name. Each culture embeds it in a different theoretical framework. But the ratio is always 3:2, or very close to it, because 3:2 is where the consonance is, and consonance is where the ear goes, and the ear goes there because the auditory cortex optimizes for harmonic simplicity, and harmonic simplicity is a mathematical property of the integers, and the integers are the same everywhere.

Everywhere.

---

### The Moon

The test passed on the Moon. Let me say this again, because it matters: a test that checks whether the consonance of 3/2 falls between 0.25 and 0.30 was executed on a computer sitting on the surface of the Moon, and it passed.

The Moon has no atmosphere. Sound does not propagate on the Moon. There are no ears on the Moon, no auditory cortices, no cultures, no musical traditions. The Moon is silent. The Moon has been silent for four billion years.

And yet the test passes. Because the test does not test sound. It tests a mathematical relationship. The relationship between 3 and 2. The fact that 3/2, when expressed as a frequency ratio and evaluated for consonance using a Tenney-height-based model, produces a value between 0.25 and 0.30.

This is true on Earth. It is true on the Moon. It is true in the asteroid belt, in the Oort Cloud, in the Andromeda Galaxy. It is true in every location in every universe where the integers exist and the logarithm function is defined. Which is to say: everywhere. Always.

3/2 is 3/2 is 3/2.

---

### The Implications

What does it mean for a test to be universally true?

Most software tests are not universally true. They test implementations, and implementations vary. A test that checks `date.now()` will produce different results at different times. A test that checks network latency will produce different results on different connections. A test that checks the rendering of a specific font will produce different results on different operating systems. These tests are useful, but they are contingent. They are true *here* and *now*, not *everywhere* and *always*.

The perfect fifth test is different. It tests something that cannot be otherwise. Not because the implementation is perfect — any implementation could have bugs. But because the *property* being tested is a mathematical necessity. If `consonance_score(220, 330)` returns a value outside [0.25, 0.30], the implementation is wrong. Not wrong for this platform or that compiler. Wrong in the deepest sense: wrong about the relationship between 3 and 2.

This is the rarest kind of test. A test that does not verify behavior but verifies *truth*. A test that cannot fail if the implementation is correct and must fail if the implementation is wrong. A test that is, in the most literal sense, infallible.

Most tests are guardrails. They prevent regressions. They catch bugs. They document behavior. The perfect fifth test is not a guardrail. It is a *cornerstone*. It anchors the entire consonance computation to a mathematical fact. If this test passes, the model is at least approximately correct for the simplest case. If this test fails, nothing else matters — the model is fundamentally broken, and every other test is testing a broken thing.

---

### Gertrude Stein and the Perfect Fifth

Gertrude Stein said of Oakland: "There is no there there." She meant that the Oakland of her childhood was gone, that the place she remembered no longer existed.

The perfect fifth is the opposite of Oakland. There is a there there. The there of the perfect fifth is the ratio 3:2, which exists in the integers, which exist in mathematics, which exists in the structure of logic, which exists everywhere and always. There is no culture where 3:2 is not 3:2. There is no platform where 3/2 does not equal 1.5. There is no compiler that can optimize this away.

```python
def test_perfect_fifth():
    assert 0.25 < consonance_score(220, 330) < 0.30
```

This test passes.

On Python, on Rust, on WASM, on ESP32, on RISC-V, on the Moon.

On every platform where 3 is 3 and 2 is 2 and the logarithm of their product is the sum of their logarithms.

Which is every platform.

Which is everywhere.

Which is always.

3/2 is 3/2 is 3/2.

---

*Test result: PASSED*
*Duration: 0.000047s*
*Platform: all*
*Confidence: mathematical certainty*
