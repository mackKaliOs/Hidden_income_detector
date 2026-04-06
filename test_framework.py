"""
Unit tests for Hidden Income Detection Framework
"""

import pytest
import json
from src.framework import AnalysisFramework, RiskLevel
from src.scoring import ScoringModel, ScoringInput


class TestAnalysisFramework:
    """Test suite for AnalysisFramework"""
    
    @pytest.fixture
    def framework(self):
        """Fixture: Initialize framework"""
        return AnalysisFramework()
    
    @pytest.fixture
    def sample_case_data(self):
        """Fixture: Sample case data"""
        return {
            "claimed_status": {
                "claimed_income": 45000,
                "claimed_employment": "Part-time"
            },
            "observed_behaviors": [
                {
                    "type": "role_mismatch",
                    "observed_role": "IT Manager",
                    "severity": 8
                }
            ],
            "statements": [
                {
                    "statement_text": "Limited work obligations",
                    "contradicted": True,
                    "contradiction_source": "Behavior evidence",
                    "severity": 8
                }
            ],
            "control_indicators": [
                {
                    "description": "Makes critical decisions",
                    "weight": 3
                }
            ],
            "observed_benefits": [
                {
                    "description": "Insurance access",
                    "estimated_value": 15000,
                    "severity": 6
                }
            ]
        }
    
    def test_framework_initialization(self, framework):
        """Test framework initialization"""
        assert framework is not None
        assert framework.weights is not None
        assert abs(sum(framework.weights.values()) - 1.0) < 0.01
    
    def test_claimed_status_verification(self, framework, sample_case_data):
        """Test claimed status verification"""
        claimed_status = framework.verify_claimed_status(sample_case_data)
        assert claimed_status is not None
        assert claimed_status.get("claimed_income") == 45000
    
    def test_risk_classification(self, framework):
        """Test risk classification"""
        assert framework.classify_risk(1.0) == RiskLevel.LOW
        assert framework.classify_risk(4.0) == RiskLevel.MODERATE
        assert framework.classify_risk(6.5) == RiskLevel.HIGH
        assert framework.classify_risk(9.0) == RiskLevel.CRITICAL


class TestScoringModel:
    """Test suite for ScoringModel"""
    
    @pytest.fixture
    def model(self):
        """Fixture: Initialize scoring model"""
        return ScoringModel()
    
    def test_model_initialization(self, model):
        """Test model initialization"""
        assert model is not None
        assert len(model.weights) == 4
        assert abs(sum(model.weights.values()) - 1.0) < 0.01
    
    def test_score_calculation(self, model):
        """Test score calculation"""
        scoring_input = ScoringInput(
            identity_delta=8.0,
            legitimacy_delta=7.0,
            control_delta=8.0,
            extraction_gap=6.0
        )
        result = model.calculate(scoring_input)
        
        assert result.final_score >= 0
        assert result.final_score <= 10
        assert result.normalized_score >= 0
        assert result.normalized_score <= 10
    
    def test_risk_categorization_low(self, model):
        """Test low risk categorization"""
        scoring_input = ScoringInput(1.0, 1.0, 1.0, 1.0)
        result = model.calculate(scoring_input)
        assert result.risk_category == "LOW"
    
    def test_risk_categorization_critical(self, model):
        """Test critical risk categorization"""
        scoring_input = ScoringInput(9.0, 9.0, 9.0, 9.0)
        result = model.calculate(scoring_input)
        assert result.risk_category == "CRITICAL"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])