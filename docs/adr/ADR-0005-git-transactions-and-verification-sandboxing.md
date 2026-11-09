# ADR-0005: Git Transactions & Verification Sandboxing

## Status
Accepted

## Context
Automated tools and agents can introduce unintended modifications or corrupt unstaged/staged working tree states when attempting repairs or running test suites.

## Decision
1. All verification and repair operations execute inside a deterministic Git transaction boundary.
2. The transaction snapshots the working tree state (including untracked files, staged index, and unstaged modifications) before applying any mutations.
3. Candidate repairs are tested against verification gates. If verification fails, the transaction is immediately rolled back to the original snapshot without damaging the developer's working tree.
4. When `--sandbox` is requested, verification executes in an isolated temporary Git worktree (`git worktree add`).
5. Destructive operations (`git reset --hard`, `git clean -fd`, silent staging) are strictly prohibited unless explicitly requested by the caller.

## Consequences
- Guaranteed safety of existing developer work.
- Zero risk of destructive unstaged loss.
- Safe automated repair loops.
