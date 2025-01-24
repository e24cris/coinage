import os
import json
import logging
from typing import Dict, List, Any
from datetime import datetime

class FeaturePrioritizationFramework:
    def __init__(
        self, 
        feature_request_dir: str = 'feature_requests',
        log_level: int = logging.INFO
    ):
        """
        Initialize Feature Prioritization Framework
        
        Args:
            feature_request_dir: Directory to store feature requests
            log_level: Logging level
        """
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Ensure feature request directory exists
        os.makedirs(feature_request_dir, exist_ok=True)
        self.feature_request_dir = feature_request_dir
        
        # Predefined feature scoring criteria
        self.scoring_criteria = {
            'user_impact': {
                'low': 1,
                'medium': 3,
                'high': 5
            },
            'technical_complexity': {
                'low': 5,
                'medium': 3,
                'high': 1
            },
            'business_value': {
                'low': 1,
                'medium': 3,
                'high': 5
            },
            'implementation_effort': {
                'low': 5,
                'medium': 3,
                'high': 1
            }
        }
    
    def submit_feature_request(
        self, 
        feature_name: str, 
        description: str, 
        requester: str,
        user_impact: str = 'medium',
        technical_complexity: str = 'medium',
        business_value: str = 'medium',
        implementation_effort: str = 'medium'
    ) -> Dict[str, Any]:
        """
        Submit a new feature request
        
        Args:
            feature_name: Name of the feature
            description: Detailed feature description
            requester: User who submitted the request
            user_impact: Impact on user experience
            technical_complexity: Complexity of implementation
            business_value: Strategic value of feature
            implementation_effort: Resources required
        
        Returns:
            Feature request details
        """
        feature_request = {
            'feature_id': f"FEAT_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'feature_name': feature_name,
            'description': description,
            'requester': requester,
            'submission_date': datetime.now().isoformat(),
            'scoring': {
                'user_impact': {
                    'level': user_impact,
                    'score': self.scoring_criteria['user_impact'][user_impact]
                },
                'technical_complexity': {
                    'level': technical_complexity,
                    'score': self.scoring_criteria['technical_complexity'][technical_complexity]
                },
                'business_value': {
                    'level': business_value,
                    'score': self.scoring_criteria['business_value'][business_value]
                },
                'implementation_effort': {
                    'level': implementation_effort,
                    'score': self.scoring_criteria['implementation_effort'][implementation_effort]
                }
            },
            'status': 'pending'
        }
        
        # Calculate priority score
        feature_request['priority_score'] = self._calculate_priority_score(feature_request)
        
        # Save feature request
        filename = f"{feature_request['feature_id']}_feature_request.json"
        filepath = os.path.join(self.feature_request_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(feature_request, f, indent=2)
        
        self.logger.info(f"Feature request submitted: {feature_name}")
        return feature_request
    
    def _calculate_priority_score(self, feature_request: Dict[str, Any]) -> float:
        """
        Calculate feature priority score
        
        Args:
            feature_request: Feature request details
        
        Returns:
            Calculated priority score
        """
        scoring = feature_request['scoring']
        
        # Weighted scoring formula
        priority_score = (
            scoring['user_impact']['score'] * 0.3 +
            (6 - scoring['technical_complexity']['score']) * 0.2 +
            scoring['business_value']['score'] * 0.3 +
            (6 - scoring['implementation_effort']['score']) * 0.2
        )
        
        return round(priority_score, 2)
    
    def get_feature_requests(self, status: str = None) -> List[Dict[str, Any]]:
        """
        Retrieve feature requests
        
        Args:
            status: Optional status filter
        
        Returns:
            List of feature requests
        """
        feature_requests = []
        
        for filename in os.listdir(self.feature_request_dir):
            if filename.endswith('_feature_request.json'):
                filepath = os.path.join(self.feature_request_dir, filename)
                
                with open(filepath, 'r') as f:
                    feature_request = json.load(f)
                
                if status is None or feature_request['status'] == status:
                    feature_requests.append(feature_request)
        
        # Sort by priority score in descending order
        return sorted(
            feature_requests, 
            key=lambda x: x['priority_score'], 
            reverse=True
        )
    
    def update_feature_request_status(
        self, 
        feature_id: str, 
        new_status: str
    ) -> bool:
        """
        Update feature request status
        
        Args:
            feature_id: Feature request identifier
            new_status: New status value
        
        Returns:
            Boolean indicating successful update
        """
        for filename in os.listdir(self.feature_request_dir):
            if filename.endswith('_feature_request.json'):
                filepath = os.path.join(self.feature_request_dir, filename)
                
                with open(filepath, 'r') as f:
                    feature_request = json.load(f)
                
                if feature_request['feature_id'] == feature_id:
                    feature_request['status'] = new_status
                    
                    with open(filepath, 'w') as f:
                        json.dump(feature_request, f, indent=2)
                    
                    self.logger.info(f"Updated feature {feature_id} status to {new_status}")
                    return True
        
        return False
    
    def generate_feature_roadmap(self) -> Dict[str, Any]:
        """
        Generate feature roadmap based on priority
        
        Returns:
            Feature roadmap with prioritized features
        """
        feature_requests = self.get_feature_requests()
        
        roadmap = {
            'short_term': [],
            'medium_term': [],
            'long_term': []
        }
        
        for feature in feature_requests:
            if feature['priority_score'] >= 4.5:
                roadmap['short_term'].append(feature)
            elif feature['priority_score'] >= 3.5:
                roadmap['medium_term'].append(feature)
            else:
                roadmap['long_term'].append(feature)
        
        return roadmap

def main():
    """
    Demonstrate Feature Prioritization Framework
    """
    feature_manager = FeaturePrioritizationFramework()
    
    # Submit feature requests
    feature_manager.submit_feature_request(
        feature_name="Social Trading Integration",
        description="Enable users to follow and copy successful investors",
        requester="beta_tester_001",
        user_impact="high",
        business_value="high",
        technical_complexity="medium"
    )
    
    feature_manager.submit_feature_request(
        feature_name="Mobile App Development",
        description="Create mobile application for on-the-go investing",
        requester="beta_tester_002",
        user_impact="high",
        business_value="high",
        technical_complexity="high"
    )
    
    # Generate feature roadmap
    feature_roadmap = feature_manager.generate_feature_roadmap()
    
    # Save roadmap
    with open('feature_roadmap.json', 'w') as f:
        json.dump(feature_roadmap, f, indent=2)
    
    print("Feature Roadmap Generated:")
    print(json.dumps(feature_roadmap, indent=2))

if __name__ == '__main__':
    main()
