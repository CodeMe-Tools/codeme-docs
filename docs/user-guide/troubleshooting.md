# Codeme Troubleshooting and Diagnostic Guide

This guide covers common diagnostic scenarios, exit codes, concurrency locks, and transaction recovery.

---

## 1. Exit Codes

Codeme CLIs follow strict deterministic exit codes:
- **`0`**: Success. Zero violations detected. Output is completely silent (0 bytes).
- **`1`**: Unresolved violations detected. Diagnostics are output to stderr/stdout.
- **`2`**: System or runtime error (missing target path, corrupted configuration).

---

## 2. Resolving Multi-Agent Lease Contention
Codeme uses an exclusive SQLite WAL concurrency lease manager to prevent agents from clobbering identical files or workspaces.

If a lease lock times out or is held by an abandoned agent process:
```bash
# Check current lease locks
codeme-concurrency status

# Clean expired or orphaned leases
codeme-concurrency prune --force
```

---

## 3. Git Transaction Rollback
If an engine execution or repair step fails during an isolated git transaction:
- The temporary git worktree is discarded automatically.
- Your working tree remains 100% untouched.
- If an interrupted transaction left an uncommitted stash:
```bash
git worktree prune
```

---

## 4. Licence Ticket Verification Errors
If `codeme-licensing status` reports `tampered_or_invalid`:
1. Check that the ticket file was not reformatted with non-canonical whitespace (RFC 8785 requires strict canonical key ordering).
2. Verify system clock synchronization if receiving an `expired` status.
3. If the 30-day offline period expired, connect to the customer portal and run `codeme-licensing renew`.
