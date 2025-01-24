import os
import secrets
import hashlib
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

class AdvancedEncryptionModule:
    def __init__(self, 
                 encryption_key: Optional[str] = None, 
                 salt_length: int = 16):
        """
        Initialize Advanced Encryption Module
        
        Args:
            encryption_key: Optional custom encryption key
            salt_length: Length of cryptographic salt
        """
        self.salt_length = salt_length
        self.encryption_key = self._generate_encryption_key(encryption_key)
        self.fernet_instance = Fernet(self.encryption_key)
    
    def _generate_encryption_key(self, custom_key: Optional[str] = None) -> bytes:
        """
        Generate a secure encryption key
        
        Args:
            custom_key: Optional user-provided key
        
        Returns:
            Base64 encoded Fernet key
        """
        if custom_key:
            # Derive key from custom input
            salt = secrets.token_bytes(self.salt_length)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(
                kdf.derive(custom_key.encode())
            )
        else:
            # Generate completely random key
            key = Fernet.generate_key()
        
        return key
    
    def encrypt_data(self, data: Dict[str, Any]) -> str:
        """
        Encrypt sensitive data
        
        Args:
            data: Dictionary of data to encrypt
        
        Returns:
            Encrypted token
        """
        import json
        
        # Convert data to JSON string
        data_json = json.dumps(data).encode()
        
        # Encrypt data
        encrypted_data = self.fernet_instance.encrypt(data_json)
        
        return encrypted_data.decode('utf-8')
    
    def decrypt_data(self, encrypted_token: str) -> Dict[str, Any]:
        """
        Decrypt sensitive data
        
        Args:
            encrypted_token: Encrypted data token
        
        Returns:
            Decrypted data dictionary
        """
        import json
        
        # Decrypt data
        decrypted_data = self.fernet_instance.decrypt(
            encrypted_token.encode('utf-8')
        )
        
        # Convert back to dictionary
        return json.loads(decrypted_data.decode('utf-8'))
    
    def generate_secure_hash(self, data: str, iterations: int = 100000) -> str:
        """
        Generate a secure cryptographic hash
        
        Args:
            data: Data to hash
            iterations: Number of hash iterations
        
        Returns:
            Secure hash string
        """
        salt = secrets.token_bytes(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
            backend=default_backend()
        )
        
        key = kdf.derive(data.encode())
        
        # Combine salt and hash for storage
        return base64.urlsafe_b64encode(salt + key).decode('utf-8')
    
    def verify_secure_hash(self, original_data: str, stored_hash: str) -> bool:
        """
        Verify a secure hash
        
        Args:
            original_data: Original data to verify
            stored_hash: Previously generated hash
        
        Returns:
            Boolean indicating hash verification
        """
        try:
            # Decode stored hash
            decoded_hash = base64.urlsafe_b64decode(stored_hash.encode('utf-8'))
            
            # Extract salt and key
            salt = decoded_hash[:16]
            original_key = decoded_hash[16:]
            
            # Recreate KDF
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            
            # Derive key from original data
            derived_key = kdf.derive(original_data.encode())
            
            return secrets.compare_digest(derived_key, original_key)
        
        except Exception:
            return False

def main():
    """
    Demonstration of Advanced Encryption Module
    """
    # Initialize encryption module
    encryption_module = AdvancedEncryptionModule()
    
    # Sample sensitive data
    sensitive_data = {
        'user_id': 'user123',
        'investment_amount': 50000,
        'risk_profile': 'moderate'
    }
    
    # Encrypt data
    encrypted_token = encryption_module.encrypt_data(sensitive_data)
    print(f"Encrypted Token: {encrypted_token}")
    
    # Decrypt data
    decrypted_data = encryption_module.decrypt_data(encrypted_token)
    print(f"Decrypted Data: {decrypted_data}")
    
    # Hash generation and verification
    password = "secure_password_123"
    password_hash = encryption_module.generate_secure_hash(password)
    
    print(f"Password Hash: {password_hash}")
    print(f"Hash Verification: {encryption_module.verify_secure_hash(password, password_hash)}")

if __name__ == '__main__':
    main()
