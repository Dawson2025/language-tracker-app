# Language Tracker Development Constitution

## Environment Tier Structure

The Language Tracker project follows industry-standard four-tier environment progression:

### 1. Development Environment (`lang-trak-dev`)
- **Firebase Project**: `lang-trak-dev`
- **Google Cloud Console Project**: `lang-trak-dev`
- **Service Account**: `firebase-service-account-dev.json` (✅ Implemented)
- **Purpose**: Active feature development and initial testing
- **Usage**: Where developers work on new features and bug fixes

### 2. Testing Environment (`lang-trak-test`)
- **Firebase Project**: `lang-trak-test`
- **Google Cloud Console Project**: `lang-trak-test`
- **Service Account**: `firebase-service-account-test.json` (✅ Implemented)
- **Purpose**: Automated testing, QA validation, and integration testing
- **Usage**: Where comprehensive test suites run against stable feature branches

### 3. Staging Environment (`lang-trak-staging`)
- **Firebase Project**: `lang-trak-staging`
- **Google Cloud Console Project**: `lang-trak-staging`
- **Service Account**: `firebase-service-account-staging.json` (✅ Implemented)
- **Purpose**: Pre-production validation and final user acceptance testing
- **Usage**: Mirror of production for final validation before release

### 4. Production Environment (`lang-trak-prod`)
- **Firebase Project**: `lang-trak-prod`
- **Google Cloud Console Project**: `lang-trak-prod`
- **Service Account**: `firebase-service-account-prod.json` (✅ Implemented)
- **Purpose**: Live application serving real users
- **Usage**: Production deployment with real data and users

## Environment Isolation Standards

- **Emulators**: Used only for local unit testing
- **Real Firebase Projects**: Used for all environment tiers (dev, test, staging, prod)
- **WSL Requirement**: All operations must be executed within WSL environment
- **Service Account Segregation**: Each environment has dedicated service account credentials
- **Data Isolation**: Complete separation between environments to prevent cross-contamination

## Firebase and Google Cloud Best Practices

Following Google's recommended enterprise-grade practices:
- Separate Firebase projects for each environment tier
- Corresponding Google Cloud Console projects for advanced features
- Environment-specific service accounts with appropriate permissions
- Professional multi-environment workflow support
- Proper credential management and security practices

## Decision Framework

When working with Language Tracker:
1. Verify correct environment tier usage (dev → test → staging → prod)
2. Ensure proper service account credentials are available
3. Confirm execution within WSL environment
4. Validate environment isolation is maintained
5. Follow established deployment and testing workflows

This constitution ensures enterprise-grade, multi-environment professional standards supporting the full development lifecycle from initial development through production deployment.

## Test-Driven Development (TDD) Requirements

### Change Management Rule
**MANDATORY**: Every code change MUST correspond to a user story with defined features and sub-features.

### User Story Validation Requirements
1. **Story Definition**: All changes must reference specific user stories (US-XXX format)
2. **Feature Mapping**: Features and sub-features must be documented and updated as needed
3. **Test Coverage**: Each user story requires comprehensive automated test coverage
4. **Parallel Testing**: All tests must support parallel execution for efficiency

### Playwright MCP Testing Standards
**REQUIRED**: Every user story must have both fast and realistic test automation using Playwright MCP with headed Chromium:

#### Fast Tests
- Minimal UI interactions
- Mock external dependencies  
- Focus on core functionality validation
- Target: <30 seconds per test

#### Realistic Tests
- Full end-to-end workflows
- Real Firebase/backend interactions
- Complete user journey validation
- Target: <5 minutes per test

### Test Organization Structure
- `tests/user_stories/` - Dedicated user story automation folder
- `tests/user_stories/automations/` - Test execution configurations for parallel runs
- `tests/user_stories/fast/` - Fast test implementations
- `tests/user_stories/realistic/` - Realistic test implementations

### Enforcement Protocol
All pull requests and changes must:
1. Reference valid user story ID
2. Update user story/feature documentation if needed
3. Include both fast and realistic test coverage
4. Pass all existing tests in parallel execution
5. Demonstrate user story completion through automated validation
