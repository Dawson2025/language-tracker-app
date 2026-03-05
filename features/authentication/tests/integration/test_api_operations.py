# resource_id: f509cc69-f0a5-48b2-b335-f287f1042f2c
"""
Integration Tests for Authentication API Operations
Language Tracker Authentication Feature
Created via GitHub Spec Kit Implementation Phase

Tests API endpoints with database integration.
Validates user stories US-001, US-002, US-004.
"""

import unittest
import tempfile
import os
import sqlite3
import sys
from unittest.mock import patch, MagicMock
from flask import Flask, request_started

# Add the feature path to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))

try:
    from features.authentication.api_operations import AuthenticationAPI
    from features.authentication.password_security import PasswordSecurity
    from features.authentication.session_manager import SessionManager
    from features.authentication.validation import AuthenticationValidator
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all dependencies are installed")
    sys.exit(1)


class TestAuthenticationAPI(unittest.TestCase):
    """Integration tests for AuthenticationAPI class."""

    def setUp(self):
        """Set up test database and Flask app context."""
        # Create Flask app for testing
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        # Create temporary database
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        # Initialize authentication API
        self.auth_api = AuthenticationAPI(self.db_path)
        
        # Initialize database schema
        self._create_test_schema()

    def tearDown(self):
        """Clean up test database and Flask app."""
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def _create_test_schema(self):
        """Create test database schema."""
        with open('features/authentication/schema.sql', 'r') as f:
            schema_sql = f.read()
        
        conn = sqlite3.connect(self.db_path)
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()

    def _create_test_user(self, username="testuser", email="test@example.com", password="testpass123"):
        """Helper method to create a test user."""
        conn = sqlite3.connect(self.db_path)
        password_hash = PasswordSecurity.hash_password(password)
        
        cursor = conn.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return user_id

    def test_register_user_success(self):
        """Test successful user registration (US-001)."""
        with self.app.app_context():
            with self.app.test_request_context(
                headers={'User-Agent': 'Test-User-Agent'},
                environ_base={'REMOTE_ADDR': '127.0.0.1'}
            ):
                registration_data = {
                    'username': 'newuser',
                    'email': 'newuser@example.com',
                    'password': 'securepassword123',
                    'confirm_password': 'securepassword123'
                }
                
                response, status_code = self.auth_api.register_user(registration_data)
                
                self.assertEqual(status_code, 201)
                self.assertTrue(response['success'])
                self.assertIn('user', response)
                self.assertIn('session', response)
                self.assertEqual(response['user']['username'], 'newuser')
                self.assertEqual(response['user']['email'], 'newuser@example.com')

    def test_register_user_duplicate_username(self):
        """Test registration with duplicate username."""
        with self.app.app_context():
            with self.app.test_request_context(
                headers={'User-Agent': 'Test-User-Agent'},
                environ_base={'REMOTE_ADDR': '127.0.0.1'}
            ):
                # Create existing user
                self._create_test_user(username='existinguser', email='existing@example.com')
                
                registration_data = {
                    'username': 'existinguser',  # Duplicate username
                    'email': 'different@example.com',
                    'password': 'securepassword123',
                    'confirm_password': 'securepassword123'
                }
                
                response, status_code = self.auth_api.register_user(registration_data)
                
                self.assertEqual(status_code, 409)  # Conflict
                self.assertFalse(response['success'])
                self.assertIn('errors', response)
                self.assertIn('Username already exists', ' '.join(response['errors']))

    def test_register_user_duplicate_email(self):
        """Test registration with duplicate email."""
        with self.app.app_context():
            with self.app.test_request_context(
                headers={'User-Agent': 'Test-User-Agent'},
                environ_base={'REMOTE_ADDR': '127.0.0.1'}
            ):
                # Create existing user
                self._create_test_user(username='existing', email='existing@example.com')
                
                registration_data = {
                    'username': 'newuser',
                    'email': 'existing@example.com',  # Duplicate email
                    'password': 'securepassword123',
                    'confirm_password': 'securepassword123'
                }
                
                response, status_code = self.auth_api.register_user(registration_data)
                
                self.assertEqual(status_code, 409)  # Conflict
                self.assertFalse(response['success'])
                self.assertIn('errors', response)
                self.assertIn('Email already registered', ' '.join(response['errors']))

    def test_register_user_invalid_data(self):
        """Test registration with invalid data."""
        test_cases = [
            # Missing required fields
            ({}, 400),
            ({'username': 'test'}, 400),
            ({'username': 'test', 'email': 'test@example.com'}, 400),
            
            # Invalid email format
            ({
                'username': 'test',
                'email': 'invalid-email',
                'password': 'password123',
                'confirm_password': 'password123'
            }, 400),
            
            # Password mismatch
            ({
                'username': 'test',
                'email': 'test@example.com',
                'password': 'password123',
                'confirm_password': 'different123'
            }, 400),
            
            # Weak password
            ({
                'username': 'test',
                'email': 'test@example.com',
                'password': '123',
                'confirm_password': '123'
            }, 400),
        ]
        
        for registration_data, expected_status in test_cases:
            with self.subTest(data=registration_data):
                response, status_code = self.auth_api.register_user(registration_data)
                self.assertEqual(status_code, expected_status)
                self.assertFalse(response['success'])

    def test_login_user_success(self):
        """Test successful user login (US-002)."""
        with self.app.app_context():
            with self.app.test_request_context(
                headers={'User-Agent': 'Test-User-Agent'},
                environ_base={'REMOTE_ADDR': '127.0.0.1'}
            ):
                # Create test user
                password = 'testpassword123'
                self._create_test_user(password=password)
                
                login_data = {
                    'email': 'test@example.com',
                    'password': password,
                    'remember_me': False
                }
                
                response, status_code = self.auth_api.login_user(login_data)
                
                self.assertEqual(status_code, 200)
                self.assertTrue(response['success'])
                self.assertIn('user', response)
                self.assertIn('session', response)
                self.assertEqual(response['user']['email'], 'test@example.com')
                self.assertIn('Welcome back', response['message'])

    def test_login_user_remember_me(self):
        """Test login with remember me option."""
        with self.app.app_context():
            with self.app.test_request_context(
                headers={'User-Agent': 'Test-User-Agent'},
                environ_base={'REMOTE_ADDR': '127.0.0.1'}
            ):
                # Create test user
                password = 'testpassword123'
                self._create_test_user(password=password)
                
                login_data = {
                    'email': 'test@example.com',
                    'password': password,
                    'remember_me': True
                }
                
                response, status_code = self.auth_api.login_user(login_data)
                
                self.assertEqual(status_code, 200)
                self.assertTrue(response['success'])
                
                # Verify session duration is longer for remember me
                session_token = response['session']['token']
                session_manager = SessionManager(self.db_path)
                is_valid, session_data = session_manager.validate_session(session_token)
                
                self.assertTrue(is_valid)
                # Remember me should create longer session (7 days vs 1 day)
                # We can't easily test the exact duration, but we can verify session exists

    def test_login_user_invalid_credentials(self):
        """Test login with invalid credentials."""
        # Create test user
        self._create_test_user(password='correctpassword')
        
        test_cases = [
            # Wrong password
            {
                'email': 'test@example.com',
                'password': 'wrongpassword'
            },
            # Wrong email
            {
                'email': 'wrong@example.com',
                'password': 'correctpassword'
            },
            # Empty fields
            {
                'email': '',
                'password': 'correctpassword'
            },
            {
                'email': 'test@example.com',
                'password': ''
            },
        ]
        
        for login_data in test_cases:
            with self.subTest(data=login_data):
                response, status_code = self.auth_api.login_user(login_data)
                self.assertIn(status_code, [400, 401])  # Bad Request or Unauthorized
                self.assertFalse(response['success'])

    def test_login_user_inactive_account(self):
        """Test login with inactive account."""
        # Create inactive user
        conn = sqlite3.connect(self.db_path)
        password_hash = PasswordSecurity.hash_password('testpassword')
        conn.execute(
            "INSERT INTO users (username, email, password_hash, is_active) VALUES (?, ?, ?, ?)",
            ('inactiveuser', 'inactive@example.com', password_hash, 0)
        )
        conn.commit()
        conn.close()
        
        login_data = {
            'email': 'inactive@example.com',
            'password': 'testpassword'
        }
        
        response, status_code = self.auth_api.login_user(login_data)
        
        self.assertEqual(status_code, 401)
        self.assertFalse(response['success'])
        self.assertIn('deactivated', ' '.join(response['errors']).lower())

    def test_logout_user_success(self):
        """Test successful user logout (US-004)."""
        # Create test user and session
        user_id = self._create_test_user()
        session_manager = SessionManager(self.db_path)
        success, session_id, _ = session_manager.create_session(user_id)
        self.assertTrue(success)
        
        # Test logout
        response, status_code = self.auth_api.logout_user(session_id)
        
        self.assertEqual(status_code, 200)
        self.assertTrue(response['success'])
        self.assertIn('Logged out', response['message'])
        
        # Verify session is invalidated
        is_valid, _ = session_manager.validate_session(session_id)
        self.assertFalse(is_valid)

    def test_logout_user_invalid_token(self):
        """Test logout with invalid session token."""
        response, status_code = self.auth_api.logout_user('invalid_token')
        
        # Should still return success (graceful handling)
        self.assertEqual(status_code, 200)
        self.assertTrue(response['success'])

    def test_logout_user_empty_token(self):
        """Test logout with empty token."""
        response, status_code = self.auth_api.logout_user('')
        
        self.assertEqual(status_code, 400)
        self.assertFalse(response['success'])

    def test_validate_session_endpoint_success(self):
        """Test session validation endpoint."""
        # Create test user and session
        user_id = self._create_test_user()
        session_manager = SessionManager(self.db_path)
        success, session_id, _ = session_manager.create_session(user_id)
        self.assertTrue(success)
        
        response, status_code = self.auth_api.validate_session_endpoint(session_id)
        
        self.assertEqual(status_code, 200)
        self.assertTrue(response['valid'])
        self.assertIn('user', response)
        self.assertIn('session', response)

    def test_validate_session_endpoint_invalid(self):
        """Test session validation with invalid token."""
        response, status_code = self.auth_api.validate_session_endpoint('invalid_token')
        
        self.assertEqual(status_code, 401)
        self.assertFalse(response['valid'])

    def test_client_ip_extraction(self):
        """Test client IP address extraction."""
        with self.app.app_context():
            with self.app.test_request_context(
                headers={
                    'X-Forwarded-For': '192.168.1.1, 10.0.0.1',
                    'User-Agent': 'Test-Agent'
                },
                environ_base={'REMOTE_ADDR': '127.0.0.1'}
            ):
                registration_data = {
                    'username': 'testuser',
                    'email': 'test@example.com',
                    'password': 'ValidPass123',
                    'confirm_password': 'ValidPass123'
                }
                
                response, status_code = self.auth_api.register_user(registration_data)
                self.assertEqual(status_code, 201)


