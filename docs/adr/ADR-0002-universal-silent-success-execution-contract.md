# ADR-0002: Universal Silent-Success Execution Contract

## Status
Accepted

## Context
Autonomous AI coding agents and automated CI pipelines run verification loops frequently. Verbose success messages consume valuable token context, clutter agent working memory, and obscure actual errors.

## Decision
1. All routine successful executions of any Codeme CLI (`codeme-syntax`, `codeme-quality`, `codeme-verify`, `codeme-invariant`, `codeme-toolchain`) must exit with status code `0` and emit **zero bytes** on both `stdout` and `stderr`.
2. Any failure must exit with a non-zero exit code (e.g., 1 for violations, 2 for configuration errors, 3 for licensing blocks) and emit actionable, deterministic diagnostics to `stderr` or formatted JSON when requested.
3. Verbose mode (`-v`, `--verbose`) is explicitly supported for human debugging and detailed trace collection.
4. Structured outputs (`--format json`, `--format sarif`) are supported for IDEs and automated aggregators without violating the default silent contract.

## Consequences
- AI agents execute verifications without token consumption on success.
- Zero false positives in automated scripts.
- Unambiguous exit codes for CI/CD gates.
