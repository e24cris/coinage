import os
import sys
import subprocess
import json
import re
from datetime import datetime
import logging
from typing import Dict, List, Any

import jwt
from cryptography.fernet import Fernet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class SecurityAudit:
    def __init__(self, project_path):
        self.project_path = project_path
        self.audit_report = {
            'timestamp': datetime.now().isoformat(),
            'vulnerabilities': [],
            'recommendations': []
        }

    def check_dependencies(self):
        """
        Check for known vulnerabilities in dependencies
        """
        try:
            # Run safety to check for known vulnerabilities
            result = subprocess.run(
                ['safety', 'check', '--output', 'json'], 
                capture_output=True, 
                text=True
            )
            
            vulnerabilities = json.loads(result.stdout)
            
            for vuln in vulnerabilities:
                self.audit_report['vulnerabilities'].append({
                    'package': vuln['package'],
                    'version': vuln['version'],
                    'vulnerability_id': vuln['vulnerability_id'],
                    'description': vuln['description']
                })
        
        except Exception as e:
            self.audit_report['vulnerabilities'].append({
                'error': f"Dependency check failed: {str(e)}"
            })

    def check_secret_exposure(self):
        """
        Scan for potential secret exposure in code
        """
        try:
            # Use Trufflehog for secret scanning
            result = subprocess.run(
                ['trufflehog', 'filesystem', self.project_path], 
                capture_output=True, 
                text=True
            )
            
            secrets_found = re.findall(r'Verified secret', result.stdout)
            
            if secrets_found:
                self.audit_report['vulnerabilities'].append({
                    'type': 'Secret Exposure',
                    'count': len(secrets_found)
                })
        
        except Exception as e:
            self.audit_report['vulnerabilities'].append({
                'error': f"Secret scanning failed: {str(e)}"
            })

    def check_code_quality(self):
        """
        Run static code analysis
        """
        try:
            # Use Bandit for Python security analysis
            result = subprocess.run(
                ['bandit', '-r', self.project_path, '-f', 'json'], 
                capture_output=True, 
                text=True
            )
            
            bandit_report = json.loads(result.stdout)
            
            for issue in bandit_report.get('results', []):
                self.audit_report['vulnerabilities'].append({
                    'type': 'Code Quality',
                    'filename': issue['filename'],
                    'line_number': issue['line_number'],
                    'issue_severity': issue['issue_severity'],
                    'issue_text': issue['issue_text']
                })
        
        except Exception as e:
            self.audit_report['vulnerabilities'].append({
                'error': f"Code quality check failed: {str(e)}"
            })

    def generate_recommendations(self):
        """
        Generate security recommendations based on findings
        """
        recommendations = []
        
        if self.audit_report['vulnerabilities']:
            recommendations.append("Update dependencies to latest secure versions")
            recommendations.append("Review and rotate exposed secrets")
            recommendations.append("Address static code analysis findings")
        
        self.audit_report['recommendations'] = recommendations

    def save_report(self, output_file='security_audit_report.json'):
        """
        Save audit report to file
        """
        with open(output_file, 'w') as f:
            json.dump(self.audit_report, f, indent=2)
        
        print(f"Security audit report saved to {output_file}")

    def run_full_audit(self):
        """
        Perform comprehensive security audit
        """
        self.check_dependencies()
        self.check_secret_exposure()
        self.check_code_quality()
        self.generate_recommendations()
        self.save_report()

class ComprehensiveSecurity:
    def __init__(self, database_url: str = None):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
        self.database_url = database_url or os.getenv('DATABASE_URL')
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)
    
    def generate_encryption_key(self) -> bytes:
        """Generate a new encryption key"""
        return Fernet.generate_key()
    
    def validate_jwt_configuration(self) -> Dict[str, Any]:
        """Check JWT configuration security"""
        jwt_secret = os.getenv('JWT_SECRET')
        
        if not jwt_secret or len(jwt_secret) < 32:
            return {
                'status': 'CRITICAL',
                'message': 'Weak or missing JWT secret'
            }
        
        return {
            'status': 'PASS',
            'message': 'JWT configuration secure'
        }
    
    def check_database_encryption(self) -> Dict[str, Any]:
        """Verify database connection encryption"""
        try:
            with self.Session() as session:
                # Dummy query to test connection
                session.execute('SELECT 1')
            
            if not self.database_url.startswith('postgresql+ssl'):
                return {
                    'status': 'WARNING',
                    'message': 'Database connection not using SSL'
                }
            
            return {
                'status': 'PASS',
                'message': 'Database connection secure'
            }
        except Exception as e:
            return {
                'status': 'CRITICAL',
                'message': f'Database connection error: {e}'
            }
    
    def audit_access_controls(self) -> List[Dict[str, Any]]:
        """Comprehensive access control audit"""
        audits = []
        
        # Check environment variables
        sensitive_vars = ['SECRET_KEY', 'DATABASE_URL', 'JWT_SECRET']
        for var in sensitive_vars:
            if not os.getenv(var):
                audits.append({
                    'status': 'CRITICAL',
                    'message': f'Missing sensitive environment variable: {var}'
                })
        
        return audits
    
    def generate_security_report(self) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        jwt_check = self.validate_jwt_configuration()
        db_check = self.check_database_encryption()
        access_audits = self.audit_access_controls()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'jwt_configuration': jwt_check,
            'database_security': db_check,
            'access_control_audits': access_audits,
            'overall_status': 'PASS' if all(
                check['status'] == 'PASS' for check in [jwt_check, db_check]
            ) else 'FAIL'
        }

def main():
    project_path = os.path.dirname(os.path.abspath(__file__))
    audit = SecurityAudit(project_path)
    audit.run_full_audit()

    security_auditor = ComprehensiveSecurity()
    report = security_auditor.generate_security_report()
    
    # Log report
    logging.info("Comprehensive Security Audit Report:")
    logging.info(report)
    
    # Optional: Write report to file
    with open('comprehensive_security_audit_report.json', 'w') as f:
        import json
        json.dump(report, f, indent=2)

if __name__ == '__main__':
    main()
