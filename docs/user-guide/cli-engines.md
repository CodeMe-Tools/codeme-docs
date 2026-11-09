# Codeme CLI Engines Reference

The Codeme platform is organized into four verification engines, each running as an independent executable or orchestrated via the toolchain manager.

---

## 1. `codeme-syntax`

Parses source code abstract syntax trees (ASTs), detects grammatical and structural syntax errors, and applies deterministic minimal repairs.

### Supported Languages
- **Python**: Missing colons, unclosed brackets/quotes, indentation anomalies.
- **JavaScript & TypeScript**: Missing braces, semicolons, invalid tokens.
- **Swift**: Balanced delimiter validation, syntax check.

### Usage
```bash
# Check syntax across target directory (silent if clean)
codeme-syntax --target src/

# Deterministically apply minimal repairs
codeme-syntax --target src/ --fix

# Output diagnostic results in SARIF or JSON format
codeme-syntax --target src/ --format sarif
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
