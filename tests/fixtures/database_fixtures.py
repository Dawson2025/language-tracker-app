# resource_id: e19a26e0-dcc8-4b78-86c6-f5f923fa104a
"""
Test Database Fixtures and Configuration
Language Tracker Hard Testing Rule Implementation

Provides comprehensive test data fixtures and database configuration
for all test environments (dev, test, staging, production).
"""

import sqlite3
import json
import os
import tempfile
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import secrets
import sys

# Add authentication module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../features/authentication'))

try:
    from password_security import PasswordSecurity
except ImportError:
    # Fallback if password security not available
    class PasswordSecurity:
        @staticmethod
        def hash_password(password: str) -> str:
            return f"hashed_{password}"
        
        @staticmethod
        def generate_session_token() -> str:
            return secrets.token_hex(32)


class TestDatabaseManager:
    """Manages test databases for different environments."""
    
    def __init__(self, environment: str = 'test'):
        self.environment = environment
        self.db_path = None
        self.connection = None
        
    def create_test_database(self) -> str:
        """Create a temporary test database with schema."""
        # Create temporary database file
        fd, self.db_path = tempfile.mkstemp(suffix=f'_{self.environment}.db')
        os.close(fd)
        
        # Initialize database with schema
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        
        # Create schema
        self._create_schema()
        
        return self.db_path
    
    def _create_schema(self):
        """Create the database schema for testing."""
        schema_sql = """
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        -- Sessions table
        CREATE TABLE IF NOT EXISTS sessions (
            id VARCHAR(64) PRIMARY KEY,
            user_id INTEGER NOT NULL,
            expires_at DATETIME NOT NULL,
            user_agent TEXT,
            ip_address VARCHAR(45),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        -- User profiles table
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            language_preference VARCHAR(10) DEFAULT 'en',
            timezone VARCHAR(50) DEFAULT 'UTC',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        -- Language learning progress table
        CREATE TABLE IF NOT EXISTS language_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            language_code VARCHAR(10) NOT NULL,
            skill_level VARCHAR(20) DEFAULT 'beginner',
            words_learned INTEGER DEFAULT 0,
            lessons_completed INTEGER DEFAULT 0,
            streak_days INTEGER DEFAULT 0,
            last_practice_date DATE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(user_id, language_code)
        );

        -- Test metrics table for performance benchmarking
        CREATE TABLE IF NOT EXISTS test_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_suite VARCHAR(50) NOT NULL,
            test_name VARCHAR(100) NOT NULL,
            execution_time_ms INTEGER NOT NULL,
            status VARCHAR(20) NOT NULL,
            environment VARCHAR(20) NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        self.connection.executescript(schema_sql)
        self.connection.commit()
    
    def cleanup(self):
        """Clean up test database."""
        if self.connection:
            self.connection.close()
        if self.db_path and os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        return self.connection


class TestDataFactory:
    """Factory for creating test data fixtures."""
    
    def __init__(self, db_manager: TestDatabaseManager):
        self.db_manager = db_manager
        self.connection = db_manager.get_connection()
    
    def create_test_users(self, count: int = 5) -> List[Dict[str, Any]]:
        """Create test users with realistic data."""
        users = []
        
        for i in range(count):
            user_data = {
                'username': f'testuser{i+1}',
                'email': f'testuser{i+1}@example.com',
                'password': f'TestPassword{i+1}!',
                'is_active': True if i < 4 else False  # Last user inactive
            }
            
            # Hash password
            password_hash = PasswordSecurity.hash_password(user_data['password'])
            
            # Insert user
            cursor = self.connection.execute(
                "INSERT INTO users (username, email, password_hash, is_active) VALUES (?, ?, ?, ?)",
                (user_data['username'], user_data['email'], password_hash, user_data['is_active'])
            )
            
            user_data['id'] = cursor.lastrowid
            user_data['password_hash'] = password_hash
            users.append(user_data)
        
        self.connection.commit()
        return users
    
    def create_test_sessions(self, user_ids: List[int]) -> List[Dict[str, Any]]:
        """Create test sessions for users."""
        sessions = []
        
        for user_id in user_ids:
            session_data = {
                'id': PasswordSecurity.generate_session_token(),
                'user_id': user_id,
                'expires_at': datetime.utcnow() + timedelta(hours=24),
                'user_agent': 'Test User Agent',
                'ip_address': '127.0.0.1'
            }
            
            self.connection.execute(
                "INSERT INTO sessions (id, user_id, expires_at, user_agent, ip_address) VALUES (?, ?, ?, ?, ?)",
                (session_data['id'], session_data['user_id'], session_data['expires_at'],
                 session_data['user_agent'], session_data['ip_address'])
            )
            
            sessions.append(session_data)
        
        self.connection.commit()
        return sessions
    
    def create_language_progress(self, user_ids: List[int]) -> List[Dict[str, Any]]:
        """Create language learning progress data."""
        languages = ['es', 'fr', 'de', 'it', 'pt', 'ja', 'zh', 'ko']
        skill_levels = ['beginner', 'elementary', 'intermediate', 'advanced']
        progress_data = []
        
        for user_id in user_ids:
            # Each user learns 1-3 languages
            user_languages = languages[:min(3, len(languages))]
            
            for lang in user_languages:
                progress = {
                    'user_id': user_id,
                    'language_code': lang,
                    'skill_level': skill_levels[min(user_id % len(skill_levels), len(skill_levels)-1)],
                    'words_learned': (user_id * 50) + (len(lang) * 10),
                    'lessons_completed': user_id * 5,
                    'streak_days': max(0, user_id * 2 - 1),
                    'last_practice_date': datetime.utcnow().date() - timedelta(days=user_id-1)
                }
                
                self.connection.execute(
                    """INSERT INTO language_progress 
                       (user_id, language_code, skill_level, words_learned, lessons_completed, 
                        streak_days, last_practice_date) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (progress['user_id'], progress['language_code'], progress['skill_level'],
                     progress['words_learned'], progress['lessons_completed'],
                     progress['streak_days'], progress['last_practice_date'])
                )
                
                progress_data.append(progress)
        
        self.connection.commit()
        return progress_data
    
    def create_performance_benchmarks(self) -> Dict[str, Any]:
        """Create performance benchmark data for test execution."""
        benchmarks = {
            'unit_tests': {
                'target_time_ms': 10000,  # 10 seconds
                'max_time_ms': 30000,     # 30 seconds
                'parallel_workers': 4
            },
            'integration_tests': {
                'target_time_ms': 15000,  # 15 seconds
                'max_time_ms': 60000,     # 1 minute
                'parallel_workers': 2
            },
            'e2e_tests': {
                'target_time_ms': 30000,  # 30 seconds
                'max_time_ms': 180000,    # 3 minutes
                'parallel_workers': 2
            },
            'user_story_fast': {
                'target_time_ms': 30000,  # 30 seconds
                'max_time_ms': 60000,     # 1 minute
                'parallel_workers': 4
            },
            'user_story_realistic': {
                'target_time_ms': 300000, # 5 minutes
                'max_time_ms': 600000,    # 10 minutes
                'parallel_workers': 1
            }
        }
        
        return benchmarks
    
    def clear_all_data(self):
        """Clear all test data from database."""
        tables = ['language_progress', 'user_profiles', 'sessions', 'users', 'test_metrics']
        
        for table in tables:
            self.connection.execute(f"DELETE FROM {table}")
        
        self.connection.commit()


