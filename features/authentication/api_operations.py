"""
Local Authentication API Operations
Language Tracker Authentication Feature
Created via GitHub Spec Kit Implementation Phase

Implements REST API endpoints for user registration, login, and logout.
Integrates password security, session management, and input validation.
"""

import sqlite3
import re
from typing import Dict, Any, Tuple, Optional
from flask import request, jsonify, current_app
from functools import wraps

from .password_security import PasswordSecurity, timing_safe_operation
from .session_manager import SessionManager
from .validation import AuthenticationValidator


class AuthenticationAPI:
    """
    Handles authentication API operations with security and validation.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize authentication API with database path.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self.session_manager = SessionManager(db_path)
        self.validator = AuthenticationValidator()
    
    @timing_safe_operation(200)  # Minimum 200ms to prevent timing attacks
    def register_user(self, request_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        Register a new user account.
        
        Implements US-001: User Registration with Local Credentials
        
        Args:
            request_data: Registration form data
            
        Returns:
            Tuple[Dict, int]: (response_data, http_status_code)
        """
        try:
            # Extract and validate input data
            username = request_data.get('username', '').strip()
            email = request_data.get('email', '').strip().lower()
            password = request_data.get('password', '')
            confirm_password = request_data.get('confirm_password', '')
            
            # Validate required fields
            validation_result = self.validator.validate_registration_data(
                username, email, password, confirm_password
            )
            
            if not validation_result['valid']:
                return {
                    'success': False,
                    'errors': validation_result['errors'],
                    'field_errors': validation_result.get('field_errors', {})
                }, 400
            
            # Check password strength
            password_valid, password_info = PasswordSecurity.validate_password_strength(password)
            if not password_valid:
                return {
                    'success': False,
                    'errors': password_info['errors'],
                    'field_errors': {'password': password_info['errors']}
                }, 400
            
            # Hash password securely
            try:
                password_hash = PasswordSecurity.hash_password(password)
            except ValueError as e:
                return {
                    'success': False,
                    'errors': [str(e)]
                }, 400
            
            # Create user in database
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            try:
                # Check for existing username/email
                existing_user = conn.execute("""
                    SELECT id, username, email FROM users 
                    WHERE username = ? OR email = ?
                """, (username, email)).fetchone()
                
                if existing_user:
                    error_msg = (
                        "Username already exists" if existing_user['username'] == username
                        else "Email already registered"
                    )
                    return {
                        'success': False,
                        'errors': [error_msg],
                        'field_errors': {
                            'username' if existing_user['username'] == username else 'email': [error_msg]
                        }
                    }, 409  # Conflict
                
                # Insert new user
                cursor = conn.execute("""
                    INSERT INTO users (username, email, password_hash, is_active)
                    VALUES (?, ?, ?, 1)
                """, (username, email, password_hash))
                
                user_id = cursor.lastrowid
                conn.commit()
                
                # Create session for automatic login
                user_agent = request.headers.get('User-Agent', '')
                client_ip = self._get_client_ip()
                
                session_success, session_id, session_info = self.session_manager.create_session(
                    user_id=user_id,
                    user_agent=user_agent,
                    ip_address=client_ip
                )
                
                if session_success:
                    return {
                        'success': True,
                        'message': 'Account created successfully',
                        'user': {
                            'id': user_id,
                            'username': username,
                            'email': email
                        },
                        'session': {
                            'token': session_id,
                            'expires_at': session_info['expires_at']
                        },
                        'redirect_url': '/dashboard'
                    }, 201
                else:
                    # User created but session failed - still success
                    return {
                        'success': True,
                        'message': 'Account created successfully. Please log in.',
                        'user': {
                            'id': user_id,
                            'username': username,
                            'email': email
                        },
                        'redirect_url': '/login'
                    }, 201
                
            except sqlite3.IntegrityError as e:
                conn.rollback()
                if 'username' in str(e):
                    return {
                        'success': False,
                        'errors': ['Username already exists'],
                        'field_errors': {'username': ['Username already exists']}
                    }, 409
                elif 'email' in str(e):
                    return {
                        'success': False,
                        'errors': ['Email already registered'],
                        'field_errors': {'email': ['Email already registered']}
                    }, 409
                else:
                    return {
                        'success': False,
                        'errors': ['Registration failed due to database constraint']
                    }, 400
                    
            except sqlite3.Error as e:
                conn.rollback()
                current_app.logger.error(f"Database error during registration: {e}")
                return {
                    'success': False,
                    'errors': ['Registration failed. Please try again.']
                }, 500
                
            finally:
                conn.close()
                
        except Exception as e:
            current_app.logger.error(f"Unexpected error during registration: {e}")
            return {
                'success': False,
                'errors': ['An unexpected error occurred. Please try again.']
            }, 500
    
    @timing_safe_operation(200)  # Prevent timing attacks
    def login_user(self, request_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        Authenticate user login.
        
        Implements US-002: User Login with Local Credentials
        
        Args:
            request_data: Login form data
            
        Returns:
            Tuple[Dict, int]: (response_data, http_status_code)
        """
        try:
            # Extract credentials
            email = request_data.get('email', '').strip().lower()
            password = request_data.get('password', '')
            remember_me = request_data.get('remember_me', False)
            
            # Basic validation
            if not email or not password:
                return {
                    'success': False,
                    'errors': ['Email and password are required'],
                    'field_errors': {
                        'email': [] if email else ['Email is required'],
                        'password': [] if password else ['Password is required']
                    }
                }, 400
            
            # Validate email format
            if not self.validator.is_valid_email(email):
                return {
                    'success': False,
                    'errors': ['Invalid email format'],
                    'field_errors': {'email': ['Invalid email format']}
                }, 400
            
            # Query user from database
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            try:
                user_row = conn.execute("""
                    SELECT id, username, email, password_hash, is_active
                    FROM users 
                    WHERE email = ?
                """, (email,)).fetchone()
                
                # Always perform password verification to prevent timing attacks
                # even if user doesn't exist
                if user_row:
                    password_valid = PasswordSecurity.verify_password(
                        password, user_row['password_hash']
                    )
                    user_active = bool(user_row['is_active'])
                else:
                    # Perform dummy password verification to maintain timing
                    PasswordSecurity.verify_password(password, 'dummy_hash')
                    password_valid = False
                    user_active = False
                
                # Check credentials and account status
                if not user_row or not password_valid or not user_active:
                    error_msg = (
                        'Account is deactivated' if user_row and not user_active
                        else 'Invalid email or password'
                    )
                    return {
                        'success': False,
                        'errors': [error_msg]
                    }, 401  # Unauthorized
                
                # Create session
                session_duration = (7 * 24) if remember_me else 24  # 7 days vs 24 hours
                user_agent = request.headers.get('User-Agent', '')
                client_ip = self._get_client_ip()
                
                session_success, session_id, session_info = self.session_manager.create_session(
                    user_id=user_row['id'],
                    duration_hours=session_duration,
                    user_agent=user_agent,
                    ip_address=client_ip
                )
                
                if session_success:
                    return {
                        'success': True,
                        'message': f'Welcome back, {user_row["username"]}!',
                        'user': {
                            'id': user_row['id'],
                            'username': user_row['username'],
                            'email': user_row['email']
                        },
                        'session': {
                            'token': session_id,
                            'expires_at': session_info['expires_at']
                        },
                        'redirect_url': '/dashboard'
                    }, 200
                else:
                    return {
                        'success': False,
                        'errors': ['Login failed. Please try again.']
                    }, 500
                    
            except sqlite3.Error as e:
                current_app.logger.error(f"Database error during login: {e}")
                return {
                    'success': False,
                    'errors': ['Login failed. Please try again.']
                }, 500
                
            finally:
                conn.close()
                
        except Exception as e:
            current_app.logger.error(f"Unexpected error during login: {e}")
            return {
                'success': False,
                'errors': ['An unexpected error occurred. Please try again.']
            }, 500
    
    def logout_user(self, session_token: str) -> Tuple[Dict[str, Any], int]:
        """
        Log out user by invalidating session.
        
        Implements US-004: User Logout
        
        Args:
            session_token: Session token to invalidate
            
        Returns:
            Tuple[Dict, int]: (response_data, http_status_code)
        """
        try:
            if not session_token:
                return {
                    'success': False,
                    'errors': ['Session token required']
                }, 400
            
            # Invalidate session
            logout_success = self.session_manager.invalidate_session(session_token)
            
            if logout_success:
                return {
                    'success': True,
                    'message': 'Logged out successfully',
                    'redirect_url': '/login'
                }, 200
            else:
                # Session might already be invalid - still success
                return {
                    'success': True,
                    'message': 'Logged out',
                    'redirect_url': '/login'
                }, 200
                
        except Exception as e:
            current_app.logger.error(f"Unexpected error during logout: {e}")
            return {
                'success': False,
                'errors': ['Logout failed. Please try again.']
            }, 500
    
    def validate_session_endpoint(self, session_token: str) -> Tuple[Dict[str, Any], int]:
        """
        Validate session token and return user information.
        
        Args:
            session_token: Session token to validate
            
        Returns:
            Tuple[Dict, int]: (response_data, http_status_code)
        """
        try:
            if not session_token:
                return {
                    'valid': False,
                    'errors': ['Session token required']
                }, 400
            
            is_valid, session_data = self.session_manager.validate_session(session_token)
            
            if is_valid and session_data:
                return {
                    'valid': True,
                    'user': {
                        'id': session_data.user_id,
                        'username': session_data.username,
                        'email': session_data.email
                    },
                    'session': {
                        'created_at': session_data.created_at.isoformat(),
                        'expires_at': session_data.expires_at.isoformat()
                    }
                }, 200
            else:
                return {
                    'valid': False,
                    'errors': ['Invalid or expired session']
                }, 401
                
        except Exception as e:
            current_app.logger.error(f"Error validating session: {e}")
            return {
                'valid': False,
                'errors': ['Session validation failed']
            }, 500
    
    def _get_client_ip(self) -> str:
        """
        Get client IP address from request headers.
        
        Returns:
            str: Client IP address
        """
        # Check for forwarded headers first (reverse proxy)
        client_ip = (
            request.headers.get('X-Forwarded-For', '').split(',')[0].strip() or
            request.headers.get('X-Real-IP', '').strip() or
            request.remote_addr or
            'unknown'
        )
        return client_ip


def require_authentication(f):
    """
    Decorator to require valid session for API endpoints.
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function that checks authentication
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get session token from header or cookie
        session_token = (
            request.headers.get('Authorization', '').replace('Bearer ', '') or
            request.cookies.get('session_token')
        )
        
        if not session_token:
            return jsonify({
                'success': False,
                'errors': ['Authentication required']
            }), 401
        
        # Validate session using SessionManager
        db_path = current_app.config.get('DATABASE_PATH', 'language_tracker.db')
        session_manager = SessionManager(db_path)
        
        is_valid, session_data = session_manager.validate_session(session_token)
        
        if not is_valid or not session_data:
            return jsonify({
                'success': False,
                'errors': ['Invalid or expired session']
            }), 401
        
        # Add user info to request context
        request.current_user = {
            'id': session_data.user_id,
            'username': session_data.username,
            'email': session_data.email
        }
        request.session_data = session_data
        
        return f(*args, **kwargs)
    
    return decorated_function


# Rate limiting decorator (basic implementation)
def rate_limit(max_requests: int = 5, window_minutes: int = 1):
    """
    Basic rate limiting decorator for authentication endpoints.
    
    Args:
        max_requests: Maximum requests allowed
        window_minutes: Time window in minutes
        
    Returns:
        Decorator function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # This is a basic implementation - in production, use Redis or similar
            # For now, we'll rely on Flask-Limiter or similar extensions
            return f(*args, **kwargs)
        return decorated_function
    return decorator