# resource_id: 5feee40a-e66b-4da1-ab32-4c2e90d8f09e
-- Authentication Feature Database Schema
-- Language Tracker Project
-- Created via GitHub Spec Kit Implementation Phase

-- Users table for local authentication
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    firebase_uid TEXT UNIQUE,  -- Firebase OAuth integration
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    
    -- Constraints
    CONSTRAINT username_length CHECK (length(username) >= 3),
    CONSTRAINT email_format CHECK (email LIKE '%_@_%._%'),
    CONSTRAINT password_hash_length CHECK (length(password_hash) >= 60)  -- bcrypt hash minimum
);

-- Sessions table for authentication state management
CREATE TABLE IF NOT EXISTS user_sessions (
    session_id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    user_agent TEXT,  -- For session tracking
    ip_address TEXT,  -- For security monitoring
    
    -- Foreign key constraint
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Ensure expires_at is in the future
    CONSTRAINT valid_expiration CHECK (expires_at > created_at)
);

-- Indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_firebase_uid ON users(firebase_uid);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON user_sessions(expires_at);
CREATE INDEX IF NOT EXISTS idx_sessions_active ON user_sessions(is_active, expires_at);

-- View for active sessions (for easy querying)
CREATE VIEW IF NOT EXISTS active_sessions AS
SELECT 
    s.session_id,
    s.user_id,
    u.username,
    u.email,
    s.created_at,
    s.expires_at,
    s.user_agent,
    s.ip_address
FROM user_sessions s
JOIN users u ON s.user_id = u.id
WHERE s.is_active = 1 
  AND s.expires_at > datetime('now');

-- Cleanup trigger to remove expired sessions
CREATE TRIGGER IF NOT EXISTS cleanup_expired_sessions
    AFTER INSERT ON user_sessions
BEGIN
    DELETE FROM user_sessions 
    WHERE expires_at < datetime('now') 
      OR is_active = 0;
END;