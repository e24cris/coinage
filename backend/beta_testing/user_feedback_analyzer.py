import os
import json
import logging
from typing import Dict, Any, List
from datetime import datetime

class UserFeedbackAnalyzer:
    def __init__(
        self, 
        feedback_dir: str = 'beta_feedback',
        log_level: int = logging.INFO
    ):
        """
        Initialize User Feedback Analyzer
        
        Args:
            feedback_dir: Directory containing feedback files
            log_level: Logging level
        """
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        self.feedback_dir = feedback_dir
        os.makedirs(feedback_dir, exist_ok=True)
    
    def load_feedback_files(self) -> List[Dict[str, Any]]:
        """
        Load all feedback files
        
        Returns:
            List of feedback dictionaries
        """
        feedback_files = [
            f for f in os.listdir(self.feedback_dir) 
            if f.endswith('_feedback.json')
        ]
        
        feedback_data = []
        for filename in feedback_files:
            filepath = os.path.join(self.feedback_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    feedback_data.append(json.load(f))
            except Exception as e:
                self.logger.error(f"Error reading {filename}: {e}")
        
        return feedback_data
    
    def aggregate_feedback_metrics(self) -> Dict[str, Any]:
        """
        Aggregate and analyze feedback metrics
        
        Returns:
            Comprehensive feedback analysis
        """
        feedback_data = self.load_feedback_files()
        
        aggregated_metrics = {
            'total_submissions': len(feedback_data),
            'submission_dates': [],
            'category_scores': {
                'user_experience': {},
                'feature_functionality': {},
                'performance': {},
                'ml_predictions': {},
                'security': {},
                'overall_satisfaction': {}
            },
            'qualitative_insights': {
                'positive_comments': [],
                'improvement_suggestions': []
            }
        }
        
        for feedback in feedback_data:
            # Track submission dates
            aggregated_metrics['submission_dates'].append(
                datetime.fromisoformat(feedback['timestamp'])
            )
            
            # Aggregate category scores
            for category, metrics in feedback['categories'].items():
                for metric, value in metrics.items():
                    if value is not None:
                        if metric not in aggregated_metrics['category_scores'][category]:
                            aggregated_metrics['category_scores'][category][metric] = []
                        aggregated_metrics['category_scores'][category][metric].append(value)
            
            # Collect qualitative insights
            comments = feedback['categories']['overall_satisfaction'].get('additional_comments')
            if comments:
                if any(positive_word in comments.lower() for positive_word in ['great', 'awesome', 'love']):
                    aggregated_metrics['qualitative_insights']['positive_comments'].append(comments)
                else:
                    aggregated_metrics['qualitative_insights']['improvement_suggestions'].append(comments)
        
        # Calculate average scores
        for category, metrics in aggregated_metrics['category_scores'].items():
            for metric, values in metrics.items():
                metrics[metric] = {
                    'average': round(sum(values) / len(values), 2) if values else None,
                    'total_responses': len(values)
                }
        
        return aggregated_metrics
    
    def generate_feedback_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive feedback report
        
        Returns:
            Detailed feedback analysis report
        """
        aggregated_metrics = self.aggregate_feedback_metrics()
        
        feedback_report = {
            'report_generated_at': datetime.now().isoformat(),
            'total_submissions': aggregated_metrics['total_submissions'],
            'feedback_timeline': {
                'first_submission': min(aggregated_metrics['submission_dates']),
                'last_submission': max(aggregated_metrics['submission_dates'])
            },
            'category_performance': {},
            'key_insights': {
                'top_positive_aspects': [],
                'primary_improvement_areas': []
            }
        }
        
        # Analyze category performance
        for category, metrics in aggregated_metrics['category_scores'].items():
            category_scores = [
                score['average'] 
                for metric_data in metrics.values() 
                for score in [metric_data] 
                if score['average'] is not None
            ]
            
            feedback_report['category_performance'][category] = {
                'average_score': round(sum(category_scores) / len(category_scores), 2) if category_scores else None,
                'metrics': metrics
            }
        
        # Identify top positive aspects and improvement areas
        for category, performance in feedback_report['category_performance'].items():
            if performance['average_score'] and performance['average_score'] >= 4:
                feedback_report['key_insights']['top_positive_aspects'].append({
                    'category': category,
                    'score': performance['average_score']
                })
            elif performance['average_score'] and performance['average_score'] < 3:
                feedback_report['key_insights']['primary_improvement_areas'].append({
                    'category': category,
                    'score': performance['average_score']
                })
        
        # Add qualitative insights
        feedback_report['qualitative_insights'] = {
            'positive_comments': aggregated_metrics['qualitative_insights']['positive_comments'][:5],
            'improvement_suggestions': aggregated_metrics['qualitative_insights']['improvement_suggestions'][:5]
        }
        
        return feedback_report
    
    def save_feedback_report(self, report: Dict[str, Any], filename: str = None):
        """
        Save feedback report to file
        
        Args:
            report: Feedback report dictionary
            filename: Optional custom filename
        """
        if not filename:
            filename = f"feedback_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.feedback_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Feedback report saved: {filepath}")

def main():
    """
    Demonstrate User Feedback Analyzer
    """
    feedback_analyzer = UserFeedbackAnalyzer()
    
    # Generate and save feedback report
    feedback_report = feedback_analyzer.generate_feedback_report()
    feedback_analyzer.save_feedback_report(feedback_report)
    
    # Print key insights
    print("Feedback Report Key Insights:")
    print(json.dumps(feedback_report, indent=2))

if __name__ == '__main__':
    main()
