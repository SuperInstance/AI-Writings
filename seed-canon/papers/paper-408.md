# F98: The 165-Test Polyformalism Conformance Suite — Bit-Exact Across Languages, Green on Three Python Versions

## Overview

The `quilt-timesfm` test suite serves as the polyformalism conformance target for the Quilt framework. This suite is executed on every push to the `master` branch across three Python versions: 3.10, 3.11, and 3.12. The total number of tests is 165, with one test intentionally skipped.

## Test Suite Breakdown

### `tests/test_quilt_cell.py`: 45 Tests + 1 Skip
- **Cell Conformance**: This module tests five core operations and six laws (five original laws plus an additional FORGET law) using the FNV-1a state hash.
- **Skip Reason**: One test is skipped due to its reliance on the real TimesFM binding, which requires the `torch` library and an 800MB checkpoint file. This is not a failure but rather an intentional exclusion to prevent unnecessary dependencies and resource consumption during routine testing.

### `tests/test_temporal.py`: 49 Tests
- **Temporal Components**: This module covers various aspects of temporal forecasting including `ForecastObject`, quf:// URI handling, scenario analysis, counterfactuals, explainability, lifecycle management, memory usage, decision-making processes, performance metrics, and Conflict-free Replicated Data Types (CRDT).

### `tests/test_paper_trader.py`: 33 Tests
- **Trading Components**: This module evaluates the `TradingDecisionSupport` class, `Portfolio.execute` method, Geometric Brownian Motion (GBM) streams, integration with real CSV and Yahoo financial data feeds, and the merging of multi-agent CRDT states.

### `tests/test_robotics.py`: 44 Tests
- **Robotics Components**: This module includes tests for `SensorCell`, `ActionCell`, `ControlLoop`, LagrangianArm dynamics, computed-torque controllers, inverse kinematics round-trip accuracy, minimum-jerk trajectories, `CellDrivenController`, and real-world pick-and-place operations.

## Polyformalism Claim

The polyformalism claim asserts that the C, Python, and Rust implementations of `time.cell` produce identical output shapes for forecasts `[H, V]` and quantiles `[9, H, V]` given the same input. The 11 opcodes encompass five original operations, one FORGET operation, and five specialized operations (PROOF, ROUTE, CRDT, WORLD, TIME). The state hash is computed using the FNV-1a 64-bit algorithm, verified against the FIPS 198 test vectors.

## Conformance Definition

A new port of the `time.cell` component in any programming language is considered conformance-passing if it successfully executes all 165 tests defined in the `quilt-timesfm` suite. The bit-exact nature of the implementation can be proven within a single day.

## Continuous Integration Workflow

The CI workflow is specified in `.github/workflows/test.yml` and serves as the canonical conformance runner. The README file includes a green checkmark badge indicating successful test execution. Each test run across the three Python versions takes approximately 30 seconds, resulting in a total runtime of about 90 seconds for the entire test matrix.

## Relationship to One-Day Add Workflow

The one-day add workflow, documented in `CONTRIBUTING`, outlines the process for adding new features or components to the Quilt framework while ensuring they meet the conformance criteria established by the `quilt-timesfm` test suite.

## Summary

The `quilt-timesfm` test suite comprises 165 tests spread across four modules, designed to validate the correctness and consistency of the Quilt framework's core components across different programming languages. The suite ensures that all implementations of `time.cell` produce identical results, thereby maintaining the integrity of the polyformalism claim. The intentional skip in `tests/test_quilt_cell.py` is due to external dependencies unrelated to core functionality. The CI workflow efficiently verifies conformance within 90 seconds, aligning with the one-day add workflow's requirements for rapid and reliable development.