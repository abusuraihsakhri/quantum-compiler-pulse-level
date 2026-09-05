"""
Security and input validation tests for quantum-compiler-pulse-level.
"""
import sys
import os
import tempfile
import csv
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from agents.base import PHIGuard, AuditLogger, SecurityException, AuditTrail, assert_no_phi
from agents.models import SystemTaskPayload, UrgencyLevel


class TestPHIGuard:
    """Test PHI outbound guard patterns."""

    def test_mrn_detection(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("Patient MRN-12345678")

    def test_ssn_detection(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("SSN: 123-45-6789")

    def test_phone_detection(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("Call 555-123-4567")

    def test_email_detection(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("Contact user@example.com")

    def test_clean_text_passes(self):
        PHIGuard.assert_no_phi("Task analysis for TARGET-01 with primary metric 25.3")

    def test_empty_text_passes(self):
        PHIGuard.assert_no_phi("")

    def test_none_text_passes(self):
        PHIGuard.assert_no_phi(None)

    def test_redact_phi(self):
        result = PHIGuard.redact_phi("Patient MRN-12345678 and SSN 123-45-6789")
        assert "REDACTED_IDENTIFIER" in result
        assert "MRN" not in result
        assert "123-45-6789" not in result

    def test_redact_preserves_clean_text(self):
        result = PHIGuard.redact_phi("Clean analysis text")
        assert result == "Clean analysis text"


class TestAuditTrail:
    """Test HMAC-SHA256 audit trail integrity."""

    def test_audit_trail_integrity(self):
        trail = AuditTrail(secret_key="test-key-2026")
        trail.log("test_actor", "supervisor", "TEST_EVENT", {"key": "value"})
        trail.log("test_actor", "supervisor", "TEST_EVENT_2", {"key2": "value2"})
        assert trail.verify_integrity() is True

    def test_audit_trail_entries_linked(self):
        trail = AuditTrail(secret_key="test-key-2026")
        entry1 = trail.log("actor1", "worker", "EVENT_1", {"data": 1})
        entry2 = trail.log("actor2", "worker", "EVENT_2", {"data": 2})
        assert entry2["prev_hash"] == entry1["current_hash"]

    def test_audit_trail_empty(self):
        trail = AuditTrail(secret_key="test-key-2026")
        assert trail.verify_integrity() is True
        assert len(trail.get_trail()) == 0


class TestBatchProcessing:
    """Test CSV batch processing with validation."""

    def _create_csv(self, rows, fieldnames=None):
        """Helper to create a temporary CSV file."""
        if fieldnames is None:
            fieldnames = ["task_id", "target_identifier", "primary_metric", "secondary_metric", "is_critical_flag", "status_descriptor"]
        fd, path = tempfile.mkstemp(suffix=".csv")
        with os.fdopen(fd, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return path

    def test_batch_valid_csv(self):
        from cli import main
        csv_path = self._create_csv([
            {"task_id": "T1", "target_identifier": "K1", "primary_metric": "10.0", "secondary_metric": "5.0", "is_critical_flag": "False", "status_descriptor": "NOMINAL"},
            {"task_id": "T2", "target_identifier": "K2", "primary_metric": "30.0", "secondary_metric": "5.0", "is_critical_flag": "False", "status_descriptor": "NOMINAL"},
        ])
        fd, output_path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            result = main(["batch", "-i", csv_path, "-o", output_path])
            assert result == 0
            with open(output_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                assert len(rows) == 2
                assert rows[0]["overall_urgency"] == "ROUTINE"
                assert rows[1]["overall_urgency"] == "ELEVATED_RISK"
        finally:
            os.unlink(csv_path)
            os.unlink(output_path)

    def test_batch_missing_file(self):
        from cli import main
        fd, output_path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            result = main(["batch", "-i", "nonexistent.csv", "-o", output_path])
            assert result == 1
        finally:
            os.unlink(output_path)

    def test_batch_invalid_numeric(self):
        from cli import main
        csv_path = self._create_csv([
            {"task_id": "T1", "target_identifier": "K1", "primary_metric": "invalid", "secondary_metric": "5.0", "is_critical_flag": "False", "status_descriptor": "NOMINAL"},
            {"task_id": "T2", "target_identifier": "K2", "primary_metric": "15.0", "secondary_metric": "5.0", "is_critical_flag": "False", "status_descriptor": "NOMINAL"},
        ])
        fd, output_path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            result = main(["batch", "-i", csv_path, "-o", output_path])
            assert result == 0  # Should succeed with valid rows
            with open(output_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                assert len(rows) == 1  # Only valid row processed
        finally:
            os.unlink(csv_path)
            os.unlink(output_path)


class TestCLICommands:
    """Test CLI command edge cases."""

    def test_audit_default_params(self):
        from cli import main
        result = main(["audit"])
        assert result == 0

    def test_audit_custom_params(self):
        from cli import main
        result = main(["audit", "--task-id", "TEST-01", "--target", "TARGET-X", "--primary", "35.0", "--secondary", "15.0", "--critical", "--status", "ANOMALY"])
        assert result == 0

    def test_chat_command(self):
        from cli import main
        result = main(["chat", "What", "is", "the", "status"])
        assert result == 0

    def test_verify_audit(self):
        from cli import main
        result = main(["verify-audit"])
        assert result == 0
