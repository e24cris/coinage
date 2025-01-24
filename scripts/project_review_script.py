import os
import json
import logging
from typing import Dict, List, Any

class ProjectReviewManager:
    def __init__(self, checklist_path='PROJECT_REVIEW_CHECKLIST.md'):
        """
        Initialize Project Review Manager
        
        Args:
            checklist_path: Path to review checklist
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        self.checklist_path = checklist_path
        self.review_results_dir = 'review_results'
        os.makedirs(self.review_results_dir, exist_ok=True)
    
    def parse_checklist(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Parse markdown checklist
        
        Returns:
            Structured checklist
        """
        with open(self.checklist_path, 'r') as f:
            content = f.read()
        
        sections = {}
        current_section = None
        
        for line in content.split('\n'):
            if line.startswith('### '):
                current_section = line.strip('### ').strip()
                sections[current_section] = []
            elif line.startswith('- [ ]'):
                if current_section:
                    sections[current_section].append({
                        'task': line.strip('- [ ]').strip(),
                        'status': 'pending',
                        'notes': ''
                    })
        
        return sections
    
    def interactive_review(self, checklist: Dict[str, List[Dict[str, Any]]]):
        """
        Conduct interactive project review
        
        Args:
            checklist: Structured checklist
        """
        review_results = {}
        
        for section, tasks in checklist.items():
            print(f"\n🔍 Reviewing Section: {section}")
            review_results[section] = []
            
            for task in tasks:
                print(f"\nTask: {task['task']}")
                status = input("Status (✅ complete/❌ incomplete/🔍 needs review): ").strip()
                
                if status in ['✅', '❌', '🔍']:
                    task['status'] = status
                
                notes = input("Additional notes (optional): ").strip()
                task['notes'] = notes
                
                review_results[section].append(task)
        
        # Save review results
        results_file = os.path.join(
            self.review_results_dir, 
            f'project_review_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        
        with open(results_file, 'w') as f:
            json.dump(review_results, f, indent=2)
        
        self.logger.info(f"Review results saved to {results_file}")
        return review_results
    
    def generate_review_summary(self, review_results: Dict[str, List[Dict[str, Any]]]):
        """
        Generate review summary report
        
        Args:
            review_results: Completed review results
        """
        summary = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'pending_tasks': 0,
            'review_needed_tasks': 0,
            'section_status': {}
        }
        
        for section, tasks in review_results.items():
            section_summary = {
                'total_tasks': len(tasks),
                'completed_tasks': sum(1 for task in tasks if task['status'] == '✅'),
                'pending_tasks': sum(1 for task in tasks if task['status'] == '❌'),
                'review_needed_tasks': sum(1 for task in tasks if task['status'] == '🔍')
            }
            
            summary['total_tasks'] += section_summary['total_tasks']
            summary['completed_tasks'] += section_summary['completed_tasks']
            summary['pending_tasks'] += section_summary['pending_tasks']
            summary['review_needed_tasks'] += section_summary['review_needed_tasks']
            
            summary['section_status'][section] = section_summary
        
        # Calculate overall completion percentage
        summary['completion_percentage'] = (
            summary['completed_tasks'] / summary['total_tasks'] * 100 
            if summary['total_tasks'] > 0 else 0
        )
        
        # Save summary
        summary_file = os.path.join(
            self.review_results_dir, 
            f'review_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Print summary
        print("\n🏁 Project Review Summary")
        print(f"Total Tasks: {summary['total_tasks']}")
        print(f"Completed Tasks: {summary['completed_tasks']}")
        print(f"Pending Tasks: {summary['pending_tasks']}")
        print(f"Tasks Needing Review: {summary['review_needed_tasks']}")
        print(f"Completion Percentage: {summary['completion_percentage']:.2f}%")
        
        return summary

def main():
    """
    Run interactive project review
    """
    from datetime import datetime
    
    review_manager = ProjectReviewManager()
    
    # Parse checklist
    checklist = review_manager.parse_checklist()
    
    # Conduct interactive review
    review_results = review_manager.interactive_review(checklist)
    
    # Generate review summary
    review_summary = review_manager.generate_review_summary(review_results)

if __name__ == '__main__':
    main()
