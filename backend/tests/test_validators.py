import unittest
from app.utils.validators import InputValidator

class TestInputValidator(unittest.TestCase):
    def test_valid_username(self):
        valid_usernames = ['john_doe', 'alice123', 'user_name']
        for username in valid_usernames:
            is_valid, error = InputValidator.validate_username(username)
            self.assertTrue(is_valid, f"Username {username} should be valid")

    def test_invalid_username(self):
        invalid_usernames = ['', '12user', 'user name', 'a'*21]
        for username in invalid_usernames:
            is_valid, error = InputValidator.validate_username(username)
            self.assertFalse(is_valid, f"Username {username} should be invalid")

    def test_valid_email(self):
        valid_emails = ['test@example.com', 'user.name@domain.co.uk']
        for email in valid_emails:
            is_valid, result = InputValidator.validate_email(email)
            self.assertTrue(is_valid, f"Email {email} should be valid")

    def test_invalid_email(self):
        invalid_emails = ['invalid_email', 'test@', '@domain.com']
        for email in invalid_emails:
            is_valid, error = InputValidator.validate_email(email)
            self.assertFalse(is_valid, f"Email {email} should be invalid")

    def test_password_strength(self):
        strong_passwords = [
            'StrongP@ssw0rd!', 
            'Secure_Password123!', 
            'ComplexPass2024#'
        ]
        for password in strong_passwords:
            is_valid, error = InputValidator.validate_password(password)
            self.assertTrue(is_valid, f"Password {password} should be valid")

    def test_weak_passwords(self):
        weak_passwords = [
            'short', 
            'onlylowercase', 
            'ONLYUPPERCASE', 
            '12345678'
        ]
        for password in weak_passwords:
            is_valid, error = InputValidator.validate_password(password)
            self.assertFalse(is_valid, f"Password {password} should be invalid")

if __name__ == '__main__':
    unittest.main()
