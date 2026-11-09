# Specification: Universal Silent-Success Execution Contract

## Standard Output Rules

### Routine Success
- Process Exit Code: `0`
- `stdout`: Exactly 0 bytes (empty)
- `stderr`: Exactly 0 bytes (empty)

### Violation / Failure
- Process Exit Code: Non-zero (`1` for verification violations, `2` for configuration errors, `3` for licensing blocks, `4` for unrecoverable errors)
- `stderr`: Structured diagnostic message containing:
  - Error Code (`CDM-xxx`)
  - File path and Line/Column coordinates
  - Diagnostic description
  - Actionable remediation advice

### Verbose Mode (`-v`, `--verbose`)
- Output allowed on `stdout` detailing timing, rules executed, files examined, and repairs performed.

### Machine-Readable Outputs
- `--format json`: Emits RFC-compliant JSON matching `CodemeDiagnosticContract`.
- `--format sarif`: Emits standard SARIF log for IDE problems view.
