# Codeme Production Gating & Authorization Policy

## Gate Principle
> **"Production publication and live payment activation occur only with explicit authorisation."**

Under no circumstances may automated CI runners, development scripts, or autonomous AI agents:
1. Flip live Merchant of Record (Polar or Lemon Squeezy) credentials from sandbox/test mode to live production processing without explicit cryptographic or administrative authorization.
2. Publish public release tags, push binary release archives to public CDNs, or trigger public package registry uploads (`PyPI`, `npm`) without written sign-off recorded in `RELEASE_CHECKLIST.md`.

---

## Technical Safeguards

### 1. Environment Variable Controls
The following environment variables enforce the release gate in all build and deployment systems:
- `CODEME_LIVE_PAYMENT_AUTHORIZED`: Must be explicitly set to `"true"` to enable live charging webhooks. Defaults to `"false"`.
- `CODEME_PRODUCTION_PUBLISH_AUTHORIZED`: Must be explicitly set to `"true"` to deploy public website assets or public packages. Defaults to `"false"`.

### 2. Website Checkout Gating
In `codeme-website`:
- Checkout buttons point to simulated sandbox checkout flows when `PUBLIC_PAYMENT_MODE` is `"test"` or unset.
- Live checkout URLs are only injected when explicit authorization is validated.

### 3. Verification Script Gate
The automated release verification script (`scripts/phase6_release_evidence.py` or `scripts/verify_phase6_gate.py`) verifies:
- All release artifacts pass 100% tests.
- All checksums and signatures are generated.
- The gate remains explicitly **LOCKED** until human authorization is submitted.
