# Codeme Commercial Release Guide

This document defines the standard procedure for assembling, signing, verifying, and publishing commercial release distributions of Codeme.

---

## Release Pipeline Stages

```
1. Version & Manifest Freeze
   └── Validate manifests/product-manifest.v1.json
       ├── Edition pricing (£19/mo, £190/yr Pro; £15/mo, £150/yr Team)
       └── Active Ed25519 root verification keys

2. Multi-Repo Boundary & Secret Audit
   └── Run PublicRepositoryAuditor
       ├── 0 private keys in public repos
       ├── 0 proprietary imports in public packages
       └── All LICENSE and THIRD_PARTY_NOTICES.md present

3. Multi-Target Distribution Packaging
   └── Run codeme-package build --target all --version <version>
       ├── macOS (arm64, x64) [.tar.gz]
       ├── Linux (x64, arm64) [.tar.gz]
       └── Windows (x64) [.zip]

4. Cryptographic Signing
   └── Sign packages using Ed25519 Release Key:
       ├── codeme-package sign <package>
       └── Produces <package>.sig and signed release-manifest.json

5. Clean-Machine Acceptance Verification
   └── Run codeme-package accept --package <archive>
       ├── Sandbox extraction
       ├── 4-engine silent pass
       └── Offline ticket activation

6. OEM SDK Distribution Validation
   └── Verify codeme-oem-sdk package and contract adherence

7. Production Publication Gate Verification
   └── Ensure PAYMENT_GATE_LIVE=false and PRODUCTION_DEPLOY_APPROVED=false
       └── Require explicit manual sign-off in RELEASE_CHECKLIST.md
```

---

## Cryptographic Artifact Signing Command
```bash
# Build native archives
codeme-package build --target all --version 0.1.0 --outdir dist

# Sign release archive using Ed25519 release key
codeme-package sign --package dist/codeme-0.1.0-macos-arm64.tar.gz --key-id codeme-root-2026-v1

# Verify signature
codeme-package verify-signature --package dist/codeme-0.1.0-macos-arm64.tar.gz
```
