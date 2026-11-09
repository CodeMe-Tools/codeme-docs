# ADR-0009: Commercial Release Preparation, Signed Distribution, and Production Publication Gate

## Status
Accepted

## Context
Phase 6 of the Codeme platform directive mandates commercial release preparation across all 9 repositories.
Key requirements include:
1. Finalising comprehensive customer documentation across Community, Pro, Team, Enterprise, and OEM editions.
2. Finalising and cryptographically validating supported editions, pricing tiers, and entitlement sets.
3. Validating the end-to-end subscription, renewal, seat allocation, and VAT billing lifecycle.
4. Auditing all public repositories to guarantee zero leakage of proprietary intellectual property, secrets, or internal keys.
5. Validating production website configuration, ensuring live payment gateways remain strictly gated.
6. Generating cryptographically signed native distribution packages (Ed25519 archive signatures and signed release manifests).
7. Validating the versioned OEM SDK distribution package for zero-CLI programmatic embedding.
8. Producing cryptographic release evidence and a formal commercial release approval checklist.
9. Enforcing the mandatory master gate: "Production publication and live payment activation occur only with explicit authorisation."

## Decision
1. **Customer Documentation Standard:**
   - Establish comprehensive user guides in `codeme-docs/docs/user-guide/` covering installation, CLI engines, licensing, team seats, enterprise air-gap mode, and OEM embedding.
   - Maintain operational documentation in `codeme-docs/docs/operations/` detailing the release process and gating controls.
   - Synchronize documentation and verify pricing accuracy against `product-manifest.v1.json` via `codeme-docs-sync`.

2. **Supported Editions Validation:**
   - Implement automated edition validation verifying canonical pricing (£19/mo, £190/yr Pro; £15/mo, £150/yr min 5 seats Team), offline policies, and entitlement definitions across manifests, billing engines, and website models.

3. **Commercial Subscription & Renewal Lifecycle:**
   - Implement `SubscriptionLifecycleVerifier` validating Polar and Lemon Squeezy webhook ingestion, Ed25519 license issuance, local 30-day ticket activation, ticket re-signing and renewal, team seat allocation, and UK VAT invoice calculation.

4. **Public Repository Boundary Audit:**
   - Deploy `PublicRepositoryAuditor` to continuously verify all 6 public repositories (`codeme-community`, `codeme-oem-sdk`, `codeme-docs`, `codeme-agent-skills`, `codeme-examples`, `.github`).
   - Block any presence of private keys, internal credentials, proprietary imports (`codeme.commercial`, `codeme.billing`), or unapproved copyleft licenses.

5. **Production Website & Payment Isolation Gate:**
   - Enforce explicit environment gating (`PAYMENT_GATE_LIVE=false`, `PRODUCTION_DEPLOY_APPROVED=false`) in `codeme-website`.
   - Prevent inadvertent live payment activation or production deployments during CI or local builds.

6. **Cryptographically Signed Installers:**
   - Enhance `codeme-package` with Ed25519 signing (`sign`) and verification (`verify-signature`).
   - Produce SHA-256 checksums and Ed25519 digital signatures (`.sig`) for all native distribution packages and `release-manifest.json`.

7. **OEM Distribution Package Validation:**
   - Implement `OEMPackageValidator` verifying standalone distribution, JSON schema contracts (`invocation-contract.v1.json`, `diagnostic-contract.v1.json`), token metric accounting, and zero proprietary runtime dependencies.

8. **Release Evidence & Master Gate Enforcement:**
   - Generate `release-evidence.v0.1.0.json` capturing git commit hashes across all 9 repositories, test results, package checksums, and signature verifications.
   - Maintain `RELEASE_CHECKLIST.md` requiring explicit sign-off before production publication or live payment gateway activation.

## Consequences
- Complete commercial release readiness across all 9 repositories.
- Tamper-proof, cryptographically signed installer bundles with verifiable provenance.
- Zero risk of accidental proprietary IP disclosure or premature live billing activation.