class FirebaseTestConfig:
    """Configuration for Firebase testing environments."""
    
    ENVIRONMENTS = {
        'dev': {
            'project_id': 'lang-trak-dev',
            'service_account_file': 'firebase-service-account-dev.json',
            'database_url': 'https://lang-trak-dev-default-rtdb.firebaseio.com',
            'storage_bucket': 'lang-trak-dev.appspot.com'
        },
        'test': {
            'project_id': 'lang-trak-test',
            'service_account_file': 'firebase-service-account-test.json',
            'database_url': 'https://lang-trak-test-default-rtdb.firebaseio.com',
            'storage_bucket': 'lang-trak-test.appspot.com'
        },
        'staging': {
            'project_id': 'lang-trak-staging',
            'service_account_file': 'firebase-service-account-staging.json',
            'database_url': 'https://lang-trak-staging-default-rtdb.firebaseio.com',
            'storage_bucket': 'lang-trak-staging.appspot.com'
        },
        'prod': {
            'project_id': 'lang-trak-prod',
            'service_account_file': 'firebase-service-account-prod.json',
            'database_url': 'https://lang-trak-prod-default-rtdb.firebaseio.com',
            'storage_bucket': 'lang-trak-prod.appspot.com'
        }
    }
    
    @classmethod
    def get_config(cls, environment: str) -> Dict[str, str]:
        """Get Firebase configuration for environment."""
        if environment not in cls.ENVIRONMENTS:
            raise ValueError(f"Unknown environment: {environment}")
        
        return cls.ENVIRONMENTS[environment].copy()
    
    @classmethod
    def validate_credentials(cls, environment: str) -> bool:
        """Validate that Firebase credentials exist for environment."""
        config = cls.get_config(environment)
        service_account_path = config['service_account_file']
        
        return os.path.exists(service_account_path)


