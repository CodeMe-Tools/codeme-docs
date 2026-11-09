# ADR-0007: Merchant-of-Record Evaluation & Commercial Billing Architecture

## Status
Accepted

## Context
Codeme requires a compliant, low-overhead commercial billing and entitlement management platform for Pro Local, Team, Enterprise, and OEM editions.
Selling software globally (with primary UK operations in GBP £ and 20% VAT) entails cross-border sales tax, EU VAT MOSS, and US economic nexus compliance. Handling direct credit card transactions via raw payment gateways exposes the platform to PCI-DSS compliance burdens and multi-jurisdiction tax filings.
A Merchant of Record (MoR) acts as the legal reseller, calculating, collecting, and remitting sales taxes and VAT on behalf of Codeme Tools while providing developer-friendly APIs and webhooks.

## Evaluation of Providers

| Criteria | Polar (`polar.sh`) | Lemon Squeezy | Stripe (Direct Gateway) |
|---|---|---|---|
| **MoR Model** | Full Merchant of Record | Full Merchant of Record | Direct processor (Stripe Tax add-on needed) |
| **Transaction Fees** | 4% + 40¢ per transaction | 5% + 50¢ (+ 1.5% international) | 1.4% + 20p UK / 2.9% + 30¢ international + Tax fees |
| **UK / EU VAT & Invoicing** | Automated B2C/B2B VAT & compliant PDFs | Automated global VAT & tax invoices | Requires Stripe Tax & Invoicing configuration |
| **Developer API & Webhooks** | Modern REST / OpenAPI, HMAC SHA-256 | REST API, HMAC SHA-256 | REST API, HMAC SHA-256 |
| **Developer Tools Focus** | Specialized for dev tools & OSS projects | General digital products & SaaS | Broad e-commerce & enterprise |
| **Sandbox & Testing** | Comprehensive sandbox & CLI test tools | Sandbox store mode | Comprehensive test mode |

## Decision
1. **Primary Provider:** Polar is selected as the primary merchant-of-record for public checkout, customer subscriptions, and automated UK VAT handling.
2. **Provider Abstraction Layer (`BillingAdapter`):**
   - Implement an extensible billing adapter pattern in `codeme.billing.adapters`.
   - Support `PolarAdapter`, `LemonSqueezyAdapter`, and `SandboxMockAdapter` (for 100% offline testing and automated CI).
3. **Webhook Security & Idempotency:**
   - Webhooks must be verified using constant-time cryptographic HMAC-SHA256 signature checks.
   - All events are recorded in an idempotent SQLite ledger (`.codeme/billing.db`) with unique event IDs before processing. Replayed or duplicate webhooks are acknowledged without duplicate ticket issuance or state corruption.
4. **Entitlement Issuance Integration:**
   - On verified `subscription.created` or `order.created`, the billing handler reads product tiers directly from `manifests/product-manifest.v1.json`.
   - Ed25519-signed offline capability tickets (30-day validity, 7-day grace period) are issued automatically and stored in the customer's portal account.
5. **Team Seat Allocation:**
   - Team editions require a minimum of 5 paid seats (£75/month or £750/year).
   - The billing engine enforces seat thresholds, named developer assignments, and container-safe device fingerprint binding.

## Consequences
- Guaranteed regulatory compliance for UK and international VAT/sales tax.
- Zero customer card data stored locally or handled by Codeme services (PCI-DSS Scope reduced to SAQ A).
- Complete offline testability via the `SandboxMockAdapter`.
