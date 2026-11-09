"""Tests for documentation synchronization engine."""

import pytest
from pathlib import Path
from codeme_docs.sync import DocumentationSynchronizer


def test_documentation_sync_and_validation():
    syncer = DocumentationSynchronizer()
    report = syncer.run(perform_sync=True)

    assert report.synchronized is True
    assert report.adrs_synced >= 7
    assert len(report.discrepancies) == 0
    assert any("ADR Synchronization" in c for c in report.checks_passed)
    assert any("Pricing" in c for c in report.checks_passed)
    assert any("Repository Registry" in c for c in report.checks_passed)


    assert any("Customer User & Operations Guides" in c for c in report.checks_passed)


def test_customer_user_and_operations_guides_exist():
    docs_user = Path("repos/codeme-docs/docs/user-guide").resolve()
    docs_ops = Path("repos/codeme-docs/docs/operations").resolve()

    assert (docs_user / "getting-started.md").is_file()
    assert (docs_user / "supported-editions.md").is_file()
    assert (docs_user / "cli-engines.md").is_file()
    assert (docs_user / "licensing-and-activation.md").is_file()
    assert (docs_user / "team-seat-management.md").is_file()
    assert (docs_user / "enterprise-air-gap.md").is_file()
    assert (docs_user / "oem-integration.md").is_file()
    assert (docs_user / "troubleshooting.md").is_file()

    assert (docs_ops / "commercial-release-guide.md").is_file()
    assert (docs_ops / "production-gating-and-authorization.md").is_file()


def test_adr_files_exist_in_docs_repo():
    docs_adr = Path("repos/codeme-docs/docs/adr").resolve()
    assert docs_adr.is_dir()
    adrs = list(docs_adr.glob("ADR-*.md"))
    assert len(adrs) >= 9
    assert (docs_adr / "ADR-0009-commercial-release-preparation-and-publication-gate.md").is_file()
