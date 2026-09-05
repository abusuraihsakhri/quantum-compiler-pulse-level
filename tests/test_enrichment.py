"""
Automated Pytest for quantum-compiler-pulse-level Enrichment Modules.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from enrichment import (
    DragPulseOptimizationViaBayesianTuningEngine,
    ImplementationEngine,
    FilesToCreatemodifyEngine,
    TestingEngine,
    CrosstalkAwarePulseSchedulingEngine,
    CrosstalkMatrixImplementationEngine,
    CrosstalkMatrixFilesEngine,
    CrosstalkTestingEngine,
    QuantumcompilerpulselevelEnrichmentSuite,
    enrichment_suite,
)

def test_enrichment_suite_execution():
    suite = QuantumcompilerpulselevelEnrichmentSuite()
    res = suite.execute_all(primary_val=0.5, secondary_val=0.2)
    assert len(res) >= 8
    for k, v in res.items():
        assert v.status in ["OPTIMAL", "WARNING", "CRITICAL_ALERT"]
        assert isinstance(v.recommendations, list)

def test_enrichment_threshold_escalation():
    suite = QuantumcompilerpulselevelEnrichmentSuite()
    res = suite.execute_all(primary_val=10.0, secondary_val=5.0)
    for k, v in res.items():
        assert v.status in ["WARNING", "CRITICAL_ALERT"]
        assert len(v.alerts) > 0

def test_enrichment_suite_unique_results():
    """Verify all 8 engines produce unique results."""
    suite = QuantumcompilerpulselevelEnrichmentSuite()
    res = suite.execute_all(primary_val=0.5, secondary_val=0.2)
    expected_keys = {
        "DragPulseOptimizationViaBayesianTuningEngine",
        "ImplementationEngine",
        "FilesToCreatemodifyEngine",
        "TestingEngine",
        "CrosstalkAwarePulseSchedulingEngine",
        "CrosstalkMatrixImplementationEngine",
        "CrosstalkMatrixFilesEngine",
        "CrosstalkTestingEngine",
    }
    assert set(res.keys()) == expected_keys

def test_individual_engines():
    """Test each enrichment engine independently."""
    engines = [
        DragPulseOptimizationViaBayesianTuningEngine(),
        ImplementationEngine(),
        FilesToCreatemodifyEngine(),
        TestingEngine(),
        CrosstalkAwarePulseSchedulingEngine(),
        CrosstalkMatrixImplementationEngine(),
        CrosstalkMatrixFilesEngine(),
        CrosstalkTestingEngine(),
    ]
    for engine in engines:
        result = engine.evaluate(0.5, 0.2)
        assert result.status == "OPTIMAL"
        assert len(result.recommendations) > 0