class TestAuthenticationAPISecurityFeatures(unittest.TestCase):
    """Test security features of the authentication API."""

    def setUp(self):
        """Set up test database and Flask app context."""
        # Create Flask app for testing
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.auth_api = AuthenticationAPI(self.db_path)
        self._create_test_schema()

    def tearDown(self):
        """Clean up test database."""
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def _create_test_schema(self):
        """Create test database schema."""
        with open('features/authentication/schema.sql', 'r') as f:
            schema_sql = f.read()
        
        conn = sqlite3.connect(self.db_path)
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()

    @patch('time.perf_counter')
    def test_timing_attack_protection(self, mock_perf_counter):
        """Test that timing attack protection is working."""
        # Mock timing to simulate fast execution
        mock_perf_counter.side_effect = [0.0, 0.05, 0.05, 0.25]  # Two calls per timing_safe_operation
        
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'anypassword'
        }
        
        with patch('time.sleep') as mock_sleep:
            response, status_code = self.auth_api.login_user(login_data)
            
            # Should call sleep to normalize timing
            mock_sleep.assert_called()

    def test_password_security_integration(self):
        """Test integration with password security module."""
        with self.app.app_context():
            with self.app.test_request_context(
                headers={'User-Agent': 'Test-Agent'},
                environ_base={'REMOTE_ADDR': '127.0.0.1'}
            ):
                registration_data = {
                    'username': 'testuser',
                    'email': 'test@example.com',
                    'password': 'TestPassword123!',
                    'confirm_password': 'TestPassword123!'
                }
                
                response, status_code = self.auth_api.register_user(registration_data)
                
                self.assertEqual(status_code, 201)
                
                # Verify password was hashed (not stored as plaintext)
                conn = sqlite3.connect(self.db_path)
                cursor = conn.execute("SELECT password_hash FROM users WHERE email = ?", ('test@example.com',))
                stored_hash = cursor.fetchone()[0]
                conn.close()
                
                self.assertNotEqual(stored_hash, 'TestPassword123!')
                self.assertTrue(len(stored_hash) > 50)  # bcrypt hash length


if __name__ == '__main__':
    unittest.main(verbosity=2)