# Specification: Ed25519 Cryptographic Licensing & Entitlements

## Cryptographic Envelope
Licensing files use standard Ed25519 digital signatures over canonical JSON (RFC 8785).

```json
{
  "schema_version": 1,
  "product": "codeme",
  "edition": "team",
  "license_id": "LIC-2026-X892",
  "customer_id": "ORG-ALPHA",
  "issued_at": "2026-11-09T00:00:00Z",
  "expires_at": "2027-11-09T00:00:00Z",
  "seat_limit": 5,
  "entitlements": [
    "advanced_invariants",
    "team_policies",
    "team_audit"
  ],
  "signature_algorithm": "Ed25519",
  "key_id": "codeme-root-2026-v1",
  "signature": "..."
}
```

## Offline Models
1. **Pro & Team 30-Day Renewable Tickets:**
   - Valid for 30 days offline from last signed ticket issue.
   - Background non-blocking renewal when connected.
   - 7-day grace period with warning before blocking.
2. **Enterprise Air-Gapped Operation:**
   - Signed capability certificates without online check-ins.
   - Indefinite or contractual long-duration validity.
   - Zero outbound requests.
