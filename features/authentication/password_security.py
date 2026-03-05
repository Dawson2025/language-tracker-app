# resource_id: b84ba57c-453d-4302-95e9-491f96830e45
"""
Password Security Module
Language Tracker Authentication Feature
Created via GitHub Spec Kit Implementation Phase

Provides secure password hashing, verification, and validation utilities.
Implements timing-safe operations to prevent timing attacks.
"""

import bcrypt
import re
import secrets
import time
from typing import Tuple, Dict, Any
from functools import wraps


class PasswordSecurity:
    """
    Secure password operations with timing attack protection.
    """
    
    # Password strength requirements
    MIN_LENGTH = 6
    REQUIRE_UPPERCASE = False  # Flexible for user convenience
    REQUIRE_LOWERCASE = False
    REQUIRE_NUMBERS = False
    REQUIRE_SPECIAL = False
    
    # bcrypt cost factor (higher = more secure but slower)
    BCRYPT_ROUNDS = 12
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt with salt.
        
        Args:
            password: Plain text password to hash
            
        Returns:
            str: Bcrypt hash string
            
        Raises:
            ValueError: If password is invalid
        """
        if not password or len(password.strip()) == 0:
            raise ValueError("Password cannot be empty")
            
        # Convert to bytes and hash
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=PasswordSecurity.BCRYPT_ROUNDS)
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash using timing-safe comparison.
        
        Args:
            password: Plain text password to verify
            password_hash: Bcrypt hash to verify against
            
        Returns:
            bool: True if password matches hash
        """
        if not password or not password_hash:
            return False
            
        try:
            password_bytes = password.encode('utf-8')
            hash_bytes = password_hash.encode('utf-8')
            
            # bcrypt.checkpw is timing-safe
            return bcrypt.checkpw(password_bytes, hash_bytes)
            
        except (ValueError, TypeError, UnicodeError):
            # Invalid hash format or encoding issues
            return False
    
    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate password strength against requirements.
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple[bool, Dict]: (is_valid, validation_details)
        """
        if not password:
            return False, {
                "valid": False,
                "errors": ["Password is required"],
                "score": 0
            }
        
        errors = []
        score = 0
        
        # Length check
        if len(password) < PasswordSecurity.MIN_LENGTH:
            errors.append(f"Password must be at least {PasswordSecurity.MIN_LENGTH} characters long")
        else:
            score += 1
        
        # Character type checks (flexible requirements)
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        
        # Score bonus for character diversity
        if has_upper:
            score += 1
        if has_lower:
            score += 1
        if has_digit:
            score += 1
        if has_special:
            score += 1
        
        # Length bonus
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        
        # Common password check (basic)
        common_passwords = {
            'password', '123456', '123456789', 'qwerty', 'abc123',
            'password123', '123123', 'admin', 'letmein', 'welcome'
        }
        if password.lower() in common_passwords:
            errors.append("Password is too common")
            score = max(0, score - 2)
        
        is_valid = len(errors) == 0
        
        return is_valid, {
            "valid": is_valid,
            "errors": errors,
            "score": min(score, 6),  # Max score of 6
            "strength": _get_strength_label(score),
            "has_uppercase": has_upper,
            "has_lowercase": has_lower,
            "has_numbers": has_digit,
            "has_special": has_special
        }
    
    @staticmethod
    def generate_session_token() -> str:
        """
        Generate a cryptographically secure session token.
        
        Returns:
            str: 64-character hexadecimal session token
        """
        return secrets.token_hex(32)
    
    @staticmethod
    def timing_safe_compare(a: str, b: str) -> bool:
        """
        Compare two strings in constant time to prevent timing attacks.
        
        Args:
            a: First string
            b: Second string
            
        Returns:
            bool: True if strings are equal
        """
        if not isinstance(a, str) or not isinstance(b, str):
            return False
        
        return secrets.compare_digest(a, b)


def _get_strength_label(score: int) -> str:
    """
    Convert numeric password strength score to descriptive label.
    
    Args:
        score: Password strength score (0-6)
        
    Returns:
        str: Strength description
    """
    if score <= 1:
        return "Very Weak"
    elif score <= 2:
        return "Weak"
    elif score <= 3:
        return "Fair"
    elif score <= 4:
        return "Good"
    elif score <= 5:
        return "Strong"
    else:
        return "Very Strong"


def timing_safe_operation(min_time_ms: int = 100):
    """
    Decorator to ensure operations take at least a minimum amount of time.
    Helps prevent timing attacks by normalizing response times.
    
    Args:
        min_time_ms: Minimum execution time in milliseconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            remaining_ms = max(0, min_time_ms - elapsed_ms)
            
            if remaining_ms > 0:
                time.sleep(remaining_ms / 1000)
            
            return result
        return wrapper
    return decorator


# Example usage and testing functions
if __name__ == "__main__":
    # Example usage for testing
    password = "MySecurePassword123!"
    
    # Hash password
    hashed = PasswordSecurity.hash_password(password)
    print(f"Hashed password: {hashed}")
    
    # Verify password
    is_valid = PasswordSecurity.verify_password(password, hashed)
    print(f"Password verification: {is_valid}")
    
    # Check strength
    strength_valid, strength_info = PasswordSecurity.validate_password_strength(password)
    print(f"Password strength: {strength_info}")
    
    # Generate session token
    token = PasswordSecurity.generate_session_token()
    print(f"Session token: {token}")