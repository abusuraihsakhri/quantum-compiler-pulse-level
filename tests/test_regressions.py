"""Regression tests for audit integrity, input constraints and API access."""
import pytest
from pydantic import ValidationError
from agents.base import AuditTrail
from agents.models import SystemTaskPayload


@pytest.mark.parametrize("field,value", [
    ("actor", "someone-else"),
    ("event_type", "TAMPERED"),
    ("payload_hash", "0" * 64),
    ("current_hash", "0" * 64),
    ("timestamp", "2000-01-01T00:00:00Z"),
])
def test_audit_chain_detects_signed_field_tampering(field, value):
    trail = AuditTrail(secret_key="test-only-key")
    trail.log("system", "supervisor", "EVALUATE", {"task": "T1"})
    trail.logs[0][field] = value
    assert trail.verify_integrity() is False


def test_audit_log_accessor_is_copy():
    trail = AuditTrail(secret_key="test-only-key")
    trail.log("system", "supervisor", "EVALUATE", {"task": "T1"})
    trail.get_trail()[0]["actor"] = "modified-copy"
    assert trail.verify_integrity() is True


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_input_rejected(value):
    with pytest.raises(ValidationError):
        SystemTaskPayload(task_id="T1", target_identifier="Q1", primary_metric=value)


def test_audit_log_endpoint_requires_secret(monkeypatch):
    from fastapi.testclient import TestClient
    from agents.api import app
    client = TestClient(app)
    monkeypatch.delenv("AUDIT_LOGS_TOKEN", raising=False)
    assert client.get("/api/audit/logs").status_code == 403
    monkeypatch.setenv("AUDIT_LOGS_TOKEN", "test-token")
    assert client.get("/api/audit/logs", headers={"Authorization": "Bearer wrong"}).status_code == 403
    assert client.get("/api/audit/logs", headers={"Authorization": "Bearer test-token"}).status_code == 200
