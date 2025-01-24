import os
import re
import math
import logging
from typing import Dict, Any, List, Optional
from decimal import Decimal, getcontext

import numpy as np
import pandas as pd
from scipy import stats

class InvestmentPlanValidator:
    """
    Comprehensive Investment Plan Validation Framework
    
    Provides advanced validation and risk assessment
    for investment plans
    """
    
    def __init__(self, logging_level: str = 'INFO'):
        """
        Initialize validator
        
        Args:
            logging_level: Logging verbosity
        """
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, logging_level),
            format='%(asctime)s - %(name)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Set decimal precision
        getcontext().prec = 6
    
    def validate_investment_plan(
        self, 
        plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Comprehensive investment plan validation
        
        Args:
            plan: Investment plan configuration
        
        Returns:
            Validation result with detailed feedback
        """
        validation_results = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Validate basic plan structure
        required_fields = [
            'name', 'description', 'risk_level', 
            'min_investment', 'asset_allocation',
            'expected_return', 'volatility'
        ]
        
        for field in required_fields:
            if field not in plan:
                validation_results['is_valid'] = False
                validation_results['errors'].append(
                    f"Missing required field: {field}"
                )
        
        # Validate name and description
        if len(plan.get('name', '')) < 3:
            validation_results['is_valid'] = False
            validation_results['errors'].append(
                "Plan name must be at least 3 characters long"
            )
        
        # Validate risk level
        valid_risk_levels = ['low', 'medium', 'high']
        if plan.get('risk_level') not in valid_risk_levels:
            validation_results['is_valid'] = False
            validation_results['errors'].append(
                f"Invalid risk level. Must be one of {valid_risk_levels}"
            )
        
        # Validate investment thresholds
        if plan.get('min_investment', 0) < 0:
            validation_results['is_valid'] = False
            validation_results['errors'].append(
                "Minimum investment cannot be negative"
            )
        
        if (plan.get('max_investment') is not None and 
            plan.get('max_investment') < plan.get('min_investment')):
            validation_results['is_valid'] = False
            validation_results['errors'].append(
                "Maximum investment must be greater than minimum investment"
            )
        
        # Validate asset allocation
        allocation = plan.get('asset_allocation', {})
        total_allocation = sum(allocation.values())
        
        if not (0.99 <= total_allocation <= 1.01):
            validation_results['is_valid'] = False
            validation_results['errors'].append(
                f"Asset allocation must total 1.0 (current: {total_allocation})"
            )
        
        # Validate individual asset allocations
        for asset, percentage in allocation.items():
            if percentage < 0 or percentage > 1:
                validation_results['is_valid'] = False
                validation_results['errors'].append(
                    f"Invalid allocation for {asset}: {percentage}"
                )
        
        # Validate return and volatility
        expected_return = plan.get('expected_return', 0)
        volatility = plan.get('volatility', 0)
        
        if expected_return < -1 or expected_return > 1:
            validation_results['is_valid'] = False
            validation_results['errors'].append(
                "Expected return must be between -100% and 100%"
            )
        
        if volatility < 0 or volatility > 1:
            validation_results['is_valid'] = False
            validation_results['errors'].append(
                "Volatility must be between 0 and 1"
            )
        
        # Risk-Return Consistency Check
        risk_return_mapping = {
            'low': (0, 0.05),
            'medium': (0.05, 0.10),
            'high': (0.10, 0.25)
        }
        
        risk_level = plan.get('risk_level', 'medium')
        min_return, max_return = risk_return_mapping.get(risk_level, (0, 0.10))
        
        if not (min_return <= expected_return <= max_return):
            validation_results['warnings'].append(
                f"Expected return {expected_return} seems inconsistent "
                f"with {risk_level} risk level (expected range: {min_return}-{max_return})"
            )
        
        return validation_results
    
    def simulate_investment_performance(
        self, 
        plan: Dict[str, Any], 
        simulations: int = 1000,
        investment_amount: float = 10000
    ) -> Dict[str, Any]:
        """
        Monte Carlo simulation of investment performance
        
        Args:
            plan: Investment plan configuration
            simulations: Number of simulation runs
            investment_amount: Initial investment amount
        
        Returns:
            Performance simulation results
        """
        # Asset return assumptions (historical averages)
        asset_returns = {
            'stocks': 0.10,
            'bonds': 0.04,
            'cash': 0.02,
            'crypto': 0.30,
            'real_estate': 0.08
        }
        
        # Asset volatilities
        asset_volatilities = {
            'stocks': 0.15,
            'bonds': 0.05,
            'cash': 0.01,
            'crypto': 0.50,
            'real_estate': 0.10
        }
        
        allocation = plan.get('asset_allocation', {})
        
        # Simulation results storage
        final_values = []
        
        for _ in range(simulations):
            portfolio_value = investment_amount
            
            for asset, weight in allocation.items():
                # Simulate asset return with randomness
                annual_return = np.random.normal(
                    asset_returns.get(asset, 0.05),
                    asset_volatilities.get(asset, 0.10)
                )
                
                asset_value = investment_amount * weight * (1 + annual_return)
                portfolio_value += asset_value - (investment_amount * weight)
            
            final_values.append(portfolio_value)
        
        # Performance analysis
        final_values_array = np.array(final_values)
        
        return {
            'mean_final_value': np.mean(final_values_array),
            'median_final_value': np.median(final_values_array),
            'min_final_value': np.min(final_values_array),
            'max_final_value': np.max(final_values_array),
            'value_at_risk_95': np.percentile(final_values_array, 5),
            'success_probability': np.mean(final_values_array > investment_amount)
        }
    
    def recommend_plan_adjustments(
        self, 
        plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Provide recommendations for plan improvement
        
        Args:
            plan: Investment plan configuration
        
        Returns:
            Recommended plan adjustments
        """
        recommendations = {
            'asset_allocation': {},
            'risk_management': []
        }
        
        # Asset allocation recommendations
        current_allocation = plan.get('asset_allocation', {})
        risk_level = plan.get('risk_level', 'medium')
        
        recommended_allocation = {
            'low': {
                'stocks': 0.4,
                'bonds': 0.5,
                'cash': 0.1
            },
            'medium': {
                'stocks': 0.6,
                'bonds': 0.3,
                'cash': 0.1
            },
            'high': {
                'stocks': 0.8,
                'crypto': 0.15,
                'cash': 0.05
            }
        }
        
        target_allocation = recommended_allocation.get(risk_level, {})
        
        for asset, target_weight in target_allocation.items():
            current_weight = current_allocation.get(asset, 0)
            deviation = abs(current_weight - target_weight)
            
            if deviation > 0.1:  # 10% deviation threshold
                recommendations['asset_allocation'][asset] = {
                    'current_weight': current_weight,
                    'recommended_weight': target_weight,
                    'suggested_action': 'rebalance'
                }
        
        # Risk management recommendations
        expected_return = plan.get('expected_return', 0)
        volatility = plan.get('volatility', 0)
        
        if volatility > 0.25 and risk_level == 'low':
            recommendations['risk_management'].append(
                "High volatility detected. Consider reducing risk exposure."
            )
        
        if expected_return < 0.03 and risk_level == 'high':
            recommendations['risk_management'].append(
                "Low expected return for high-risk plan. Consider adjusting strategy."
            )
        
        return recommendations

def main():
    """
    Demonstrate investment plan validation
    """
    validator = InvestmentPlanValidator()
    
    # Sample investment plan
    growth_plan = {
        'name': 'Aggressive Growth Strategy',
        'description': 'High-risk investment plan',
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
        'investment_duration': 24
    }
    
    # Validate investment plan
    validation_result = validator.validate_investment_plan(growth_plan)
    print("Plan Validation Result:")
    print(validation_result)
    
    # Simulate investment performance
    performance_simulation = validator.simulate_investment_performance(
        growth_plan, 
        simulations=5000
    )
    print("\nPerformance Simulation:")
    print(performance_simulation)
    
    # Get plan adjustment recommendations
    recommendations = validator.recommend_plan_adjustments(growth_plan)
    print("\nPlan Recommendations:")
    print(recommendations)

if __name__ == '__main__':
    main()