class TestMetricsCollector:
    """Collects and reports test execution metrics."""
    
    def __init__(self, db_manager: TestDatabaseManager):
        self.db_manager = db_manager
        self.connection = db_manager.get_connection()
    
    def record_test_execution(self, test_suite: str, test_name: str, 
                            execution_time_ms: int, status: str, environment: str):
        """Record test execution metrics."""
        self.connection.execute(
            """INSERT INTO test_metrics 
               (test_suite, test_name, execution_time_ms, status, environment) 
               VALUES (?, ?, ?, ?, ?)""",
            (test_suite, test_name, execution_time_ms, status, environment)
        )
        self.connection.commit()
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for all tests."""
        cursor = self.connection.execute(
            """SELECT test_suite, 
                      COUNT(*) as total_tests,
                      AVG(execution_time_ms) as avg_time_ms,
                      MAX(execution_time_ms) as max_time_ms,
                      MIN(execution_time_ms) as min_time_ms,
                      SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) as passed_tests,
                      SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_tests
               FROM test_metrics 
               GROUP BY test_suite 
               ORDER BY test_suite"""
        )
        
        results = {}
        for row in cursor.fetchall():
            results[row['test_suite']] = {
                'total_tests': row['total_tests'],
                'avg_time_ms': round(row['avg_time_ms'], 2),
                'max_time_ms': row['max_time_ms'],
                'min_time_ms': row['min_time_ms'],
                'passed_tests': row['passed_tests'],
                'failed_tests': row['failed_tests'],
                'pass_rate': round((row['passed_tests'] / row['total_tests']) * 100, 2)
            }
        
        return results


# Test data export utilities
def export_test_fixtures(db_manager: TestDatabaseManager, output_dir: str):
    """Export test fixtures to JSON files."""
    os.makedirs(output_dir, exist_ok=True)
    
    factory = TestDataFactory(db_manager)
    connection = db_manager.get_connection()
    
    # Export users
    users = connection.execute("SELECT * FROM users").fetchall()
    with open(os.path.join(output_dir, 'users.json'), 'w') as f:
        json.dump([dict(user) for user in users], f, indent=2, default=str)
    
    # Export sessions
    sessions = connection.execute("SELECT * FROM sessions").fetchall()
    with open(os.path.join(output_dir, 'sessions.json'), 'w') as f:
        json.dump([dict(session) for session in sessions], f, indent=2, default=str)
    
    # Export language progress
    progress = connection.execute("SELECT * FROM language_progress").fetchall()
    with open(os.path.join(output_dir, 'language_progress.json'), 'w') as f:
        json.dump([dict(p) for p in progress], f, indent=2, default=str)


if __name__ == "__main__":
    # Example usage and testing
    print("🧪 Testing Database Fixtures...")
    
    # Create test database
    db_manager = TestDatabaseManager('test')
    db_path = db_manager.create_test_database()
    print(f"✅ Test database created: {db_path}")
    
    # Create test data
    factory = TestDataFactory(db_manager)
    users = factory.create_test_users(3)
    print(f"✅ Created {len(users)} test users")
    
    sessions = factory.create_test_sessions([user['id'] for user in users])
    print(f"✅ Created {len(sessions)} test sessions")
    
    progress = factory.create_language_progress([user['id'] for user in users])
    print(f"✅ Created {len(progress)} language progress records")
    
    # Test metrics
    metrics = TestMetricsCollector(db_manager)
    metrics.record_test_execution('unit_tests', 'test_password_hash', 150, 'passed', 'test')
    print("✅ Test metrics recorded")
    
    # Export fixtures
    export_test_fixtures(db_manager, 'test_fixtures_export')
    print("✅ Test fixtures exported")
    
    # Cleanup
    db_manager.cleanup()
    print("✅ Test database cleaned up")
    
    print("\n🎉 Database fixtures system ready for Hard Testing Rule enforcement!")