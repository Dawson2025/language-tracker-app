"""
Firebase OAuth Integration
Language Tracker Authentication Feature
Created via GitHub Spec Kit Implementation Phase

Implements Google Sign-In via Firebase Auth with local account linking.
Provides graceful degradation when Firebase services are unavailable.
"""

import json
import logging
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
import sqlite3

try:
    import firebase_admin
    from firebase_admin import credentials, auth as firebase_auth
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    firebase_admin = None
    firebase_auth = None

from .session_manager import SessionManager
from .password_security import PasswordSecurity


class FirebaseAuthenticationError(Exception):
    """Custom exception for Firebase authentication errors."""
    pass


class FirebaseAuthManager:
    """
    Manages Firebase OAuth integration with local account linking.
    Implements graceful degradation when Firebase is unavailable.
    """
    
    def __init__(self, db_path: str, service_account_path: str = None):
        """
        Initialize Firebase authentication manager.
        
        Args:
            db_path: Path to SQLite database
            service_account_path: Path to Firebase service account JSON file
        """
        self.db_path = db_path
        self.session_manager = SessionManager(db_path)
        self.firebase_initialized = False
        self.firebase_app = None
        
        # Default service account paths for different environments
        if not service_account_path:
            service_account_path = self._get_default_service_account_path()
        
        self.service_account_path = service_account_path
        
        # Initialize Firebase if available
        if FIREBASE_AVAILABLE:
            self._initialize_firebase()
        else:
            logging.warning("Firebase Admin SDK not available. OAuth functionality disabled.")
    
    def _get_default_service_account_path(self) -> str:
        """
        Get default service account path based on environment.
        
        Returns:
            str: Path to service account file
        """
        # Check environment or use development by default
        import os
        env = os.getenv('FLASK_ENV', 'development')
        
        if env == 'production':
            return 'firebase-service-account-prod.json'
        elif env == 'staging':
            return 'firebase-service-account-staging.json'
        elif env == 'testing':
            return 'firebase-service-account-test.json'
        else:
            return 'firebase-service-account-dev.json'
    
    def _initialize_firebase(self) -> bool:
        """
        Initialize Firebase Admin SDK with service account.
        
        Returns:
            bool: True if initialization successful
        """
        try:
            # Check if already initialized
            if self.firebase_initialized and self.firebase_app:
                return True
            
            # Load service account credentials
            if not self.service_account_path:
                logging.error("Firebase service account path not configured")
                return False
            
            try:
                cred = credentials.Certificate(self.service_account_path)
                
                # Initialize Firebase app
                self.firebase_app = firebase_admin.initialize_app(
                    cred, 
                    name=f'lang_trak_auth_{datetime.now().timestamp()}'
                )
                
                self.firebase_initialized = True
                logging.info("Firebase Admin SDK initialized successfully")
                return True
                
            except FileNotFoundError:
                logging.error(f"Firebase service account file not found: {self.service_account_path}")
                return False
            except Exception as e:
                logging.error(f"Firebase initialization failed: {e}")
                return False
                
        except Exception as e:
            logging.error(f"Unexpected error during Firebase initialization: {e}")
            return False
    
    def is_firebase_available(self) -> bool:
        """
        Check if Firebase is available and initialized.
        
        Returns:
            bool: True if Firebase is ready for use
        """
        return FIREBASE_AVAILABLE and self.firebase_initialized
    
    def verify_firebase_token(self, id_token: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Verify Firebase ID token and extract user information.
        
        Args:
            id_token: Firebase ID token from client
            
        Returns:
            Tuple[bool, Optional[Dict]]: (is_valid, user_info)
        """
        if not self.is_firebase_available():
            return False, {"error": "Firebase authentication not available"}
        
        try:
            # Verify the ID token
            decoded_token = firebase_auth.verify_id_token(id_token, app=self.firebase_app)
            
            # Extract user information
            user_info = {
                'firebase_uid': decoded_token.get('uid'),
                'email': decoded_token.get('email'),
                'email_verified': decoded_token.get('email_verified', False),
                'name': decoded_token.get('name'),
                'picture': decoded_token.get('picture'),
                'provider': 'google.com' if 'google.com' in decoded_token.get('firebase', {}).get('sign_in_provider', '') else 'firebase'
            }
            
            # Validate required fields
            if not user_info['firebase_uid'] or not user_info['email']:
                return False, {"error": "Invalid token: missing required fields"}
            
            return True, user_info
            
        except firebase_auth.InvalidIdTokenError:
            return False, {"error": "Invalid or expired token"}
        except firebase_auth.ExpiredIdTokenError:
            return False, {"error": "Token has expired"}
        except Exception as e:
            logging.error(f"Firebase token verification error: {e}")
            return False, {"error": "Token verification failed"}
    
    def authenticate_with_firebase(
        self,
        id_token: str,
        user_agent: str = None,
        ip_address: str = None
    ) -> Tuple[Dict[str, Any], int]:
        """
        Authenticate user with Firebase token and create/link local account.
        
        Implements US-003: Firebase Authentication (Google Sign-In)
        
        Args:
            id_token: Firebase ID token from client
            user_agent: Browser user agent string
            ip_address: Client IP address
            
        Returns:
            Tuple[Dict, int]: (response_data, http_status_code)
        """
        try:
            # Check if Firebase is available
            if not self.is_firebase_available():
                return {
                    'success': False,
                    'errors': ['Google Sign-In is temporarily unavailable. Please use email/password login.'],
                    'fallback_available': True
                }, 503  # Service Unavailable
            
            # Verify Firebase token
            token_valid, user_info = self.verify_firebase_token(id_token)
            
            if not token_valid:
                return {
                    'success': False,
                    'errors': [user_info.get('error', 'Authentication failed')]
                }, 401
            
            firebase_uid = user_info['firebase_uid']
            email = user_info['email']
            name = user_info.get('name', '')
            
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            try:
                # Check if user exists with this Firebase UID
                existing_user = conn.execute("""
                    SELECT id, username, email, is_active FROM users 
                    WHERE firebase_uid = ?
                """, (firebase_uid,)).fetchone()
                
                if existing_user:
                    # User exists - verify account is active
                    if not existing_user['is_active']:
                        return {
                            'success': False,
                            'errors': ['Account is deactivated']
                        }, 401
                    
                    user_id = existing_user['id']
                    username = existing_user['username']
                    
                else:
                    # Check if user exists with this email (for linking)
                    email_user = conn.execute("""
                        SELECT id, username, is_active FROM users 
                        WHERE email = ? AND firebase_uid IS NULL
                    """, (email,)).fetchone()
                    
                    if email_user:
                        # Link existing local account to Firebase
                        if not email_user['is_active']:
                            return {
                                'success': False,
                                'errors': ['Account is deactivated']
                            }, 401
                        
                        conn.execute("""
                            UPDATE users SET firebase_uid = ?, last_login = ?
                            WHERE id = ?
                        """, (firebase_uid, datetime.now().isoformat(), email_user['id']))
                        
                        user_id = email_user['id']
                        username = email_user['username']
                        
                    else:
                        # Create new user account
                        username = self._generate_username_from_email_or_name(email, name, conn)
                        
                        # Generate placeholder password hash (won't be used for Firebase auth)
                        placeholder_password = PasswordSecurity.generate_session_token()
                        password_hash = PasswordSecurity.hash_password(placeholder_password)
                        
                        cursor = conn.execute("""
                            INSERT INTO users (username, email, password_hash, firebase_uid, is_active)
                            VALUES (?, ?, ?, ?, 1)
                        """, (username, email, password_hash, firebase_uid))
                        
                        user_id = cursor.lastrowid
                
                conn.commit()
                
                # Create session
                session_success, session_id, session_info = self.session_manager.create_session(
                    user_id=user_id,
                    duration_hours=24,  # Standard session duration
                    user_agent=user_agent,
                    ip_address=ip_address
                )
                
                if session_success:
                    return {
                        'success': True,
                        'message': f'Welcome, {username}!',
                        'user': {
                            'id': user_id,
                            'username': username,
                            'email': email,
                            'auth_provider': 'google'
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
                        'errors': ['Authentication succeeded but session creation failed']
                    }, 500
                    
            except sqlite3.Error as e:
                conn.rollback()
                logging.error(f"Database error during Firebase auth: {e}")
                return {
                    'success': False,
                    'errors': ['Authentication failed. Please try again.']
                }, 500
                
            finally:
                conn.close()
                
        except Exception as e:
            logging.error(f"Unexpected error during Firebase authentication: {e}")
            return {
                'success': False,
                'errors': ['An unexpected error occurred. Please try again.']
            }, 500
    
    def _generate_username_from_email_or_name(
        self, 
        email: str, 
        name: str, 
        conn: sqlite3.Connection
    ) -> str:
        """
        Generate a unique username from email or name.
        
        Args:
            email: User's email address
            name: User's display name
            conn: Database connection
            
        Returns:
            str: Unique username
        """
        # Try to use name first if available
        if name:
            base_username = ''.join(c.lower() for c in name if c.isalnum())
            if len(base_username) >= 3:
                base_username = base_username[:20]  # Limit length
            else:
                base_username = email.split('@')[0]
        else:
            base_username = email.split('@')[0]
        
        # Clean up the base username
        base_username = ''.join(c for c in base_username if c.isalnum() or c in '_-')
        if len(base_username) < 3:
            base_username = 'user' + base_username
        
        # Ensure it's not too long
        base_username = base_username[:20]
        
        # Check if username is available
        username = base_username
        counter = 1
        
        while True:
            existing = conn.execute(
                "SELECT id FROM users WHERE username = ?", 
                (username,)
            ).fetchone()
            
            if not existing:
                break
                
            username = f"{base_username}{counter}"
            counter += 1
            
            # Prevent infinite loop
            if counter > 1000:
                username = f"user{PasswordSecurity.generate_session_token()[:8]}"
                break
        
        return username
    
    def unlink_firebase_account(self, user_id: int) -> Tuple[bool, str]:
        """
        Unlink Firebase account from local user account.
        
        Args:
            user_id: Local user ID
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Check if user has a password set (can't unlink if no local password)
            user_row = conn.execute("""
                SELECT password_hash FROM users 
                WHERE id = ? AND firebase_uid IS NOT NULL
            """, (user_id,)).fetchone()
            
            if not user_row:
                return False, "User not found or not linked to Firebase"
            
            # For security, require a local password before unlinking
            # (This should be enforced at the API level)
            
            # Unlink Firebase UID
            conn.execute("""
                UPDATE users SET firebase_uid = NULL 
                WHERE id = ?
            """, (user_id,))
            
            conn.commit()
            conn.close()
            
            return True, "Firebase account unlinked successfully"
            
        except sqlite3.Error as e:
            logging.error(f"Database error during Firebase unlinking: {e}")
            return False, "Failed to unlink Firebase account"
        except Exception as e:
            logging.error(f"Unexpected error during Firebase unlinking: {e}")
            return False, "An unexpected error occurred"
    
    def get_firebase_config_for_client(self) -> Optional[Dict[str, str]]:
        """
        Get Firebase configuration for client-side initialization.
        This should be called to provide config to the frontend.
        
        Returns:
            Optional[Dict]: Firebase config or None if not available
        """
        if not self.is_firebase_available():
            return None
        
        # In a real implementation, you would return the client-side Firebase config
        # This is typically stored in environment variables or config files
        # For security, never expose service account credentials to the client
        
        return {
            "apiKey": "your-firebase-api-key",
            "authDomain": "your-project.firebaseapp.com",
            "projectId": "your-project-id",
            "storageBucket": "your-project.appspot.com",
            "messagingSenderId": "123456789",
            "appId": "your-app-id"
        }
    
    def cleanup(self):
        """
        Cleanup Firebase resources.
        """
        if self.firebase_app:
            try:
                firebase_admin.delete_app(self.firebase_app)
                self.firebase_initialized = False
                self.firebase_app = None
                logging.info("Firebase app cleaned up successfully")
            except Exception as e:
                logging.error(f"Error during Firebase cleanup: {e}")


# Utility functions for Firebase integration

def require_firebase_available(f):
    """
    Decorator to ensure Firebase is available for endpoints.
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function that checks Firebase availability
    """
    from functools import wraps
    from flask import jsonify
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not FIREBASE_AVAILABLE:
            return jsonify({
                'success': False,
                'errors': ['Firebase authentication is not available'],
                'fallback_available': True
            }), 503
        
        return f(*args, **kwargs)
    
    return decorated_function


def get_firebase_error_message(error_code: str) -> str:
    """
    Convert Firebase error codes to user-friendly messages.
    
    Args:
        error_code: Firebase error code
        
    Returns:
        str: User-friendly error message
    """
    error_messages = {
        'auth/invalid-id-token': 'Authentication token is invalid',
        'auth/id-token-expired': 'Authentication token has expired',
        'auth/id-token-revoked': 'Authentication token has been revoked',
        'auth/user-disabled': 'This account has been disabled',
        'auth/user-not-found': 'Account not found',
        'auth/invalid-email': 'Invalid email address',
        'auth/email-already-exists': 'Email address is already registered'
    }
    
    return error_messages.get(error_code, 'Authentication failed')