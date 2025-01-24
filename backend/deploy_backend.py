import os
import logging
import subprocess
import sys

def setup_backend_services():
    """
    Set up and configure backend services
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    services = [
        {'name': 'API Server', 'command': ['flask', 'run']},
        {'name': 'ML Prediction Service', 'command': ['python', 'ml/prediction_service.py']},
        {'name': 'Background Task Worker', 'command': ['celery', '-A', 'tasks', 'worker']}
    ]
    
    for service in services:
        try:
            logger.info(f"Starting {service['name']}")
            subprocess.Popen(service['command'])
            logger.info(f"{service['name']} started successfully")
        except Exception as e:
            logger.error(f"Failed to start {service['name']}: {e}")
            return False
    
    return True

def main():
    """
    Main backend deployment script
    """
    result = setup_backend_services()
    sys.exit(0 if result else 1)

if __name__ == '__main__':
    main()
