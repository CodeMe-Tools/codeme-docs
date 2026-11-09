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


def test_adr_files_exist_in_docs_repo():
    docs_adr = Path("repos/codeme-docs/docs/adr").resolve()
    assert docs_adr.is_dir()
    adrs = list(docs_adr.glob("ADR-*.md"))
    assert len(adrs) >= 7
