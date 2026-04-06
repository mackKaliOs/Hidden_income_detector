"""Integration Test Suite - Verify Complete Framework

Tests all major components and workflows
"""

import pytest
import json
import os
from pathlib import Path

# Import framework components
from src.framework import AnalysisFramework, RiskLevel
from src.scoring import ScoringModel, ScoringInput
from src.timeline import TimelineBuilder
from src.license_enforcer import LicenseValidator, CommercialUseDetector


class TestFrameworkIntegration:
    """Integration tests for the complete framework"""
    
    @pytest.fixture
    def sample_case_data(self):
        """Sample case data for testing"""
        return {
            "case_name": "Integration Test Case",
            "claimed_status": {
                "claimed_income": 45000,
                "claimed_employment": "Part-time",
                "claimed_capacity": "Limited"
            },
            "observed_behaviors": [
                {"type": "role_mismatch", "observed_role": "IT Manager", "severity": 8},
                {"type": "authority_expansion", "severity": 7}
            ],
            "statements": [
                {
                    "statement_text": "Limited work obligations",
                    "contradicted": True,
                    "contradiction_source": "Observed behavior",
                    "severity": 8
                }
            ],
            "control_indicators": [
                {"description": "Makes critical decisions", "weight": 3},
                {"description": "Manages infrastructure", "weight": 3}
            ],
            "observed_benefits": [
                {"description": "Insurance access", "estimated_value": 15000, "severity": 6},
                {"description": "Business benefits", "estimated_value": 20000, "severity": 7}
            ],
            "timeline": [
                {
                    "date": "2024-01-15",
                    "event": "Court Appearance",
                    "claimed_position": "Part-time",
                    "observed_behavior": "Prioritized work",
                    "contradiction_type": "Identity Mismatch",
                    "impact": "High capacity"
                }
            ]
        }
    
    def test_framework_initialization(self):
        """Test framework initializes without errors"""
        framework = AnalysisFramework()
        assert framework is not None
        assert hasattr(framework, 'weights')
    
    def test_framework_analysis_complete(self, sample_case_data):
        """Test complete framework analysis workflow"""
        framework = AnalysisFramework()
        
        claimed = framework.verify_claimed_status(sample_case_data)
        assert claimed is not None
        assert claimed['claimed_income'] == 45000
        
        identity_score, _ = framework.analyze_identity_consistency(sample_case_data)
        assert 0 <= identity_score <= 10
        
        legitimacy_score, _ = framework.analyze_legitimacy_consistency(sample_case_data)
        assert 0 <= legitimacy_score <= 10
        
        control_score, _ = framework.analyze_control(sample_case_data)
        assert 0 <= control_score <= 10
        
        benefit_score, _ = framework.analyze_benefit_gap(sample_case_data)
        assert 0 <= benefit_score <= 10
    
    def test_scoring_calculation(self):
        """Test weighted scoring calculation"""
        framework = AnalysisFramework()
        score = framework.calculate_contradiction_score(8, 8, 8, 6)
        assert 0 <= score <= 10
        assert isinstance(score, (int, float))
    
    def test_risk_classification(self):
        """Test risk classification for all levels"""
        framework = AnalysisFramework()
        
        assert framework.classify_risk(1.0) == RiskLevel.LOW
        assert framework.classify_risk(3.5) == RiskLevel.MODERATE
        assert framework.classify_risk(6.0) == RiskLevel.HIGH
        assert framework.classify_risk(9.0) == RiskLevel.CRITICAL
    
    def test_scoring_model_initialization(self):
        """Test scoring model initializes correctly"""
        model = ScoringModel()
        assert model is not None
        assert len(model.weights) == 4
        assert abs(sum(model.weights.values()) - 1.0) < 0.01
    
    def test_timeline_builder_initialization(self):
        """Test timeline builder initializes"""
        timeline = TimelineBuilder()
        assert timeline is not None
        assert len(timeline.events) == 0
    
    def test_timeline_event_addition(self):
        """Test adding events to timeline"""
        timeline = TimelineBuilder()
        
        timeline.add_event(
            date="2024-01-15",
            event="Test Event",
            claimed_position="Claimed",
            observed_behavior="Observed",
            contradiction_type="Type",
            impact="Impact"
        )
        
        assert len(timeline.events) == 1
        assert timeline.events[0]["date"] == "2024-01-15"
    
    def test_license_validator_initialization(self):
        """Test license validator initializes"""
        validator = LicenseValidator()
        assert validator is not None
        assert validator.is_valid is False
    
    def test_commercial_use_detector_initialization(self):
        """Test commercial use detector initializes"""
        detector = CommercialUseDetector()
        assert detector is not None
        assert detector.is_commercial_context is False


class TestDependencies:
    """Test that all dependencies are available and working"""
    
    def test_pypdf_import(self):
        """Test pypdf imports correctly"""
        try:
            import pypdf
            assert hasattr(pypdf, '__version__')
        except ImportError:
            pytest.skip("pypdf not installed")
    
    def test_required_imports(self):
        """Test all required modules import successfully"""
        import json
        import os
        import logging
        from datetime import datetime
        from pathlib import Path
        
        assert json is not None
        assert os is not None
        assert logging is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])