# Codeme Enterprise Air-Gapped Deployment

The Codeme Enterprise edition is designed for isolated defense environments, financial institutions, and secure on-premise infrastructure where external internet access is prohibited.

---

## Architectural Principles
1. **Zero External Egress**: Enterprise installations require no external network calls, telemetry, or remote licence server handshakes.
2. **Perpetual Cryptographic Certificates**: Licences are issued as tamper-evident RFC 8785 Ed25519 certificates with permanent validity (`"allow_perpetual_certificate": true`).
3. **On-Premise Toolchain Mirrors**: Standalone binaries can be hosted internally on an artifactory or local shared filesystem without internet access.

---

## Deployment Steps

### 1. Offline Binary Installation
Copy the native archive to your target machine:
```bash
# macOS
tar -xzf codeme-0.1.0-macos-arm64.tar.gz -C /opt/codeme

# Linux
tar -xzf codeme-0.1.0-linux-x64.tar.gz -C /opt/codeme
```

### 2. Perpetual Certificate Deployment
Place your enterprise certificate in the system configuration directory:
```bash
# Linux system-wide path
sudo mkdir -p /etc/codeme
sudo cp codeme-enterprise-perpetual.json /etc/codeme/license.json
sudo chmod 644 /etc/codeme/license.json
```

### 3. Verification
Verify that the engine recognizes the perpetual offline certificate:
```bash
codeme-licensing status
```
Expected output:
```json
{
  "status": "valid",
  "tier": "enterprise",
  "mode": "air_gapped",
  "expires_at": null,
  "entitlements": ["*"]
}
```
All enterprise invariants, transaction managers, and audit reporters will execute with zero network requirements.
