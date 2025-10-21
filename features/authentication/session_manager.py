"""
Session Management System
Language Tracker Authentication Feature
Created via GitHub Spec Kit Implementation Phase

Handles user session creation, validation, expiration, and cleanup.
Implements security best practices to prevent session fixation and hijacking.
"""

import sqlite3
import datetime
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass
from contextlib import contextmanager

from .password_security import PasswordSecurity


@dataclass
class UserSession:
    """Data class representing a user session."""
    session_id: str
    user_id: int
    username: str
    email: str
    created_at: datetime.datetime
    expires_at: datetime.datetime
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None


class SessionManager:
    """
    Manages user sessions with security features and automatic cleanup.
    """
    
    # Session configuration
    DEFAULT_SESSION_DURATION_HOURS = 24
    MAX_SESSION_DURATION_HOURS = 7 * 24  # 7 days
    CLEANUP_EXPIRED_ON_OPERATION = True
    
    def __init__(self, db_path: str):
        """
        Initialize session manager with database connection.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._ensure_tables_exist()
    
    @contextmanager
    def get_db_connection(self):
        """
        Context manager for database connections with proper cleanup.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        try:
            yield conn
        finally:
            conn.close()
    
    def _ensure_tables_exist(self):
        """
        Ensure required tables exist by running schema if needed.
        """
        try:
            with self.get_db_connection() as conn:
                # Check if users table exists
                cursor = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
                )
                if not cursor.fetchone():
                    # Load schema from file
                    schema_path = "features/authentication/schema.sql"
                    try:
                        with open(schema_path, 'r') as f:
                            schema_sql = f.read()
                        conn.executescript(schema_sql)
                        conn.commit()
                    except FileNotFoundError:
                        raise RuntimeError(f"Schema file not found: {schema_path}")
        except sqlite3.Error as e:
            raise RuntimeError(f"Database initialization failed: {e}")
    
    def create_session(
        self, 
        user_id: int, 
        duration_hours: int = None,
        user_agent: str = None,
        ip_address: str = None
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Create a new session for a user.
        
        Args:
            user_id: ID of the user
            duration_hours: Session duration in hours (default: 24)
            user_agent: Browser user agent string
            ip_address: Client IP address
            
        Returns:
            Tuple[bool, str, Dict]: (success, session_id, session_info)
        """
        if duration_hours is None:
            duration_hours = self.DEFAULT_SESSION_DURATION_HOURS
        
        # Enforce maximum session duration
        duration_hours = min(duration_hours, self.MAX_SESSION_DURATION_HOURS)
        
        try:
            with self.get_db_connection() as conn:
                # Verify user exists and is active
                user_row = conn.execute(
                    "SELECT id, username, email FROM users WHERE id = ? AND is_active = 1",
                    (user_id,)
                ).fetchone()
                
                if not user_row:
                    return False, "", {"error": "User not found or inactive"}
                
                # Generate secure session token
                session_id = PasswordSecurity.generate_session_token()
                
                # Calculate expiration time
                created_at = datetime.datetime.now()
                expires_at = created_at + datetime.timedelta(hours=duration_hours)
                
                # Insert session record
                conn.execute("""
                    INSERT INTO user_sessions 
                    (session_id, user_id, created_at, expires_at, user_agent, ip_address)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    session_id,
                    user_id,
                    created_at.isoformat(),
                    expires_at.isoformat(),
                    user_agent,
                    ip_address
                ))
                
                # Update user's last login
                conn.execute(
                    "UPDATE users SET last_login = ? WHERE id = ?",
                    (created_at.isoformat(), user_id)
                )
                
                conn.commit()
                
                # Cleanup expired sessions
                if self.CLEANUP_EXPIRED_ON_OPERATION:
                    self._cleanup_expired_sessions(conn)
                
                session_info = {
                    "session_id": session_id,
                    "user_id": user_id,
                    "username": user_row["username"],
                    "email": user_row["email"],
                    "created_at": created_at.isoformat(),
                    "expires_at": expires_at.isoformat(),
                    "duration_hours": duration_hours
                }
                
                return True, session_id, session_info
                
        except sqlite3.Error as e:
            return False, "", {"error": f"Database error: {str(e)}"}
    
    def validate_session(self, session_id: str) -> Tuple[bool, Optional[UserSession]]:
        """
        Validate a session and return session information.
        
        Args:
            session_id: Session ID to validate
            
        Returns:
            Tuple[bool, Optional[UserSession]]: (is_valid, session_data)
        """
        if not session_id or len(session_id) != 64:  # Session tokens are 64 chars
            return False, None
        
        try:
            with self.get_db_connection() as conn:
                # Query active session with user info
                row = conn.execute("""
                    SELECT 
                        s.session_id, s.user_id, s.created_at, s.expires_at,
                        s.user_agent, s.ip_address,
                        u.username, u.email
                    FROM user_sessions s
                    JOIN users u ON s.user_id = u.id
                    WHERE s.session_id = ? 
                      AND s.is_active = 1 
                      AND s.expires_at > datetime('now')
                      AND u.is_active = 1
                """, (session_id,)).fetchone()
                
                if not row:
                    return False, None
                
                # Convert to UserSession object
                session = UserSession(
                    session_id=row["session_id"],
                    user_id=row["user_id"],
                    username=row["username"],
                    email=row["email"],
                    created_at=datetime.datetime.fromisoformat(row["created_at"]),
                    expires_at=datetime.datetime.fromisoformat(row["expires_at"]),
                    user_agent=row["user_agent"],
                    ip_address=row["ip_address"]
                )
                
                return True, session
                
        except (sqlite3.Error, ValueError) as e:
            return False, None
    
    def extend_session(self, session_id: str, hours: int = None) -> bool:
        """
        Extend a session's expiration time.
        
        Args:
            session_id: Session ID to extend
            hours: Hours to extend (default: reset to full duration)
            
        Returns:
            bool: True if session was extended
        """
        if hours is None:
            hours = self.DEFAULT_SESSION_DURATION_HOURS
        
        hours = min(hours, self.MAX_SESSION_DURATION_HOURS)
        
        try:
            with self.get_db_connection() as conn:
                new_expires_at = datetime.datetime.now() + datetime.timedelta(hours=hours)
                
                cursor = conn.execute("""
                    UPDATE user_sessions 
                    SET expires_at = ?
                    WHERE session_id = ? 
                      AND is_active = 1 
                      AND expires_at > datetime('now')
                """, (new_expires_at.isoformat(), session_id))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error:
            return False
    
    def invalidate_session(self, session_id: str) -> bool:
        """
        Invalidate a specific session (logout).
        
        Args:
            session_id: Session ID to invalidate
            
        Returns:
            bool: True if session was invalidated
        """
        try:
            with self.get_db_connection() as conn:
                cursor = conn.execute(
                    "UPDATE user_sessions SET is_active = 0 WHERE session_id = ?",
                    (session_id,)
                )
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error:
            return False
    
    def invalidate_all_user_sessions(self, user_id: int) -> int:
        """
        Invalidate all sessions for a user (logout from all devices).
        
        Args:
            user_id: User ID whose sessions to invalidate
            
        Returns:
            int: Number of sessions invalidated
        """
        try:
            with self.get_db_connection() as conn:
                cursor = conn.execute(
                    "UPDATE user_sessions SET is_active = 0 WHERE user_id = ?",
                    (user_id,)
                )
                conn.commit()
                return cursor.rowcount
                
        except sqlite3.Error:
            return 0
    
    def get_active_sessions(self, user_id: int) -> list[Dict[str, Any]]:
        """
        Get all active sessions for a user.
        
        Args:
            user_id: User ID to query
            
        Returns:
            list: List of active session information
        """
        try:
            with self.get_db_connection() as conn:
                rows = conn.execute("""
                    SELECT 
                        session_id, created_at, expires_at, user_agent, ip_address
                    FROM user_sessions 
                    WHERE user_id = ? 
                      AND is_active = 1 
                      AND expires_at > datetime('now')
                    ORDER BY created_at DESC
                """, (user_id,)).fetchall()
                
                return [dict(row) for row in rows]
                
        except sqlite3.Error:
            return []
    
    def cleanup_expired_sessions(self) -> int:
        """
        Manually trigger cleanup of expired sessions.
        
        Returns:
            int: Number of sessions cleaned up
        """
        try:
            with self.get_db_connection() as conn:
                return self._cleanup_expired_sessions(conn)
        except sqlite3.Error:
            return 0
    
    def _cleanup_expired_sessions(self, conn: sqlite3.Connection) -> int:
        """
        Internal method to cleanup expired sessions.
        
        Args:
            conn: Database connection
            
        Returns:
            int: Number of sessions cleaned up
        """
        cursor = conn.execute("""
            DELETE FROM user_sessions 
            WHERE expires_at < datetime('now') OR is_active = 0
        """)
        conn.commit()
        return cursor.rowcount
    
    def get_session_stats(self) -> Dict[str, int]:
        """
        Get session statistics for monitoring.
        
        Returns:
            Dict: Session statistics
        """
        try:
            with self.get_db_connection() as conn:
                active_count = conn.execute("""
                    SELECT COUNT(*) FROM user_sessions 
                    WHERE is_active = 1 AND expires_at > datetime('now')
                """).fetchone()[0]
                
                expired_count = conn.execute("""
                    SELECT COUNT(*) FROM user_sessions 
                    WHERE expires_at <= datetime('now')
                """).fetchone()[0]
                
                inactive_count = conn.execute("""
                    SELECT COUNT(*) FROM user_sessions 
                    WHERE is_active = 0
                """).fetchone()[0]
                
                return {
                    "active_sessions": active_count,
                    "expired_sessions": expired_count,
                    "inactive_sessions": inactive_count,
                    "total_sessions": active_count + expired_count + inactive_count
                }
                
        except sqlite3.Error:
            return {
                "active_sessions": 0,
                "expired_sessions": 0,
                "inactive_sessions": 0,
                "total_sessions": 0
            }