import os
import sys
import logging
import pytest
from typing import Dict, Any, List

# Import core system components
from backend.investment_plans import InvestmentPlanManager
from backend.ml.investment_prediction_model import InvestmentPredictionModel
from backend.security_audit import ComprehensiveSecurity
from backend.monitoring.health_monitor import SystemHealthMonitor
from backend.database.connection import DatabaseConnection

class ComprehensiveSystemIntegrationTest:
    def __init__(self):
        """
        Initialize comprehensive system integration test
        Configures logging and test environment
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize system components
        self.investment_plan_manager = InvestmentPlanManager()
        self.prediction_model = InvestmentPredictionModel()
        self.security_auditor = ComprehensiveSecurity()
        self.health_monitor = SystemHealthMonitor()
        self.db_connection = DatabaseConnection()
    
    def test_database_connectivity(self) -> Dict[str, Any]:
        """
        Test database connection and basic operations
        
        Returns:
            Test results with connection status and performance metrics
        """
        try:
            connection_result = self.db_connection.test_connection()
            performance_metrics = self.db_connection.get_connection_performance()
            
            return {
                'status': 'SUCCESS',
                'connection_time_ms': performance_metrics['connection_time'],
                'query_performance': performance_metrics['query_performance']
            }
        except Exception as e:
            self.logger.error(f"Database connectivity test failed: {e}")
            return {
                'status': 'FAILED',
                'error': str(e)
            }
    
    def test_investment_plan_workflow(self) -> Dict[str, Any]:
        """
        Test complete investment plan creation and validation workflow
        
        Returns:
            Workflow test results with plan creation and validation details
        """
        test_plans = [
            {
                'name': 'Conservative Growth',
                'risk_level': 'low',
                'initial_investment': 5000,
                'asset_allocation': {
                    'bonds': 0.7,
                    'stocks': 0.3
                }
            },
            {
                'name': 'Tech Innovation',
                'risk_level': 'high',
                'initial_investment': 10000,
                'asset_allocation': {
                    'tech_stocks': 0.6,
                    'emerging_markets': 0.4
                }
            }
        ]
        
        workflow_results = []
        
        for plan in test_plans:
            try:
                # Create investment plan
                created_plan = self.investment_plan_manager.create_plan(plan)
                
                # Validate investment plan
                validation_result = self.investment_plan_manager.validate_plan(created_plan)
                
                workflow_results.append({
                    'plan_name': plan['name'],
                    'created': True,
                    'validated': validation_result['is_valid'],
                    'recommendations': validation_result.get('recommendations', [])
                })
            except Exception as e:
                workflow_results.append({
                    'plan_name': plan['name'],
                    'created': False,
                    'error': str(e)
                })
        
        return {
            'total_plans_tested': len(test_plans),
            'workflow_results': workflow_results
        }
    
    def test_ml_prediction_integration(self) -> Dict[str, Any]:
        """
        Test machine learning prediction model integration
        
        Returns:
            Prediction test results with model performance metrics
        """
        test_scenarios = [
            [0.5, 0.07, 3, 5],   # Moderate risk scenario
            [0.2, 0.04, 1, 2],   # Low risk scenario
            [0.8, 0.15, 5, 7]    # High risk scenario
        ]
        
        prediction_results = []
        
        for scenario in test_scenarios:
            try:
                predicted_return = self.prediction_model.predict_investment_return(scenario)
                prediction_results.append({
                    'input_features': scenario,
                    'predicted_return': predicted_return
                })
            except Exception as e:
                prediction_results.append({
                    'input_features': scenario,
                    'error': str(e)
                })
        
        return {
            'total_scenarios': len(test_scenarios),
            'prediction_results': prediction_results
        }
    
    def test_security_integration(self) -> Dict[str, Any]:
        """
        Comprehensive security integration test
        
        Returns:
            Security test results with audit details
        """
        try:
            security_report = self.security_auditor.generate_comprehensive_report()
            
            return {
                'overall_status': security_report['overall_status'],
                'critical_checks': [
                    check for check in security_report['security_checks']
                    if check['status'] == 'CRITICAL'
                ]
            }
        except Exception as e:
            self.logger.error(f"Security integration test failed: {e}")
            return {
                'status': 'FAILED',
                'error': str(e)
            }
    
    def run_comprehensive_integration_test(self) -> Dict[str, Any]:
        """
        Execute comprehensive system integration test
        
        Returns:
            Complete test suite results
        """
        self.logger.info("Starting Comprehensive System Integration Test")
        
        integration_results = {
            'database_connectivity': self.test_database_connectivity(),
            'investment_plan_workflow': self.test_investment_plan_workflow(),
            'ml_prediction_integration': self.test_ml_prediction_integration(),
            'security_integration': self.test_security_integration()
        }
        
        # Log test results
        for test_name, result in integration_results.items():
            self.logger.info(f"{test_name}: {result}")
        
        return integration_results

def main():
    """
    Run comprehensive system integration test
    """
    integration_test = ComprehensiveSystemIntegrationTest()
    comprehensive_results = integration_test.run_comprehensive_integration_test()
    
    # Generate integration test report
    with open('system_integration_report.json', 'w') as f:
        import json
        json.dump(comprehensive_results, f, indent=2)

if __name__ == '__main__':
    main()
