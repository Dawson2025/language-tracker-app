# resource_id: c74fd508-34bc-407c-bd85-76f6e6f57e83
"""
Authentication Input Validation
Language Tracker Authentication Feature
Created via GitHub Spec Kit Implementation Phase

Provides comprehensive input validation for authentication forms and data.
Implements security best practices and user-friendly error messaging.
"""

import re
from typing import Dict, List, Any, Tuple


class AuthenticationValidator:
    """
    Validates authentication-related input data with security focus.
    """
    
    # Validation patterns
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    USERNAME_PATTERN = re.compile(
        r'^[a-zA-Z0-9_-]{3,50}$'
    )
    
    # Security constraints
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 50
    MAX_EMAIL_LENGTH = 255
    MAX_PASSWORD_LENGTH = 128  # Prevent DoS via extremely long passwords
    
    # Forbidden usernames (security/system reserved)
    FORBIDDEN_USERNAMES = {
        'admin', 'administrator', 'root', 'system', 'api', 'www', 'mail',
        'ftp', 'web', 'support', 'help', 'info', 'contact', 'service',
        'user', 'guest', 'anonymous', 'null', 'undefined', 'test'
    }
    
    def validate_registration_data(
        self,
        username: str,
        email: str,
        password: str,
        confirm_password: str
    ) -> Dict[str, Any]:
        """
        Validate complete registration form data.
        
        Args:
            username: Username to validate
            email: Email address to validate
            password: Password to validate
            confirm_password: Password confirmation to validate
            
        Returns:
            Dict: Validation result with errors and field-specific feedback
        """
        errors = []
        field_errors = {}
        
        # Validate username
        username_valid, username_errors = self.validate_username(username)
        if not username_valid:
            errors.extend(username_errors)
            field_errors['username'] = username_errors
        
        # Validate email
        email_valid, email_errors = self.validate_email(email)
        if not email_valid:
            errors.extend(email_errors)
            field_errors['email'] = email_errors
        
        # Validate password
        password_valid, password_errors = self.validate_password_basic(password)
        if not password_valid:
            errors.extend(password_errors)
            field_errors['password'] = password_errors
        
        # Validate password confirmation
        if password and confirm_password:
            if password != confirm_password:
                confirm_error = "Passwords do not match"
                errors.append(confirm_error)
                field_errors['confirm_password'] = [confirm_error]
        elif not confirm_password:
            confirm_error = "Password confirmation is required"
            errors.append(confirm_error)
            field_errors['confirm_password'] = [confirm_error]
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'field_errors': field_errors
        }
    
    def validate_username(self, username: str) -> Tuple[bool, List[str]]:
        """
        Validate username according to rules and constraints.
        
        Args:
            username: Username to validate
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, error_messages)
        """
        if not username:
            return False, ["Username is required"]
        
        errors = []
        
        # Length validation
        if len(username) < self.MIN_USERNAME_LENGTH:
            errors.append(f"Username must be at least {self.MIN_USERNAME_LENGTH} characters long")
        elif len(username) > self.MAX_USERNAME_LENGTH:
            errors.append(f"Username cannot exceed {self.MAX_USERNAME_LENGTH} characters")
        
        # Pattern validation (alphanumeric, underscore, hyphen only)
        if not self.USERNAME_PATTERN.match(username):
            errors.append("Username can only contain letters, numbers, underscores, and hyphens")
        
        # Forbidden usernames check
        if username.lower() in self.FORBIDDEN_USERNAMES:
            errors.append("This username is not available")
        
        # Additional security checks
        if username.lower().startswith(('admin', 'root', 'system')):
            errors.append("Username cannot start with reserved words")
        
        return len(errors) == 0, errors
    
    def validate_email(self, email: str) -> Tuple[bool, List[str]]:
        """
        Validate email address format and constraints.
        
        Args:
            email: Email address to validate
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, error_messages)
        """
        if not email:
            return False, ["Email address is required"]
        
        errors = []
        
        # Length validation
        if len(email) > self.MAX_EMAIL_LENGTH:
            errors.append(f"Email address cannot exceed {self.MAX_EMAIL_LENGTH} characters")
        
        # Format validation
        if not self.is_valid_email(email):
            errors.append("Please enter a valid email address")
        
        # Additional checks
        if email.count('@') != 1:
            errors.append("Email address must contain exactly one @ symbol")
        
        # Check for suspicious patterns
        if '..' in email or email.startswith('.') or email.endswith('.'):
            errors.append("Email address format is invalid")
        
        return len(errors) == 0, errors
    
    def validate_password_basic(self, password: str) -> Tuple[bool, List[str]]:
        """
        Basic password validation (length and security).
        Note: Detailed strength validation is handled by PasswordSecurity class.
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, error_messages)
        """
        if not password:
            return False, ["Password is required"]
        
        errors = []
        
        # Length validation
        if len(password) > self.MAX_PASSWORD_LENGTH:
            errors.append(f"Password cannot exceed {self.MAX_PASSWORD_LENGTH} characters")
        
        # Basic security checks
        if password.strip() != password:
            errors.append("Password cannot start or end with spaces")
        
        # Check for null bytes or control characters
        if '\x00' in password or any(ord(c) < 32 and c not in '\t\n\r' for c in password):
            errors.append("Password contains invalid characters")
        
        return len(errors) == 0, errors
    
    def is_valid_email(self, email: str) -> bool:
        """
        Check if email format is valid using regex pattern.
        
        Args:
            email: Email address to check
            
        Returns:
            bool: True if email format is valid
        """
        if not email or len(email) > self.MAX_EMAIL_LENGTH:
            return False
        
        return bool(self.EMAIL_PATTERN.match(email))
    
    def validate_login_data(self, email: str, password: str) -> Dict[str, Any]:
        """
        Validate login form data.
        
        Args:
            email: Email address
            password: Password
            
        Returns:
            Dict: Validation result
        """
        errors = []
        field_errors = {}
        
        # Basic required field validation
        if not email:
            email_error = "Email address is required"
            errors.append(email_error)
            field_errors['email'] = [email_error]
        elif not self.is_valid_email(email):
            email_error = "Please enter a valid email address"
            errors.append(email_error)
            field_errors['email'] = [email_error]
        
        if not password:
            password_error = "Password is required"
            errors.append(password_error)
            field_errors['password'] = [password_error]
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'field_errors': field_errors
        }
    
    def sanitize_input(self, input_str: str, max_length: int = None) -> str:
        """
        Sanitize input string by removing dangerous characters.
        
        Args:
            input_str: String to sanitize
            max_length: Maximum allowed length
            
        Returns:
            str: Sanitized string
        """
        if not input_str:
            return ""
        
        # Remove null bytes and control characters (except tab, newline, carriage return)
        sanitized = ''.join(c for c in input_str if ord(c) >= 32 or c in '\t\n\r')
        
        # Strip whitespace
        sanitized = sanitized.strip()
        
        # Limit length if specified
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized
    
    def validate_session_token(self, token: str) -> bool:
        """
        Validate session token format.
        
        Args:
            token: Session token to validate
            
        Returns:
            bool: True if token format is valid
        """
        if not token:
            return False
        
        # Session tokens should be 64-character hexadecimal strings
        if len(token) != 64:
            return False
        
        # Check if all characters are valid hexadecimal
        try:
            int(token, 16)
            return True
        except ValueError:
            return False
    
    def check_suspicious_input(self, data: Dict[str, Any]) -> List[str]:
        """
        Check for suspicious input patterns that might indicate attacks.
        
        Args:
            data: Input data dictionary to check
            
        Returns:
            List[str]: List of security warnings
        """
        warnings = []
        
        for field, value in data.items():
            if not isinstance(value, str):
                continue
            
            value_lower = value.lower()
            
            # Check for SQL injection patterns
            sql_patterns = [
                'union select', 'drop table', 'delete from', 'insert into',
                'update set', '--', '/*', '*/', 'xp_', 'sp_'
            ]
            if any(pattern in value_lower for pattern in sql_patterns):
                warnings.append(f"Suspicious SQL pattern detected in {field}")
            
            # Check for XSS patterns
            xss_patterns = [
                '<script', 'javascript:', 'onload=', 'onerror=', 'onclick='
            ]
            if any(pattern in value_lower for pattern in xss_patterns):
                warnings.append(f"Suspicious script pattern detected in {field}")
            
            # Check for path traversal
            if '../' in value or '..\\' in value:
                warnings.append(f"Path traversal pattern detected in {field}")
            
            # Check for extremely long inputs (potential DoS)
            if len(value) > 1000:  # Reasonable limit for form fields
                warnings.append(f"Extremely long input detected in {field}")
        
        return warnings
    
    def validate_password_change_data(
        self,
        current_password: str,
        new_password: str,
        confirm_new_password: str
    ) -> Dict[str, Any]:
        """
        Validate password change form data.
        
        Args:
            current_password: Current password
            new_password: New password
            confirm_new_password: New password confirmation
            
        Returns:
            Dict: Validation result
        """
        errors = []
        field_errors = {}
        
        # Validate current password
        if not current_password:
            current_error = "Current password is required"
            errors.append(current_error)
            field_errors['current_password'] = [current_error]
        
        # Validate new password
        new_password_valid, new_password_errors = self.validate_password_basic(new_password)
        if not new_password_valid:
            errors.extend(new_password_errors)
            field_errors['new_password'] = new_password_errors
        
        # Validate confirmation
        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                confirm_error = "New passwords do not match"
                errors.append(confirm_error)
                field_errors['confirm_new_password'] = [confirm_error]
        elif not confirm_new_password:
            confirm_error = "New password confirmation is required"
            errors.append(confirm_error)
            field_errors['confirm_new_password'] = [confirm_error]
        
        # Check if new password is different from current
        if current_password and new_password and current_password == new_password:
            same_password_error = "New password must be different from current password"
            errors.append(same_password_error)
            field_errors['new_password'] = field_errors.get('new_password', []) + [same_password_error]
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'field_errors': field_errors
        }