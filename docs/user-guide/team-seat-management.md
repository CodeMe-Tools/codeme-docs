# Codeme Team Seat Management

The Codeme Team edition provides multi-developer licensing, centralized policy distribution, and aggregated token audit metrics.

---

## 5-Seat Minimum Policy
Team subscriptions enforce a minimum allocation of **5 seats** (£75.00/month or £750.00/year). Additional seats can be purchased dynamically at £15.00/seat/month (£150.00/seat/year).

---

## Seat Allocation Models

Codeme Team supports two seat management strategies:

### 1. Named Developer Seats (Default)
Each seat is explicitly assigned to an individual engineer's email address or developer ID.
- Assigned developers receive an individual signed Ed25519 capability ticket.
- Reassignment can be performed via the customer portal or CLI by an administrator.

### 2. Floating Developer Pool
For dynamic teams and CI/CD pipelines:
- A shared lease pool allows unassigned developers or automated agents to check out an offline capability lease.
- Leases are valid for up to 30 days and return to the pool upon explicit release or lease expiration.

---

## Managing Seats via Customer Portal
1. Navigate to `/account/seats` on the Codeme customer portal.
2. View current seat utilization (e.g. `5 of 5 assigned`).
3. Click **Assign Seat** to add a developer's email address.
4. Click **Revoke / Reassign** to move a seat to another developer.

---

## Team Policy Distribution
Team administrators can commit an organization-wide policy manifest (`codeme-team-policy.json`) to their repository root:
```json
{
  "$schema": "https://codeme.tools/schemas/team-policy.v1.json",
  "policy_name": "Acme Core Team Policy",
  "rules": {
    "max_cyclomatic_complexity": 8,
    "max_nesting_depth": 3,
    "enforce_ddd_boundaries": true,
    "block_destructive_migrations": true
  }
}
```
All developers running with a Team licence automatically inherit and enforce these standards.
