# Codeme CLI Engines Reference

The Codeme platform is organized into four verification engines, each running as an independent executable or orchestrated via the toolchain manager.

---

## 1. `codeme-syntax`

Parses source code into concrete syntax trees (CSTs) and abstract syntax trees (ASTs), detects grammatical and structural syntax violations, and applies surgical, deterministic minimal repairs.

### Why No Host Compiler Toolchain? (The Architectural Advantage)
Unlike traditional compilers that require full toolchain suites (`rustc`, `go`, `javac`, `kotlinc`, `clang++`) installed on the host machine, `codeme-syntax` embeds modern Tree-sitter bindings running in-process via C/ABI3:
1. **Zero Toolchain Bloat:** No need to install 15–20 GB of SDKs, JDKs, build systems, or cross-compilation environments to check or repair syntax.
2. **Pure Grammar Validation:** Native compilers halt immediately when `#include` headers, Maven dependencies, or Cargo crates are missing. `codeme-syntax` checks syntax in pure syntactic isolation, preventing build/linkage errors from masking syntax bugs.
3. **In-Process Millisecond Speed:** Tree-sitter parses in 1–5ms in-process, bypassing the high latency of compiler process invocations (e.g. JVM startup times of 500ms–2s).
4. **GLR Error Recovery:** Generates concrete syntax trees with `ERROR` and `MISSING` nodes that isolate broken tokens without cascading hundreds of false-positive compiler errors.
5. **Universal Rollback Guarantee:** If a broken file cannot be deterministically repaired, all changes are rolled back to preserve the working tree.

### Supported Languages
- **Rust (`.rs`)**: Missing semicolons, unclosed delimiters, macro syntax validation.
- **Go (`.go`)**: Unclosed braces, malformed function headers, package declarations.
- **C++ (`.cpp`, `.cc`, `.cxx`, `.hpp`, `.h`)**: Semicolon insertions, namespace/class brace balancing.
- **Java (`.java`)**: Class block balancing, statement terminators, parameter delimiters.
- **Kotlin (`.kt`, `.kts`)**: Lambda and function call delimiter tracking.
- **Ruby (`.rb`)**: Missing `end` keywords, block delimiters, string interpolation recovery.
- **Python (`.py`)**: Missing colons, unclosed brackets/quotes, indentation anomalies.
- **JavaScript & TypeScript (`.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs`)**: Missing braces, template literals, unclosed quotes.
- **Swift (`.swift`)**: Balanced delimiter validation, structural checking.

### Usage
```bash
# Check syntax silently across repository root (0 bytes emitted on exit 0)
codeme-syntax run --repo .

# Verify a single file in any supported language
codeme-syntax run --file src/engine.rs

# Deterministically apply minimal repairs with rollback protection
codeme-syntax run --repo . --fix

# Output verbose diagnostics for debugging
codeme-syntax run --file Broken.java -v
```

---

## 2. `codeme-quality`

Calculates code quality metrics, cyclomatic complexity, nesting depth, and enforces architectural boundaries.

### Capabilities
- **Cyclomatic Complexity**: Measures control flow branches per function. Default threshold: 10.
- **Nesting Depth**: Blocks excessively nested loops and conditionals. Default threshold: 4.
- **DDD Layer Boundaries**: Enforces dependency rules (e.g. `domain` cannot import `infrastructure`).
- **Unused Import Removal**: Strips unreferenced import statements cleanly during `--fix`.

### Usage
```bash
# Audit quality with custom thresholds
codeme-quality --target src/ --max-complexity 12 --max-nesting 4

# Check architectural boundary rules
codeme-quality --target src/ --ddd-rules config/architecture-rules.json

# Auto-fix quality violations (e.g. remove unused imports, trim trailing whitespace)
codeme-quality --target src/ --fix
```

---

## 3. `codeme-verify`

Discovers and executes builds and test suites across multiple language ecosystems, with automatic targeted test selection and mechanical repair.

### Supported Test Runners
- **Python**: `pytest`, `unittest`
- **TypeScript / JavaScript**: `vitest`, `jest`, `npm test`
- **Swift**: `swift test`

### Usage
```bash
# Automatic discovery and targeted execution
codeme-verify --target .

# Run specific targeted test file or filter
codeme-verify --target . --filter test_billing

# Auto-repair missing fixtures or unresolved import paths
codeme-verify --target . --fix
```

---

## 4. `codeme-invariant`

Enforces immutable system invariants, preventing regressions that standard tests fail to catch.

### Protected Invariants
1. **Database Migration Safety**: Enforces non-destructive schema changes (e.g. rejects `DROP TABLE` or `DROP COLUMN` in production migrations).
2. **State Machine Transitions**: Validates entity state machine definitions against invalid transitions.
3. **Golden State Baselines**: Cryptographically compares directory snapshots to golden hashes to prevent silent modification of baselines without explicit promotion.

### Usage
```bash
# Verify all invariants
codeme-invariant --target .

# Verify database migrations specifically
codeme-invariant --target migrations/ --guard database

# Promote a new golden-state baseline (requires explicit flag)
codeme-invariant --target tests/golden --promote
```

---

## Output Formats and Exit Contracts

All four engines support three output modes:
- `--format text` (default): Minimal human-readable diagnostics when failures occur; zero output on success.
- `--format json`: Structured JSON diagnostic objects conforming to `diagnostic-contract.v1.json`.
- `--format sarif`: OASIS Standard SARIF v2.1.0 for IDE and GitHub Security tab integration.

### Universal Silent-Success Contract:
- Exit Code `0`: Execution succeeded with zero unresolved violations. Exactly 0 bytes emitted to stdout and stderr.
- Exit Code `1`: Unresolved violations detected. Diagnostics written to stdout/stderr.
- Exit Code `2`: Fatal configuration or runtime error.
