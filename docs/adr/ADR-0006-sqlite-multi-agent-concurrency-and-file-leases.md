# ADR-0006: SQLite Multi-Agent Concurrency & File Leases

## Status
Accepted

## Context
Multiple coding agents or background processes may analyze and attempt repairs in the same repository simultaneously. Without concurrency controls, file collisions and conflicting modifications can corrupt the project.

## Decision
1. Concurrency coordination is managed via a local, zero-config SQLite database located at `.codeme/locks.db`.
2. Agents must acquire an exclusive lease before modifying any file. Shared read leases are permitted for concurrent analysis.
3. Every lease carries a time-to-live (default 60 seconds) and must be refreshed via heartbeats.
4. If an agent crashes or hangs, stale locks expire automatically, preventing deadlocks.
5. SQLite WAL mode (Write-Ahead Logging) is enabled for fast, concurrency-safe access across processes.

## Consequences
- Conflict-free multi-agent collaboration.
- Automatic recovery from agent crashes.
- Zero external daemon or server requirement.
