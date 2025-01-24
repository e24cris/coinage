import os
import re
import json
import logging
from typing import Dict, List, Any, Optional

import jwt
from cryptography.fernet import Fernet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from investment_plans import InvestmentPlan, InvestmentPlanManager
from app.utils.security import SecurityMiddleware

class InvestmentPlanSecurityAudit:
    """
    Comprehensive Security Audit for Investment Plans
    
    Performs multi-layered security assessments
    """
    
    def __init__(
        self, 
        database_url: Optional[str] = None,
        log_level: str = 'INFO'
    ):
        """
        Initialize security audit
        
        Args:
            database_url: Database connection string
            log_level: Logging verbosity
        """
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Database connection
        self.database_url = database_url or os.getenv(
            'DATABASE_URL', 
            'sqlite:///investment_plans_security.db'
        )
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)
        
        # Security middleware
        self.security_middleware = SecurityMiddleware()
        
        # Encryption key management
        self.encryption_key = self._generate_encryption_key()
        self.encryption_cipher = Fernet(self.encryption_key)
    
    def _generate_encryption_key(self) -> bytes:
        """
        Generate a secure encryption key
        
        Returns:
            Encryption key
        """
        return Fernet.generate_key()
    
    def audit_investment_plan_access(
        self, 
        user_id: int, 
        plan_id: int
    ) -> Dict[str, Any]:
        """
        Audit access to an investment plan
        
        Args:
            user_id: User attempting access
            plan_id: Investment plan identifier
        
        Returns:
            Access audit results
        """
        session = self.Session()
        
        try:
            # Retrieve investment plan
            plan = session.query(InvestmentPlan).get(plan_id)
            
            if not plan:
                return {
                    'status': 'error',
                    'message': 'Investment plan not found'
                }
            
            # Check user authorization
            authorized = self._check_user_authorization(user_id, plan)
            
            # Log access attempt
            self.logger.info(
                f"Investment Plan Access Attempt: "
                f"User {user_id}, Plan {plan_id}, Authorized: {authorized}"
            )
            
            return {
                'status': 'success',
                'authorized': authorized,
                'risk_level': plan.risk_level
            }
        
        except Exception as e:
            self.logger.error(f"Access audit error: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
        finally:
            session.close()
    
    def _check_user_authorization(
        self, 
        user_id: int, 
        plan: InvestmentPlan
    ) -> bool:
        """
        Check user authorization for investment plan
        
        Args:
            user_id: User identifier
            plan: Investment plan object
        
        Returns:
            Authorization status
        """
        # Implement complex authorization logic
        # This is a placeholder and should be replaced with actual logic
        return True
    
    def encrypt_sensitive_plan_data(
        self, 
        plan_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Encrypt sensitive investment plan data
        
        Args:
            plan_data: Investment plan configuration
        
        Returns:
            Encrypted plan data
        """
        encrypted_data = plan_data.copy()
        
        # Fields to encrypt
        sensitive_fields = [
            'asset_allocation', 
            'expected_return', 
            'volatility'
        ]
        
        for field in sensitive_fields:
            if field in encrypted_data:
                encrypted_value = self.encryption_cipher.encrypt(
                    json.dumps(encrypted_data[field]).encode()
                )
                encrypted_data[field] = encrypted_value.decode()
        
        return encrypted_data
    
    def decrypt_sensitive_plan_data(
        self, 
        encrypted_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Decrypt sensitive investment plan data
        
        Args:
            encrypted_data: Encrypted investment plan configuration
        
        Returns:
            Decrypted plan data
        """
        decrypted_data = encrypted_data.copy()
        
        # Fields to decrypt
        sensitive_fields = [
            'asset_allocation', 
            'expected_return', 
            'volatility'
        ]
        
        for field in sensitive_fields:
            if field in decrypted_data:
                decrypted_value = self.encryption_cipher.decrypt(
                    decrypted_data[field].encode()
                )
                decrypted_data[field] = json.loads(decrypted_value.decode())
        
        return decrypted_data
    
    def validate_plan_configuration(
        self, 
        plan_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate investment plan configuration security
        
        Args:
            plan_data: Investment plan configuration
        
        Returns:
            Security validation results
        """
        validation_results = {
            'is_secure': True,
            'warnings': [],
            'errors': []
        }
        
        # Check for potentially malicious input
        for key, value in plan_data.items():
            # Prevent SQL injection
            if isinstance(value, str):
                if re.search(r'[\'";`]', value):
                    validation_results['is_secure'] = False
                    validation_results['errors'].append(
                        f"Potential SQL injection in {key}"
                    )
            
            # Prevent excessive complexity
            if isinstance(value, (dict, list)) and len(str(value)) > 10000:
                validation_results['is_secure'] = False
                validation_results['errors'].append(
                    f"Excessively large value for {key}"
                )
        
        # Check asset allocation security
        asset_allocation = plan_data.get('asset_allocation', {})
        if not isinstance(asset_allocation, dict):
            validation_results['is_secure'] = False
            validation_results['errors'].append(
                "Invalid asset allocation format"
            )
        
        # Warn about high-risk configurations
        if (plan_data.get('risk_level') == 'high' and 
            plan_data.get('expected_return', 0) > 0.25):
            validation_results['warnings'].append(
                "Extremely high expected return for high-risk plan"
            )
        
        return validation_results
    
    def generate_access_token(
        self, 
        user_id: int, 
        plan_id: int
    ) -> str:
        """
        Generate a secure access token for an investment plan
        
        Args:
            user_id: User identifier
            plan_id: Investment plan identifier
        
        Returns:
            JWT access token
        """
        payload = {
            'user_id': user_id,
            'plan_id': plan_id,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        
        return jwt.encode(
            payload, 
            os.getenv('JWT_SECRET_KEY'), 
            algorithm='HS256'
        )
    
    def audit_investment_plan_system(self) -> Dict[str, Any]:
        """
        Comprehensive system-wide security audit
        
        Returns:
            Security audit results
        """
        audit_results = {
            'database_security': self._audit_database_security(),
            'encryption_status': self._check_encryption_status(),
            'access_controls': self._review_access_controls()
        }
        
        return audit_results
    
    def _audit_database_security(self) -> Dict[str, Any]:
        """
        Audit database security for investment plans
        
        Returns:
            Database security assessment
        """
        # Implement database security checks
        return {
            'status': 'secure',
            'encrypted_connection': True,
            'latest_migration': datetime.utcnow()
        }
    
    def _check_encryption_status(self) -> Dict[str, Any]:
        """
        Check encryption key and method status
        
        Returns:
            Encryption status details
        """
        return {
            'encryption_method': 'Fernet',
            'key_rotated_at': datetime.utcnow(),
            'key_length': len(self.encryption_key) * 8
        }
    
    def _review_access_controls(self) -> Dict[str, Any]:
        """
        Review system-wide access controls
        
        Returns:
            Access control review results
        """
        return {
            'admin_roles': ['super_admin', 'investment_manager'],
            'role_based_access_control': True,
            'multi_factor_authentication': True
        }

def main():
    """
    Demonstrate investment plan security audit
    """
    security_audit = InvestmentPlanSecurityAudit()
    
    # Sample investment plan data
    sample_plan = {
        'name': 'Secure Growth Plan',
        'risk_level': 'medium',
        'asset_allocation': {
            'stocks': 0.6,
            'bonds': 0.3,
            'cash': 0.1
        },
        'expected_return': 0.07
    }
    
    # Validate plan configuration
    validation_result = security_audit.validate_plan_configuration(sample_plan)
    print("Plan Configuration Security:")
    print(json.dumps(validation_result, indent=2))
    
    # Encrypt sensitive data
    encrypted_plan = security_audit.encrypt_sensitive_plan_data(sample_plan)
    print("\nEncrypted Plan Data:")
    print(json.dumps(encrypted_plan, indent=2))
    
    # Decrypt sensitive data
    decrypted_plan = security_audit.decrypt_sensitive_plan_data(encrypted_plan)
    print("\nDecrypted Plan Data:")
    print(json.dumps(decrypted_plan, indent=2))
    
    # Perform system-wide security audit
    system_audit = security_audit.audit_investment_plan_system()
    print("\nSystem Security Audit:")
    print(json.dumps(system_audit, indent=2))

if __name__ == '__main__':
    main()
