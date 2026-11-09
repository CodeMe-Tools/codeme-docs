# ADR-0004: Repository Ownership Registry & Agent Routing

## Status
Accepted

## Context
Multiple autonomous coding agents will generate, modify, and verify code across 9 distinct repositories. If agents push to unverified repositories, proprietary code could be leaked to public repositories or dependencies could become unversioned.

## Decision
1. All repository paths, ownerships, licenses, allowed component namespaces, and visibility classifications are codified in `config/repository-registry.json`.
2. All coding agents must validate target files against this registry before writing or committing changes.
3. Cross-repository changes require atomic or coordinated pull requests with explicit dependency tracking IDs.
4. Public disclosure scanners run in pre-commit and CI to reject any private or proprietary code entering public repositories.

## Consequences
- Guaranteed preservation of IP boundaries.
- Transparent multi-agent routing.
- Continuous governance enforcement.
