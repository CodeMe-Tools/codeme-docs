"""Documentation Synchronization and Consistency Validator.

Implements Phase 4 documentation synchronization between specifications,
ADRs, repository registries, product manifests, and docs repository.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class SyncReport:
    synchronized: bool
    adrs_synced: int = 0
    checks_passed: List[str] = field(default_factory=list)
    discrepancies: List[str] = field(default_factory=list)


class DocumentationSynchronizer:
    """Synchronizes and validates documentation consistency across the Codeme workspace."""

    def __init__(self, workspace_root: Optional[str | Path] = None):
        self.workspace_root = self._resolve_root(workspace_root)
        self.docs_repo = self.workspace_root / "repos" / "codeme-docs"

    def _resolve_root(self, given: Optional[str | Path]) -> Path:
        if given:
            return Path(given).resolve()
        curr = Path.cwd().resolve()
        for p in [curr] + list(curr.parents):
            if (p / "config" / "repository-registry.json").is_file():
                return p
        return curr

    def sync_adrs(self) -> int:
        """Copies ADRs from master docs/decisions into repos/codeme-docs/docs/adr/."""
        source_dir = self.workspace_root / "docs" / "decisions"
        dest_dir = self.docs_repo / "docs" / "adr"
        dest_dir.mkdir(parents=True, exist_ok=True)

        if not source_dir.is_dir():
            return 0

        synced = 0
        for adr in source_dir.glob("ADR-*.md"):
            dest_file = dest_dir / adr.name
            shutil.copy2(adr, dest_file)
            synced += 1

        return synced

    def validate_pricing_consistency(self) -> Tuple[bool, List[str]]:
        """Verifies product-manifest pricing matches documentation references."""
        manifest_path = self.workspace_root / "manifests" / "product-manifest.v1.json"
        discrepancies: List[str] = []

        if not manifest_path.is_file():
            discrepancies.append(f"Manifest not found: {manifest_path}")
            return False, discrepancies

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        pro = manifest.get("editions", {}).get("pro_local", {}).get("pricing", {})
        monthly = pro.get("monthly")
        annual = pro.get("annual")

        if monthly != 19.00 or annual != 190.00:
            discrepancies.append(f"Unexpected Pro Local pricing: monthly={monthly}, annual={annual}")

        return len(discrepancies) == 0, discrepancies

    def validate_repository_registry(self) -> Tuple[bool, List[str]]:
        """Verifies all repositories defined in registry exist on disk."""
        reg_path = self.workspace_root / "config" / "repository-registry.json"
        discrepancies: List[str] = []

        if not reg_path.is_file():
            discrepancies.append(f"Registry not found: {reg_path}")
            return False, discrepancies

        with open(reg_path, "r", encoding="utf-8") as f:
            reg = json.load(f)

        for repo in reg.get("repositories", []):
            expected_dir = self.workspace_root / repo["path"]
            if not expected_dir.is_dir():
                discrepancies.append(f"Repository directory does not exist: {expected_dir}")

        return len(discrepancies) == 0, discrepancies

    def run(self, perform_sync: bool = True) -> SyncReport:
        adrs_synced = 0
        if perform_sync:
            adrs_synced = self.sync_adrs()

        checks_passed: List[str] = []
        all_discrepancies: List[str] = []

        # Check 1: ADR Synchronization
        adr_dest = self.docs_repo / "docs" / "adr"
        if adr_dest.is_dir() and len(list(adr_dest.glob("ADR-*.md"))) >= 7:
            checks_passed.append("ADR Synchronization (>= 7 ADRs in codeme-docs)")
        else:
            all_discrepancies.append("ADR documentation synchronization incomplete.")

        # Check 2: Pricing consistency
        pricing_ok, p_discrepancies = self.validate_pricing_consistency()
        if pricing_ok:
            checks_passed.append("Product Manifest & Pricing Consistency")
        else:
            all_discrepancies.extend(p_discrepancies)

        # Check 3: Repository Registry consistency
        reg_ok, r_discrepancies = self.validate_repository_registry()
        if reg_ok:
            checks_passed.append("Repository Registry Path Synchronization")
        else:
            all_discrepancies.extend(r_discrepancies)

        is_sync = (len(all_discrepancies) == 0)

        return SyncReport(
            synchronized=is_sync,
            adrs_synced=adrs_synced,
            checks_passed=checks_passed,
            discrepancies=all_discrepancies,
        )


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="codeme-docs-sync", description="Codeme Documentation Synchronization Engine")
    parser.add_argument("--check-only", action="store_true", help="Validate without syncing")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args(argv)
    syncer = DocumentationSynchronizer()
    report = syncer.run(perform_sync=not args.check_only)

    if report.synchronized:
        if args.verbose:
            print(f"Documentation synchronized successfully. ADRs copied: {report.adrs_synced}")
            for c in report.checks_passed:
                print(f"  ✓ {c}")
        # Silent success contract
        return 0
    else:
        sys.stderr.write("Documentation synchronization discrepancies detected:\n")
        for d in report.discrepancies:
            sys.stderr.write(f"  ✗ {d}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
