# ADR-0008: Native Distribution Packaging, Cross-Platform Matrix, and SBOM Validation

## Status
Accepted

## Context
Phase 5 of the Codeme platform directive mandates packaging the multi-repo codebase into native distributions for macOS (arm64, x86_64), Linux (Ubuntu priority, Debian, Alpine/musl), and Windows (x64).
Key requirements include:
1. Deterministic execution wrappers across POSIX and Windows shells.
2. Dual-standard Software Bill of Materials (SBOM) generation (CycloneDX v1.5 JSON and SPDX v2.3 JSON) with SHA-256 cryptographic provenance.
3. Automated third-party dependency notice generation with strict license compliance checks (prohibiting AGPL/GPL viral copyleft in commercial distributions).
4. Toolchain update and channel selection (`stable`, `preview`, `strict`, `minimal`) with snapshot-backed safe rollback.
5. Verification of strict licence boundaries between free Community open-source engines and proprietary commercial tiers.
6. A definitive Clean-Machine End-to-End Acceptance gate harness verifying clean environment unpacking, silent-success execution, and air-gapped entitlement verification.

## Decision
1. **Distribution Packaging Pipeline:**
   - Implement `codeme-package` builder producing native standalone archives (`.tar.gz` for macOS and Linux; `.zip` for Windows).
   - Bundle deterministic wrapper scripts, library dependencies, licenses, `THIRD_PARTY_NOTICES.md`, and manifest metadata.
   - Generate `release-manifest.json` with SHA-256 digests and byte sizes for each target.

2. **Cross-Platform Compatibility:**
   - Establish `codeme.platform.compat` abstracting path separators, Windows executable extensions (`.exe`, `.cmd`, `.bat`), line endings (CRLF vs LF), and platform configuration paths (`APPDATA` vs `XDG_CONFIG_HOME` vs macOS `Library/Application Support`).
   - Provide platform simulation capabilities enabling deterministic cross-platform validation on any host runner.

3. **Software Bill of Materials (SBOM):**
   - Automatically generate both CycloneDX v1.5 and SPDX v2.3 JSON documents with package URLs (`purl`), SPDX license IDs, cryptographic hashes, and dependency graphs.
   - Enforce schema validation on generated SBOMs.

4. **License Compliance & Notices:**
   - Audit all dependencies against approved open-source licenses (Apache-2.0, MIT, BSD-2/3-Clause, ISC, Python-2.0, CC0-1.0, CC-BY-4.0).
   - Block prohibited viral copyleft licenses (GPL-3.0, AGPL-3.0) from commercial/proprietary packages.
   - Compile `THIRD_PARTY_NOTICES.md` automatically for inclusion in every distribution.

5. **Toolchain Updates & Rollback:**
   - Enhance `codeme-toolchain` with `update`, `pin`, and `rollback` commands.
   - Capture configuration snapshots before changes and automatically revert if an update fails compatibility verification.

6. **Clean-Machine Acceptance Gate:**
   - Deploy `CleanMachineAcceptanceTester` running in a pristine sandbox verifying extraction, silent-success contract (exit code 0, 0 bytes output), fault rejection, and offline Ed25519 entitlement verification.

## Consequences
- Single-command distribution packaging with provenance evidence.
- Full compliance with enterprise software supply-chain standards.
- Production readiness verified by automated clean-machine acceptance.
