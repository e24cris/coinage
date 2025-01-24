import os
import json
import logging
from typing import Dict, List, Any, Optional

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InvestmentPlanUserAcceptanceTester:
    """
    Comprehensive User Acceptance Testing Framework
    for Investment Plan Selection and Management
    """
    
    def __init__(
        self, 
        base_url: str = 'http://localhost:3000',
        browser: str = 'chrome',
        log_level: str = 'INFO'
    ):
        """
        Initialize UAT framework
        
        Args:
            base_url: Application base URL
            browser: Web browser for testing
            log_level: Logging verbosity
        """
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Web driver configuration
        self.base_url = base_url
        self.browser = self._setup_browser(browser)
        
        # Test configuration
        self.test_scenarios = self._load_test_scenarios()
    
    def _setup_browser(self, browser: str):
        """
        Set up web driver
        
        Args:
            browser: Browser name
        
        Returns:
            Configured web driver
        """
        if browser.lower() == 'chrome':
            return webdriver.Chrome()
        elif browser.lower() == 'firefox':
            return webdriver.Firefox()
        elif browser.lower() == 'safari':
            return webdriver.Safari()
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    def _load_test_scenarios(self) -> List[Dict[str, Any]]:
        """
        Load user acceptance test scenarios
        
        Returns:
            List of test scenarios
        """
        scenarios_path = os.path.join(
            os.path.dirname(__file__), 
            'investment_plan_scenarios.json'
        )
        
        with open(scenarios_path, 'r') as f:
            return json.load(f)
    
    def run_investment_plan_scenarios(self) -> List[Dict[str, Any]]:
        """
        Execute investment plan user acceptance scenarios
        
        Returns:
            Test execution results
        """
        results = []
        
        for scenario in self.test_scenarios:
            try:
                result = self._execute_scenario(scenario)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Scenario failed: {scenario['name']}")
                results.append({
                    'scenario': scenario['name'],
                    'status': 'failed',
                    'error': str(e)
                })
        
        return results
    
    def _execute_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single user acceptance scenario
        
        Args:
            scenario: Test scenario configuration
        
        Returns:
            Scenario execution result
        """
        self.browser.get(f"{self.base_url}{scenario['url']}")
        
        # Scenario-specific actions
        actions = scenario.get('actions', [])
        
        for action in actions:
            self._perform_action(action)
        
        # Validate expectations
        expectations = scenario.get('expectations', [])
        validation_results = self._validate_expectations(expectations)
        
        return {
            'scenario': scenario['name'],
            'status': 'passed' if all(validation_results.values()) else 'failed',
            'validation_results': validation_results
        }
    
    def _perform_action(self, action: Dict[str, Any]) -> None:
        """
        Perform a user interaction action
        
        Args:
            action: Action configuration
        """
        action_type = action.get('type')
        selector = action.get('selector')
        value = action.get('value')
        
        # Wait for element
        element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        
        if action_type == 'click':
            element.click()
        elif action_type == 'input':
            element.clear()
            element.send_keys(value)
        elif action_type == 'select':
            element.find_element(By.XPATH, f"//option[text()='{value}']").click()
    
    def _validate_expectations(
        self, 
        expectations: List[Dict[str, Any]]
    ) -> Dict[str, bool]:
        """
        Validate scenario expectations
        
        Args:
            expectations: List of expectation configurations
        
        Returns:
            Validation results
        """
        validation_results = {}
        
        for expectation in expectations:
            selector = expectation.get('selector')
            expected_value = expectation.get('value')
            validation_type = expectation.get('type', 'text')
            
            element = self.browser.find_element(By.CSS_SELECTOR, selector)
            
            if validation_type == 'text':
                actual_value = element.text
                validation_results[selector] = actual_value == expected_value
            elif validation_type == 'attribute':
                attribute = expectation.get('attribute', 'value')
                actual_value = element.get_attribute(attribute)
                validation_results[selector] = actual_value == expected_value
        
        return validation_results
    
    def generate_test_report(
        self, 
        results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive test report
        
        Args:
            results: Scenario execution results
        
        Returns:
            Test report summary
        """
        passed_scenarios = [r for r in results if r['status'] == 'passed']
        failed_scenarios = [r for r in results if r['status'] == 'failed']
        
        return {
            'total_scenarios': len(results),
            'passed_scenarios': len(passed_scenarios),
            'failed_scenarios': len(failed_scenarios),
            'pass_rate': len(passed_scenarios) / len(results) * 100,
            'detailed_results': results
        }
    
    def cleanup(self) -> None:
        """
        Clean up testing resources
        """
        self.browser.quit()

def main():
    """
    Run investment plan user acceptance tests
    """
    uat_tester = InvestmentPlanUserAcceptanceTester()
    
    try:
        # Run test scenarios
        test_results = uat_tester.run_investment_plan_scenarios()
        
        # Generate test report
        test_report = uat_tester.generate_test_report(test_results)
        
        # Print test report
        print("Investment Plan UAT Test Report:")
        print(json.dumps(test_report, indent=2))
    
    finally:
        # Always clean up resources
        uat_tester.cleanup()

if __name__ == '__main__':
    main()
