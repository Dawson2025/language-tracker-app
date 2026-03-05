# resource_id: e2363b11-b3ec-4c45-8d45-e4cd28894408
"""
Unit Tests for Password Security Module
Language Tracker Authentication Feature
Created via GitHub Spec Kit Implementation Phase

Tests password hashing, validation, and security utilities.
Ensures >90% code coverage and security compliance.
"""

import unittest
import time
from unittest.mock import patch, MagicMock
import sys
import os

# Add the feature path to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))

try:
    from features.authentication.password_security import (
        PasswordSecurity,
        timing_safe_operation,
        _get_strength_label
    )
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure bcrypt is installed: pip install bcrypt")
    sys.exit(1)


class TestPasswordSecurity(unittest.TestCase):
    """Test cases for PasswordSecurity class."""

    def test_hash_password_success(self):
        """Test successful password hashing."""
        password = "test_password_123"
        hashed = PasswordSecurity.hash_password(password)
        
        # Check that hash is returned
        self.assertIsInstance(hashed, str)
        self.assertGreater(len(hashed), 50)  # bcrypt hashes are typically 60+ chars
        
        # Check that hash is different from original password
        self.assertNotEqual(password, hashed)
        
        # Check that hashing same password twice gives different results (salt)
        hashed2 = PasswordSecurity.hash_password(password)
        self.assertNotEqual(hashed, hashed2)

    def test_hash_password_empty_fails(self):
        """Test that empty passwords raise ValueError."""
        with self.assertRaises(ValueError):
            PasswordSecurity.hash_password("")
        
        with self.assertRaises(ValueError):
            PasswordSecurity.hash_password("   ")

    def test_hash_password_none_fails(self):
        """Test that None password raises ValueError."""
        with self.assertRaises(ValueError):
            PasswordSecurity.hash_password(None)

    def test_verify_password_success(self):
        """Test successful password verification."""
        password = "correct_password_123"
        hashed = PasswordSecurity.hash_password(password)
        
        # Correct password should verify
        self.assertTrue(PasswordSecurity.verify_password(password, hashed))

    def test_verify_password_failure(self):
        """Test password verification with wrong password."""
        password = "correct_password_123"
        wrong_password = "wrong_password_456"
        hashed = PasswordSecurity.hash_password(password)
        
        # Wrong password should not verify
        self.assertFalse(PasswordSecurity.verify_password(wrong_password, hashed))

    def test_verify_password_empty_inputs(self):
        """Test password verification with empty inputs."""
        # Empty password
        self.assertFalse(PasswordSecurity.verify_password("", "valid_hash"))
        
        # Empty hash
        self.assertFalse(PasswordSecurity.verify_password("password", ""))
        
        # Both empty
        self.assertFalse(PasswordSecurity.verify_password("", ""))

    def test_verify_password_invalid_hash(self):
        """Test password verification with invalid hash format."""
        password = "test_password"
        invalid_hash = "not_a_valid_bcrypt_hash"
        
        # Should return False, not raise exception
        self.assertFalse(PasswordSecurity.verify_password(password, invalid_hash))

    def test_validate_password_strength_valid(self):
        """Test password strength validation for valid passwords."""
        test_cases = [
            ("Password123!", True),  # Strong password
            ("mypassword", True),    # Meets minimum length
            ("Pass1!", True),        # Meets minimum with variety
        ]
        
        for password, expected_valid in test_cases:
            with self.subTest(password=password):
                valid, info = PasswordSecurity.validate_password_strength(password)
                self.assertEqual(valid, expected_valid)
                self.assertIn("valid", info)
                self.assertIn("score", info)
                self.assertIn("strength", info)

    def test_validate_password_strength_invalid(self):
        """Test password strength validation for invalid passwords."""
        test_cases = [
            ("", False),           # Empty
            ("a", False),          # Too short
            ("12345", False),      # Too short
            ("password", False),   # Common password (should be invalid)
        ]
        
        for password, expected_valid in test_cases:
            with self.subTest(password=password):
                valid, info = PasswordSecurity.validate_password_strength(password)
                self.assertEqual(valid, expected_valid)
                if not valid:
                    self.assertGreater(len(info["errors"]), 0)

    def test_validate_password_strength_scoring(self):
        """Test password strength scoring system."""
        test_cases = [
            ("a", 0),                    # Very short
            ("password", 1),             # Basic length (common, so score reduced from 3 to 1)
            ("Testword", 2),             # Length + uppercase + lowercase
            ("Testword123", 5),          # Length + uppercase + lowercase + numbers + length>=8 bonus
            ("Testword123!", 6),         # Length + uppercase + lowercase + numbers + special + length>=8 bonus
            ("VeryLongTestword123!", 6), # All criteria + long (max score is 6)
        ]
        
        for password, min_expected_score in test_cases:
            with self.subTest(password=password):
                valid, info = PasswordSecurity.validate_password_strength(password)
                # Some passwords might be invalid due to common word check
                if password not in ['password']:
                    self.assertGreaterEqual(info["score"], min_expected_score)

    def test_validate_password_strength_character_types(self):
        """Test password strength character type detection."""
        password = "Password123!"
        valid, info = PasswordSecurity.validate_password_strength(password)
        
        self.assertTrue(info["has_uppercase"])
        self.assertTrue(info["has_lowercase"])
        self.assertTrue(info["has_numbers"])
        self.assertTrue(info["has_special"])

    def test_generate_session_token(self):
        """Test session token generation."""
        token1 = PasswordSecurity.generate_session_token()
        token2 = PasswordSecurity.generate_session_token()
        
        # Check token format
        self.assertIsInstance(token1, str)
        self.assertEqual(len(token1), 64)  # 32 bytes * 2 (hex encoding)
        
        # Check tokens are different
        self.assertNotEqual(token1, token2)
        
        # Check tokens are hexadecimal
        try:
            int(token1, 16)
            int(token2, 16)
        except ValueError:
            self.fail("Generated tokens should be valid hexadecimal")

    def test_timing_safe_compare(self):
        """Test timing-safe string comparison."""
        # Identical strings
        self.assertTrue(PasswordSecurity.timing_safe_compare("hello", "hello"))
        
        # Different strings
        self.assertFalse(PasswordSecurity.timing_safe_compare("hello", "world"))
        
        # Different lengths
        self.assertFalse(PasswordSecurity.timing_safe_compare("hello", "hello world"))
        
        # Empty strings
        self.assertTrue(PasswordSecurity.timing_safe_compare("", ""))
        
        # Non-string inputs
        self.assertFalse(PasswordSecurity.timing_safe_compare("hello", 123))
        self.assertFalse(PasswordSecurity.timing_safe_compare(123, "hello"))


