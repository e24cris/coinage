import os
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List

class BetaTestingFeedbackSystem:
    def __init__(self, 
                 feedback_storage_path: str = 'beta_feedback',
                 log_level: int = logging.INFO):
        """
        Initialize Beta Testing Feedback Collection System
        
        Args:
            feedback_storage_path: Directory to store feedback
            log_level: Logging level
        """
        # Configure logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Ensure feedback storage directory exists
        self.feedback_storage_path = feedback_storage_path
        os.makedirs(feedback_storage_path, exist_ok=True)
        
        # Feedback categories
        self.feedback_categories = [
            'user_experience',
            'feature_functionality',
            'performance',
            'ml_predictions',
            'security',
            'overall_satisfaction'
        ]
    
    def generate_feedback_form(self, tester_id: str = None) -> Dict[str, Any]:
        """
        Generate a structured feedback form
        
        Args:
            tester_id: Optional tester identifier
        
        Returns:
            Structured feedback form
        """
        feedback_form = {
            'feedback_id': str(uuid.uuid4()),
            'tester_id': tester_id or str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'categories': {category: {} for category in self.feedback_categories}
        }
        
        # Add detailed questions for each category
        feedback_form['categories']['user_experience'] = {
            'interface_intuitiveness': None,
            'navigation_ease': None,
            'overall_design_rating': None
        }
        
        feedback_form['categories']['feature_functionality'] = {
            'investment_plan_creation': None,
            'ai_recommendation_accuracy': None,
            'feature_completeness': None
        }
        
        feedback_form['categories']['performance'] = {
            'platform_speed': None,
            'prediction_model_responsiveness': None,
            'loading_times': None
        }
        
        feedback_form['categories']['ml_predictions'] = {
            'prediction_accuracy': None,
            'risk_assessment_reliability': None,
            'recommendation_usefulness': None
        }
        
        feedback_form['categories']['security'] = {
            'authentication_process': None,
            'data_privacy_confidence': None,
            'security_features_rating': None
        }
        
        feedback_form['categories']['overall_satisfaction'] = {
            'likelihood_to_recommend': None,
            'would_pay_for_service': None,
            'additional_comments': None
        }
        
        return feedback_form
    
    def submit_feedback(self, feedback: Dict[str, Any]) -> bool:
        """
        Submit and store beta testing feedback
        
        Args:
            feedback: Completed feedback form
        
        Returns:
            Boolean indicating successful submission
        """
        try:
            # Validate feedback
            if not self._validate_feedback(feedback):
                self.logger.warning("Invalid feedback submission")
                return False
            
            # Generate unique filename
            filename = f"{feedback['feedback_id']}_feedback.json"
            filepath = os.path.join(self.feedback_storage_path, filename)
            
            # Store feedback
            import json
            with open(filepath, 'w') as f:
                json.dump(feedback, f, indent=2)
            
            self.logger.info(f"Feedback submitted: {feedback['feedback_id']}")
            return True
        
        except Exception as e:
            self.logger.error(f"Feedback submission error: {e}")
            return False
    
    def _validate_feedback(self, feedback: Dict[str, Any]) -> bool:
        """
        Validate feedback form completeness and structure
        
        Args:
            feedback: Feedback form to validate
        
        Returns:
            Boolean indicating valid feedback
        """
        # Check required fields
        required_fields = ['feedback_id', 'tester_id', 'timestamp', 'categories']
        if not all(field in feedback for field in required_fields):
            return False
        
        # Validate categories
        for category in self.feedback_categories:
            if category not in feedback['categories']:
                return False
        
        return True
    
    def analyze_feedback(self) -> Dict[str, Any]:
        """
        Analyze collected beta testing feedback
        
        Returns:
            Comprehensive feedback analysis
        """
        import json
        
        feedback_files = [
            f for f in os.listdir(self.feedback_storage_path) 
            if f.endswith('_feedback.json')
        ]
        
        analysis_results = {
            'total_submissions': len(feedback_files),
            'category_insights': {category: {} for category in self.feedback_categories}
        }
        
        for filename in feedback_files:
            filepath = os.path.join(self.feedback_storage_path, filename)
            
            with open(filepath, 'r') as f:
                feedback = json.load(f)
            
            # Aggregate insights
            for category, metrics in feedback['categories'].items():
                for metric, value in metrics.items():
                    if value is not None:
                        if metric not in analysis_results['category_insights'][category]:
                            analysis_results['category_insights'][category][metric] = []
                        analysis_results['category_insights'][category][metric].append(value)
        
        # Calculate averages
        for category, metrics in analysis_results['category_insights'].items():
            for metric, values in metrics.items():
                analysis_results['category_insights'][category][metric] = {
                    'average': sum(values) / len(values) if values else None,
                    'total_responses': len(values)
                }
        
        return analysis_results

def main():
    """
    Demonstration of Beta Testing Feedback Collection System
    """
    # Initialize feedback system
    feedback_system = BetaTestingFeedbackSystem()
    
    # Generate feedback form
    feedback_form = feedback_system.generate_feedback_form()
    
    # Simulate feedback submission
    feedback_form['categories']['user_experience']['interface_intuitiveness'] = 4
    feedback_form['categories']['user_experience']['navigation_ease'] = 5
    feedback_form['categories']['overall_satisfaction']['additional_comments'] = "Great platform with potential for improvement!"
    
    # Submit feedback
    submission_result = feedback_system.submit_feedback(feedback_form)
    print("Feedback Submission Result:", submission_result)
    
    # Analyze feedback
    feedback_analysis = feedback_system.analyze_feedback()
    print("Feedback Analysis:", feedback_analysis)

if __name__ == '__main__':
    main()
