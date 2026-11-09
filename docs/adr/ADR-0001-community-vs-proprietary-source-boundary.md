# ADR-0001: Separation of Community (Open Source) and Commercial (Proprietary) Source

## Status
Accepted

## Context
Codeme serves both open-source developers through standard linting, syntax repair, and build checks, and commercial organizations needing advanced invariant verification, database migration guards, state-machine validation, audit trails, and multi-agent concurrency.
There is a potential conflict between providing genuine open-source capabilities and protecting proprietary commercial innovations.

## Decision
1. We separate the codebase across distinct repositories:
   - `codeme-community` is strictly open-source (Apache-2.0). It provides fully functional `codeme-syntax`, `codeme-quality`, `codeme-verify`, and basic invariant checks. Community features are never intentionally crippled or gated behind artificial paywalls.
   - `codeme-core` and `codeme-commercial` are proprietary. They implement advanced database migration guards, golden-state promotions, state-machine invariants, transaction sandboxing, audit aggregation, and Ed25519 cryptographic licensing.
2. The verification engine uses a plugin/adapter boundary where commercial extensions hook into the core runner without modifying the open-source CLI contract.
3. No proprietary code or customer credentials may ever be committed to `codeme-community`, `codeme-oem-sdk`, or any public repository.

## Consequences
- Open-source users get deterministic, production-grade tools.
- Commercial assets remain protected in private repositories.
- Clear licensing and distribution compliance is maintained.
