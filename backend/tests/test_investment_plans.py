import os
import pytest
import json
from decimal import Decimal

# Import modules to test
from investment_plans import InvestmentPlanManager
from investment_plan_validator import InvestmentPlanValidator

@pytest.fixture
def plan_manager():
    """
    Fixture to create an InvestmentPlanManager with a test database
    """
    test_db_url = 'sqlite:///test_investment_plans.db'
    return InvestmentPlanManager(database_url=test_db_url)

@pytest.fixture
def plan_validator():
    """
    Fixture to create an InvestmentPlanValidator
    """
    return InvestmentPlanValidator()

def test_create_investment_plan(plan_manager):
    """
    Test creating a valid investment plan
    """
    plan_data = {
        'name': 'Test Growth Plan',
        'description': 'High-risk investment strategy',
        'risk_level': 'high',
        'min_investment': 5000.0,
        'max_investment': 50000.0,
        'asset_allocation': {
            'stocks': 0.7,
            'crypto': 0.2,
            'cash': 0.1
        },
        'expected_return': 0.12,
        'volatility': 0.25,
        'investment_duration': 24,
        'rebalancing_frequency': 'quarterly'
    }
    
    result = plan_manager.create_investment_plan(**plan_data)
    
    assert result['status'] == 'created'
    assert result['name'] == plan_data['name']
    assert 'id' in result

def test_invalid_investment_plan_creation(plan_manager):
    """
    Test creating an invalid investment plan
    """
    invalid_plan_data = {
        'name': 'Invalid Plan',
        'risk_level': 'extreme',  # Invalid risk level
        'min_investment': -1000,  # Negative investment
        'asset_allocation': {
            'stocks': 1.5  # Invalid allocation
        }
    }
    
    with pytest.raises(ValueError):
        plan_manager.create_investment_plan(**invalid_plan_data)

def test_investment_plan_validation(plan_validator):
    """
    Test investment plan validation
    """
    valid_plan = {
        'name': 'Balanced Portfolio',
        'description': 'Moderate risk investment strategy',
        'risk_level': 'medium',
        'min_investment': 3000.0,
        'asset_allocation': {
            'stocks': 0.6,
            'bonds': 0.3,
            'cash': 0.1
        },
        'expected_return': 0.07,
        'volatility': 0.15
    }
    
    validation_result = plan_validator.validate_investment_plan(valid_plan)
    
    assert validation_result['is_valid'] is True
    assert len(validation_result['errors']) == 0

def test_investment_plan_performance_simulation(plan_validator):
    """
    Test performance simulation for investment plans
    """
    test_plan = {
        'name': 'Growth Strategy',
        'risk_level': 'high',
        'asset_allocation': {
            'stocks': 0.7,
            'crypto': 0.2,
            'cash': 0.1
        },
        'expected_return': 0.12,
        'volatility': 0.25
    }
    
    simulation_result = plan_validator.simulate_investment_performance(
        test_plan, 
        simulations=1000,
        investment_amount=10000
    )
    
    assert 'mean_final_value' in simulation_result
    assert 'success_probability' in simulation_result
    assert simulation_result['success_probability'] > 0
    assert simulation_result['success_probability'] <= 1

def test_investment_plan_recommendations(plan_validator):
    """
    Test plan adjustment recommendations
    """
    test_plan = {
        'name': 'Unbalanced Portfolio',
        'risk_level': 'low',
        'asset_allocation': {
            'stocks': 0.8,
            'crypto': 0.2
        },
        'expected_return': 0.03,
        'volatility': 0.30
    }
    
    recommendations = plan_validator.recommend_plan_adjustments(test_plan)
    
    assert 'asset_allocation' in recommendations
    assert 'risk_management' in recommendations
    assert len(recommendations['risk_management']) > 0

def test_investment_plan_retrieval(plan_manager):
    """
    Test retrieving investment plans with filters
    """
    # Create multiple plans
    plan_manager.create_investment_plan(
        name='Low Risk Plan',
        risk_level='low',
        min_investment=1000,
        asset_allocation={'bonds': 0.7, 'cash': 0.3},
        expected_return=0.04
    )
    
    plan_manager.create_investment_plan(
        name='High Risk Plan',
        risk_level='high',
        min_investment=5000,
        asset_allocation={'stocks': 0.8, 'crypto': 0.2},
        expected_return=0.12
    )
    
    # Retrieve plans
    low_risk_plans = plan_manager.get_investment_plans(
        risk_level='low',
        min_investment=500
    )
    
    high_risk_plans = plan_manager.get_investment_plans(
        risk_level='high',
        min_investment=3000
    )
    
    assert len(low_risk_plans) > 0
    assert len(high_risk_plans) > 0
    assert all(plan['risk_level'] == 'low' for plan in low_risk_plans)
    assert all(plan['risk_level'] == 'high' for plan in high_risk_plans)

def test_investment_plan_update(plan_manager):
    """
    Test updating an existing investment plan
    """
    # Create a plan
    original_plan = plan_manager.create_investment_plan(
        name='Initial Plan',
        risk_level='medium',
        min_investment=3000,
        asset_allocation={'stocks': 0.6, 'bonds': 0.4},
        expected_return=0.07
    )
    
    # Update the plan
    updated_plan = plan_manager.update_investment_plan(
        original_plan['id'],
        name='Updated Plan',
        expected_return=0.08,
        asset_allocation={'stocks': 0.7, 'bonds': 0.3}
    )
    
    assert updated_plan['name'] == 'Updated Plan'
    assert updated_plan['status'] == 'updated'

def main():
    """
    Run all tests
    """
    pytest.main([__file__])

if __name__ == '__main__':
    main()
