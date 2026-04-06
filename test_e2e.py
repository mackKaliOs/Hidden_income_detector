"""End-to-End System Test

Tests the complete system with real-world scenario
"""

import pytest
import tempfile
from pathlib import Path

from src.framework import AnalysisFramework


class TestEndToEndSystem:
    """End-to-end system tests with realistic scenarios"""
    
    @pytest.fixture
    def realistic_case(self):
        """Create a realistic case for testing"""
        return {
            "case_name": "Smith v. Jones - Child Support",
            "claimed_status": {
                "claimed_income": 40000,
                "claimed_employment": "Part-time Consultant",
                "claimed_capacity": "Limited availability"
            },
            "observed_behaviors": [
                {
                    "type": "role_mismatch",
                    "observed_role": "Business Operations Manager",
                    "severity": 8
                },
                {
                    "type": "authority_expansion",
                    "description": "Makes strategic decisions",
                    "severity": 9
                }
            ],
            "statements": [
                {
                    "statement_text": "I work part-time with limited availability",
                    "context": "Affidavit filed 2024-01-15",
                    "contradicted": True,
                    "contradiction_source": "LinkedIn shows full-time role",
                    "severity": 9
                },
                {
                    "statement_text": "I have no business control",
                    "context": "Court testimony 2024-02-10",
                    "contradicted": True,
                    "contradiction_source": "Company filings show signatory authority",
                    "severity": 8
                }
            ],
            "control_indicators": [
                {
                    "description": "Authorized signatory",
                    "weight": 3,
                    "source": "Company Secretary docs"
                },
                {
                    "description": "Hiring/firing decisions",
                    "weight": 3,
                    "source": "Employee interviews"
                }
            ],
            "observed_benefits": [
                {
                    "description": "Health insurance",
                    "estimated_value": 12000,
                    "severity": 6
                },
                {
                    "description": "Vehicle allowance",
                    "estimated_value": 8000,
                    "severity": 6
                },
                {
                    "description": "Office equipment",
                    "estimated_value": 15000,
                    "severity": 7
                }
            ],
            "timeline": [
                {
                    "date": "2024-01-15",
                    "event": "Affidavit filed",
                    "claimed_position": "Part-time, limited availability",
                    "observed_behavior": "Approved major contract",
                    "contradiction_type": "Time allocation",
                    "impact": "Suggests higher capacity"
                },
                {
                    "date": "2024-02-10",
                    "event": "Court testimony",
                    "claimed_position": "No business control",
                    "observed_behavior": "Updated signatory authority",
                    "contradiction_type": "Direct contradiction",
                    "impact": "Material misrepresentation"
                }
            ]
        }
    
    def test_realistic_case_analysis(self, realistic_case):
        """Test analysis of realistic case"""
        framework = AnalysisFramework()
        
        claimed_status = framework.verify_claimed_status(realistic_case)
        assert claimed_status['claimed_income'] == 40000
        
        identity_score, identity_contradictions = framework.analyze_identity_consistency(realistic_case)
        assert identity_score > 5
        assert len(identity_contradictions) > 0
        
        legitimacy_score, legitimacy_contradictions = framework.analyze_legitimacy_consistency(realistic_case)
        assert legitimacy_score > 5
        assert len(legitimacy_contradictions) >= 1
        
        control_score, control_findings = framework.analyze_control(realistic_case)
        assert control_score > 6
        assert len(control_findings) >= 2
        
        benefit_score, benefit_gaps = framework.analyze_benefit_gap(realistic_case)
        assert benefit_score > 4
        total_benefits = sum(b['estimated_value'] for b in realistic_case['observed_benefits'])
        assert total_benefits > 30000
    
    def test_realistic_case_scoring(self, realistic_case):
        """Test scoring on realistic case"""
        framework = AnalysisFramework()
        
        id_score, _ = framework.analyze_identity_consistency(realistic_case)
        leg_score, _ = framework.analyze_legitimacy_consistency(realistic_case)
        ctrl_score, _ = framework.analyze_control(realistic_case)
        ben_score, _ = framework.analyze_benefit_gap(realistic_case)
        
        final_score = framework.calculate_contradiction_score(
            id_score, leg_score, ctrl_score, ben_score
        )
        
        assert final_score > 6.0
        
        risk = framework.classify_risk(final_score)
        assert risk.value in ['HIGH', 'CRITICAL']
    
    def test_system_error_handling(self):
        """Test system handles errors gracefully"""
        framework = AnalysisFramework()
        
        empty_case = {}
        claimed = framework.verify_claimed_status(empty_case)
        assert claimed is not None
        
        score = framework.calculate_contradiction_score(-1, -1, -1, -1)
        assert isinstance(score, (int, float))
        
        risk_low = framework.classify_risk(0)
        risk_high = framework.classify_risk(100)
        assert risk_low is not None
        assert risk_high is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])