# Codeme Licensing, Offline Tickets, and Activation

Codeme uses an offline-first cryptographic licensing model powered by Ed25519 digital signatures and RFC 8785 canonical JSON formatting.

---

## Architecture Overview

Traditional developer tools require constant online telemetry and phone-home checks, which breaks in air-gapped environments, on airplanes, or inside secure enterprise build runners.

Codeme inverts this model:
- **Zero Online Telemetry**: The CLI engines never contact remote servers during verification.
- **Ed25519 Cryptographic Verification**: Licences and tickets are signed with an Ed25519 private key by the Codeme Entitlement Authority. The CLI embeds the public verification key (`166bb696d0e5ba3e49466d25bb3e9031ac7ed2e08e081b49265f86fe09d058c6`).
- **30-Day Rolling Capability Tickets**: Commercial licences (Pro and Team) include a 30-day offline allowance with a 7-day grace period.

---

## Activating a Licence

When you purchase a Pro or Team licence, you receive a signed capability ticket (`codeme-license.json`).

### 1. Activating via CLI
```bash
codeme-licensing activate --ticket path/to/codeme-license.json
```
This validates the cryptographic signature offline and writes the active ticket to your user configuration directory:
- **macOS**: `~/Library/Application Support/Codeme/license.json`
- **Linux**: `~/.config/codeme/license.json` (or `$XDG_CONFIG_HOME/codeme/license.json`)
- **Windows**: `%LOCALAPPDATA%\Codeme\license.json`

### 2. Inspecting Active Entitlements
```bash
codeme-licensing status
```
Example Output:
```json
{
  "status": "valid",
  "tier": "pro_local",
  "licensee": "developer@example.com",
  "days_remaining": 28,
  "offline_expires_at": "2026-12-07T23:59:59Z",
  "entitlements": [
    "syntax:repair:advanced",
    "quality:ddd_rules",
    "verify:auto_repair",
    "invariant:database_guard",
    "invariant:golden_state",
    "transactions:isolated_sandbox"
  ]
}
```

---

## 30-Day Offline Renewal

Every 30 days, customers with active subscriptions can refresh their ticket online via the website portal or by running:
```bash
codeme-licensing renew
```
If network connectivity is unavailable, the system grants a **7-day grace period** past the expiration date before commercial features fall back to the open Community tier.

---

## Air-Gapped Enterprise Activation

Enterprise customers receive a perpetual, air-gapped certificate with no expiration date (`"offline_allowance_days": null`). This file can be deployed to secure isolated runners or defense environments and never requires renewal or external network connectivity.