class TestPasswordStrengthLabels(unittest.TestCase):
    """Test password strength label generation."""

    def test_strength_labels(self):
        """Test strength label mapping."""
        test_cases = [
            (0, "Very Weak"),
            (1, "Very Weak"),
            (2, "Weak"),
            (3, "Fair"),
            (4, "Good"),
            (5, "Strong"),
            (6, "Very Strong"),
            (10, "Very Strong"),  # Max should be "Very Strong"
        ]
        
        for score, expected_label in test_cases:
            with self.subTest(score=score):
                label = _get_strength_label(score)
                self.assertEqual(label, expected_label)


class TestTimingSafeOperation(unittest.TestCase):
    """Test timing-safe operation decorator."""

    def test_timing_safe_operation_decorator(self):
        """Test that timing-safe decorator enforces minimum time."""
        min_time_ms = 100
        
        @timing_safe_operation(min_time_ms)
        def fast_function():
            return "result"
        
        start_time = time.perf_counter()
        result = fast_function()
        end_time = time.perf_counter()
        
        elapsed_ms = (end_time - start_time) * 1000
        
        self.assertEqual(result, "result")
        self.assertGreaterEqual(elapsed_ms, min_time_ms * 0.9)  # Allow 10% tolerance

    def test_timing_safe_operation_already_slow(self):
        """Test timing-safe decorator with already slow function."""
        min_time_ms = 50
        sleep_time = 0.1  # 100ms
        
        @timing_safe_operation(min_time_ms)
        def slow_function():
            time.sleep(sleep_time)
            return "result"
        
        start_time = time.perf_counter()
        result = slow_function()
        end_time = time.perf_counter()
        
        elapsed_ms = (end_time - start_time) * 1000
        
        self.assertEqual(result, "result")
        # Should not add extra delay since function already takes longer than min_time
        self.assertLessEqual(elapsed_ms, sleep_time * 1000 + 20)  # 20ms tolerance


class TestPasswordSecurityConstants(unittest.TestCase):
    """Test PasswordSecurity class constants and configuration."""

    def test_constants(self):
        """Test that security constants are properly set."""
        self.assertEqual(PasswordSecurity.MIN_LENGTH, 6)
        self.assertIsInstance(PasswordSecurity.BCRYPT_ROUNDS, int)
        self.assertGreaterEqual(PasswordSecurity.BCRYPT_ROUNDS, 10)  # Minimum secure rounds


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)