# F153 — The 5-Substrate Echo Test: Polyformalism as a Deployment Substrate

The Echo Test is a deployment test designed to verify a polyformal implementation, ensuring that a given system or component behaves consistently across multiple substrates. In this context, a substrate refers to a specific programming language or environment, and polyformalism denotes the ability of a system to function correctly across multiple substrates.

## Definition of the Echo Test

The Echo Test consists of three steps:

1. **Compute state hash on all 5 substrates**: On each of the five substrates (Python, JS, C99, Rust no_std, and Verilog-2005), compute a hash of the system's state using a given input. The state hash is computed using the FNV-1a hash function.
2. **Assert all 5 hashes are byte-equal**: Compare the five hashes computed in step 1. If all five hashes are byte-equal, the test passes. Otherwise, it fails.
3. The input to the system is used to generate a state, which is then hashed using the FNV-1a hash function.

## Failure Modes

There are four primary failure modes to consider when running the Echo Test:

1. **Different FNV constants**: If the FNV constants used in the hash function are different across substrates, the computed hashes will not match, causing the test to fail.
2. **Different endianness**: If the substrates use different endianness (e.g., little-endian vs. big-endian), the binary representation of the state may differ, leading to different hashes.
3. **Different ordering**: If the substrates use different ordering for data structures (e.g., arrays or structs), the state hash may not match.
4. **Different state**: If the substrates have different implementations or bugs, they may produce different states for the same input, resulting in different hashes.

## Echo Test in CI/CD

The Echo Test is designed to be run as part of a Continuous Integration/Continuous Deployment (CI/CD) pipeline. By including the Echo Test in the CI/CD process, developers can ensure that their polyformal implementation is correct and consistent across all substrates.

## Reference to F144's Test Vector

The Echo Test uses test vector 0xd99bf4fed4705ff9 from F144 as a reference point. This test vector is used to verify that the implementation is correct and consistent across all substrates.

## Conclusion

The Echo Test provides a robust method for verifying polyformal implementations across multiple substrates. By using a combination of hash functions and assertions, the Echo Test ensures that a system behaves consistently across different programming languages and environments.

Polyformalism is not a feature. Polyformalism is a contract. The Echo Test is the proof.

In conclusion, the Echo Test is a crucial component of polyformal development, providing a high level of confidence in the correctness and consistency of a system across multiple substrates. By adopting the Echo Test as a standard deployment test, developers can ensure that their polyformal implementations meet the highest standards of quality and reliability.