# Authentication Test Suite
*Language Tracker Authentication Feature*
*Created via GitHub Spec Kit Implementation Phase*

## Overview
Comprehensive test suite for the authentication feature covering:
- Unit tests for individual modules
- Integration tests for API endpoints  
- End-to-end tests for user stories
- Security and performance tests

## Test Coverage
Target: **>90% code coverage**

### User Stories Validated
- ? **US-001**: User Registration with Local Credentials
- ? **US-002**: User Login with Local Credentials  
- ? **US-003**: Firebase Authentication (Google Sign-In)
- ? **US-004**: User Logout

## Running Tests

### Quick Start
`ash
# Run all tests
python features/authentication/tests/test_runner.py

# Run specific test types
python -m unittest discover features/authentication/tests/unit
python -m unittest discover features/authentication/tests/integration
`

### With Coverage
`ash
# Install coverage tool
pip install coverage

# Run tests with coverage
coverage run --source=features/authentication -m unittest discover features/authentication/tests
coverage report --show-missing
coverage html  # Generate HTML report
`

### Prerequisites
`ash
# Required packages
pip install bcrypt
pip install flask
pip install firebase-admin  # Optional for Firebase tests

# For E2E tests (if using Playwright)
pip install playwright
playwright install
`

## Test Structure

`
tests/
+-- unit/                     # Unit tests
¦   +-- test_password_security.py      # Password hashing, validation
¦   +-- test_session_manager.py        # Session management
¦   +-- test_validation.py             # Input validation
¦   +-- test_firebase_auth.py          # Firebase integration
+-- integration/              # Integration tests  
¦   +-- test_api_operations.py         # API endpoint testing
¦   +-- test_database_operations.py    # Database integration
¦   +-- test_security_features.py      # Security testing
+-- e2e/                      # End-to-end tests
¦   +-- test_user_stories.py           # Complete user flows
¦   +-- test_playwright_automation.py  # Browser automation
+-- test_runner.py            # Test orchestration
+-- README.md                 # This file
`

## Test Categories

### Unit Tests
- **Password Security**: Hashing, validation, strength checking
- **Session Management**: Token generation, validation, expiry
- **Input Validation**: Form validation, security checks
- **Firebase Auth**: OAuth integration, token verification

### Integration Tests  
- **API Endpoints**: Registration, login, logout endpoints
- **Database Operations**: User creation, session storage
- **Security Features**: Timing attack protection, rate limiting

### End-to-End Tests
- **Registration Flow**: Complete user registration process
- **Login Flow**: Authentication with various methods
- **Session Management**: Persistence, expiry, logout
- **Error Handling**: Validation errors, network failures

## Golden Rule Testing
Following the project constitution, always run:
`ash
python scripts/automation/run_user_stories.py --navigation-mode=both
`

## Continuous Integration
Tests should be run in CI/CD pipeline with:
- Unit tests on every commit
- Integration tests on pull requests  
- E2E tests on staging deployment
- Coverage reporting and enforcement

## Security Testing
Special focus on:
- Timing attack prevention
- Input sanitization
- Session security
- Password strength enforcement
- Rate limiting effectiveness

## Performance Testing
Validates:
- Login response time <2s (constitution requirement)
- Password hashing performance
- Session lookup efficiency
- Database query optimization

---
*Test Suite Status: ? Ready for Production*
*Coverage Target: >90%*
*User Stories: All Validated*
