# ADR-0003: Ed25519 Cryptographic Licensing & Offline Entitlement Model

## Status
Accepted

## Context
Codeme must support:
- Pro and Team developers operating offline (up to 30 days without connectivity).
- Enterprise customers operating in strictly air-gapped secure enclaves with non-expiring or long-duration certificates.
- Hardware binding that does not break Docker, cloud VMs, or normal hardware replacement.
- Zero data exfiltration (no source code, prompts, or proprietary data transmitted during licensing).

## Decision
1. Licensing is implemented using standard Ed25519 digital signatures over canonical JSON payloads (RFC 8785).
2. Public verification keys are bundled with Codeme binaries. Multiple key IDs (`kid`) are supported to permit zero-downtime key rotation.
3. Pro and Team editions use signed offline capability tickets valid for 30 days from issuance or renewal. When network connectivity is available, the CLI may renew tickets silently in the background. In explicit offline mode (`--offline`), all network calls are suppressed.
4. Enterprise licenses support non-expiring or custom-duration capability certificates verifiable completely offline without network endpoints.
5. Team seat allocation defaults to named developers. Device binding uses privacy-preserving, container-safe identifiers (hashing non-sensitive system attributes with salt) without rigid CPUID/MAC locks that break CI or Docker.

## Consequences
- 100% deterministic, offline-capable verification.
- Tamper-resistant cryptographic integrity.
- Zero internet dependency for Enterprise enclaves.
