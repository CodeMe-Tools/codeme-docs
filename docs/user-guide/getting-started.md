# Codeme User Guide: Getting Started

Welcome to **Codeme** — the autonomous code quality, verification, and invariant platform.

## Overview
Codeme provides four deterministic CLI engines designed for both human software engineers and autonomous AI coding agents:
1. `codeme-syntax`: Syntactic structure parsing and deterministic token repair.
2. `codeme-quality`: Cyclomatic complexity, nesting depth, and clean-architecture boundary auditing.
3. `codeme-verify`: Targeted build and test runner with automatic environment discovery.
4. `codeme-invariant`: Database migration guards, state machine transition validators, and golden snapshot verifiers.

All engines adhere strictly to the **Universal Silent-Success Execution Contract**:
- On clean execution with zero violations, the process exits with code `0` and writes **0 bytes** to standard output and standard error.
- On unresolved violations, the process exits with a non-zero exit code and outputs structured diagnostics.

---

## Installation

### macOS (Apple Silicon / Intel)
```bash
curl -fsSL https://downloads.codeme.tools/install.sh | sh
# Or unpack directly:
tar -xzf codeme-0.1.0-macos-arm64.tar.gz -C ~/.codeme
export PATH="$HOME/.codeme/bin:$PATH"
```

### Linux (Ubuntu, Debian, Alpine/musl, RHEL)
```bash
tar -xzf codeme-0.1.0-linux-x64.tar.gz -C ~/.codeme
export PATH="$HOME/.codeme/bin:$PATH"
```

### Windows (PowerShell / cmd)
```powershell
Expand-Archive -Path codeme-0.1.0-windows-x64.zip -DestinationPath "$env:LOCALAPPDATA\Codeme"
$env:PATH += ";$env:LOCALAPPDATA\Codeme\bin"
```

---

## Quickstart Verification

Check that your installation is functional:
```bash
codeme-toolchain --version
codeme-syntax --help
codeme-quality --help
codeme-verify --help
codeme-invariant --help
```

To run a verification pass across your current directory:
```bash
# 1. Check syntax
codeme-syntax --target src/

# 2. Check quality & complexity limits
codeme-quality --target src/ --max-complexity 10

# 3. Discover and run test suite
codeme-verify --target .

# 4. Enforce structural invariants
codeme-invariant --target .
```
If all checks pass, all four commands exit silently (`0` bytes output, exit code `0`).
