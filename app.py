#!/usr/bin/env python3
"""
Language Tracker Web Application
Main Flask Application Server
Created via GitHub Spec Kit Implementation Phase

Connects React frontend with authentication backend APIs.
Implements US-001 through US-003 with full authentication flow.
"""

import os
import sys
import logging
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from werkzeug.exceptions import NotFound

# Add features directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'features'))

from authentication.api_operations import AuthenticationAPI
from authentication.firebase_auth import FirebaseAuthManager
from authentication.session_manager import SessionManager
from authentication.validation import AuthenticationValidator

# Initialize Flask app
def create_app(config=None):
    app = Flask(__name__, static_folder='build/static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DATABASE_PATH'] = os.environ.get('DATABASE_PATH', 'langtrak.db')
    app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'development')
    
    # Override with provided config
    if config:
        app.config.update(config)
    
    # CORS configuration - more restrictive in production
    if app.config['FLASK_ENV'] == 'production':
        CORS(app, origins=['https://yourdomain.com'])
    else:
        CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])
    
    # Logging configuration
    if app.config['FLASK_ENV'] != 'testing':
        logging.basicConfig(
            level=logging.INFO if app.config['FLASK_ENV'] == 'production' else logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    # Initialize authentication components
    auth_api = AuthenticationAPI(app.config['DATABASE_PATH'])
    firebase_auth = FirebaseAuthManager(app.config['DATABASE_PATH'])
    session_manager = SessionManager(app.config['DATABASE_PATH'])
    validator = AuthenticationValidator()
    
    # Helper function to get client IP
    def get_client_ip():
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        elif request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        else:
            return request.remote_addr
    
    # Helper function to validate session token
    def validate_token():
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None, {'error': 'Missing or invalid authorization header'}, 401
        
        token = auth_header.split(' ')[1]
        is_valid, session = session_manager.validate_session(token)
        
        if not is_valid:
            return None, {'error': 'Invalid or expired session'}, 401
            
        return session, None, None
    
    # Authentication API Routes
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        """User registration endpoint - implements US-001"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'errors': ['No data provided']}), 400
            
            # Get client info
            user_agent = request.headers.get('User-Agent', '')
            client_ip = get_client_ip()
            
            # Call authentication API
            response_data, status_code = auth_api.register_user({
                **data,
                'user_agent': user_agent,
                'ip_address': client_ip
            })
            
            return jsonify(response_data), status_code
            
        except Exception as e:
            app.logger.error(f"Registration endpoint error: {e}")
            return jsonify({
                'success': False, 
                'errors': ['Registration failed. Please try again.']
            }), 500
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """User login endpoint - implements US-002"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'errors': ['No data provided']}), 400
            
            # Get client info
            user_agent = request.headers.get('User-Agent', '')
            client_ip = get_client_ip()
            
            # Call authentication API
            response_data, status_code = auth_api.login_user({
                **data,
                'user_agent': user_agent,
                'ip_address': client_ip
            })
            
            return jsonify(response_data), status_code
            
        except Exception as e:
            app.logger.error(f"Login endpoint error: {e}")
            return jsonify({
                'success': False, 
                'errors': ['Login failed. Please try again.']
            }), 500
    
    @app.route('/api/auth/firebase', methods=['POST'])
    def firebase_login():
        """Firebase/Google OAuth login - implements US-003"""
        try:
            data = request.get_json()
            if not data or 'id_token' not in data:
                return jsonify({
                    'success': False, 
                    'errors': ['ID token is required']
                }), 400
            
            # Get client info
            user_agent = request.headers.get('User-Agent', '')
            client_ip = get_client_ip()
            
            # Call Firebase authentication
            response_data, status_code = firebase_auth.authenticate_with_firebase(
                data['id_token'],
                user_agent,
                client_ip
            )
            
            return jsonify(response_data), status_code
            
        except Exception as e:
            app.logger.error(f"Firebase login endpoint error: {e}")
            return jsonify({
                'success': False,
                'errors': ['Google Sign-In failed. Please try again.']
            }), 500
    
    @app.route('/api/auth/validate', methods=['GET'])
    def validate_session():
        """Session validation endpoint"""
        session, error_response, status_code = validate_token()
        if error_response:
            return jsonify(error_response), status_code
        
        return jsonify({
            'valid': True,
            'user': {
                'id': session.user_id,
                'username': session.username,
                'email': session.email
            },
            'session': {
                'expires_at': session.expires_at.isoformat()
            }
        })
    
    @app.route('/api/auth/logout', methods=['POST'])
    def logout():
        """Logout endpoint"""
        session, error_response, status_code = validate_token()
        if error_response:
            # Allow logout even with invalid token
            return jsonify({'success': True, 'message': 'Logged out locally'})
        
        try:
            # Invalidate session
            success = session_manager.invalidate_session(session.session_id)
            
            return jsonify({
                'success': success,
                'message': 'Logged out successfully' if success else 'Logout may have failed'
            })
            
        except Exception as e:
            app.logger.error(f"Logout endpoint error: {e}")
            return jsonify({'success': True, 'message': 'Logged out locally'})
    
    @app.route('/api/auth/firebase-config', methods=['GET'])
    def get_firebase_config():
        """Get Firebase configuration for client"""
        try:
            config = firebase_auth.get_firebase_config_for_client()
            if config:
                return jsonify(config)
            else:
                return jsonify({'error': 'Firebase configuration not available'}), 503
        except Exception as e:
            app.logger.error(f"Firebase config endpoint error: {e}")
            return jsonify({'error': 'Firebase configuration not available'}), 503
    
    # User management endpoints
    @app.route('/api/user/profile', methods=['GET'])
    def get_user_profile():
        """Get user profile information"""
        session, error_response, status_code = validate_token()
        if error_response:
            return jsonify(error_response), status_code
        
        return jsonify({
            'user': {
                'id': session.user_id,
                'username': session.username,
                'email': session.email,
                'created_at': session.created_at.isoformat() if hasattr(session, 'created_at') else None
            }
        })
    
    @app.route('/api/user/sessions', methods=['GET'])
    def get_user_sessions():
        """Get active user sessions"""
        session, error_response, status_code = validate_token()
        if error_response:
            return jsonify(error_response), status_code
        
        try:
            sessions = session_manager.get_active_sessions(session.user_id)
            return jsonify({'sessions': sessions})
        except Exception as e:
            app.logger.error(f"Get sessions endpoint error: {e}")
            return jsonify({'error': 'Failed to retrieve sessions'}), 500
    
    # Health check and info endpoints
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })
    
    @app.route('/api/info', methods=['GET'])
    def app_info():
        """Application information"""
        return jsonify({
            'name': 'Language Tracker',
            'version': '1.0.0',
            'environment': app.config['FLASK_ENV'],
            'features': {
                'authentication': True,
                'firebase_auth': firebase_auth.is_firebase_available(),
                'session_management': True
            }
        })
    
    # React app routes - serve static files and handle client-side routing
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react_app(path):
        """Serve React application"""
        # Check if this is an API request that doesn't exist
        if path.startswith('api/'):
            return jsonify({'error': 'API endpoint not found'}), 404
        
        # Serve static files from build directory
        build_path = Path(app.root_path) / 'build'
        
        if build_path.exists():
            # Try to serve the requested file
            if path and (build_path / path).exists():
                return send_from_directory('build', path)
            
            # For client-side routing, serve index.html
            return send_from_directory('build', 'index.html')
        else:
            # Development mode - serve simple HTML page with links to auth forms
            return """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Language Tracker - Development</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                    .api-endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 4px; }
                    .method { font-weight: bold; color: #007bff; }
                </style>
            </head>
            <body>
                <h1>Language Tracker API Server</h1>
                <p>The Flask backend server is running successfully!</p>
                
                <h2>Available API Endpoints:</h2>
                
                <div class="api-endpoint">
                    <span class="method">POST</span> /api/auth/register - User registration
                </div>
                
                <div class="api-endpoint">
                    <span class="method">POST</span> /api/auth/login - User login
                </div>
                
                <div class="api-endpoint">
                    <span class="method">POST</span> /api/auth/firebase - Google OAuth login
                </div>
                
                <div class="api-endpoint">
                    <span class="method">GET</span> /api/auth/validate - Session validation
                </div>
                
                <div class="api-endpoint">
                    <span class="method">POST</span> /api/auth/logout - User logout
                </div>
                
                <div class="api-endpoint">
                    <span class="method">GET</span> /api/user/profile - User profile
                </div>
                
                <div class="api-endpoint">
                    <span class="method">GET</span> /api/health - Health check
                </div>
                
                <h3>Frontend Development:</h3>
                <p>To use the React frontend:</p>
                <ol>
                    <li>Install Node.js dependencies: <code>npm install</code></li>
                    <li>Build the React app: <code>npm run build</code></li>
                    <li>Restart this Flask server</li>
                </ol>
                
                <p>Or run React in development mode alongside this server on port 3000.</p>
            </body>
            </html>
            """
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'API endpoint not found'}), 404
        return serve_react_app('')
    
    @app.errorhandler(500)
    def internal_error(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error'}), 500
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    # Import datetime here to avoid circular imports
    from datetime import datetime
    
    # Database initialization
    db_path = app.config['DATABASE_PATH']
    if not os.path.exists(db_path):
        print(f"WARNING: Database not found at {db_path}")
        print("Initialize the database using the authentication tests first")
        print("   Run: python -m pytest features/authentication/tests/unit/")
    
    # Server configuration
    port = int(os.environ.get('PORT', 5001))
    debug = app.config['FLASK_ENV'] == 'development'
    
    print(f"Starting Language Tracker server...")
    print(f"Environment: {app.config['FLASK_ENV']}")
    print(f"Port: {port}")
    print(f"Debug mode: {debug}")
    print(f"Database: {db_path}")
    
    if debug:
        print(f"API Documentation: http://localhost:{port}")
        print(f"Health Check: http://localhost:{port}/api/health")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    )