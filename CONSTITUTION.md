---
resource_id: "b4804e3f-21b7-4c82-a2c7-f7516d232e5b"
---
# Language Tracker Development Constitution

<!-- section_id: "5e5a53b6-de3c-461b-9b9a-896936706e60" -->
## Environment Tier Structure

The Language Tracker project follows industry-standard four-tier environment progression:

<!-- section_id: "d6d78420-c2b4-4eac-abf0-c29a2c50ba3f" -->
### 1. Development Environment (`lang-trak-dev`)
- **Firebase Project**: `lang-trak-dev`
- **Google Cloud Console Project**: `lang-trak-dev`
- **Service Account**: `firebase-service-account-dev.json` (✅ Implemented)
- **Purpose**: Active feature development and initial testing
- **Usage**: Where developers work on new features and bug fixes

<!-- section_id: "273843bc-a438-4a97-b420-882c6ff2c8a2" -->
### 2. Testing Environment (`lang-trak-test`)
- **Firebase Project**: `lang-trak-test`
- **Google Cloud Console Project**: `lang-trak-test`
- **Service Account**: `firebase-service-account-test.json` (✅ Implemented)
- **Purpose**: Automated testing, QA validation, and integration testing
- **Usage**: Where comprehensive test suites run against stable feature branches

<!-- section_id: "14954ce3-a409-4f1c-be7f-9b0cc78cb0d2" -->
### 3. Staging Environment (`lang-trak-staging`)
- **Firebase Project**: `lang-trak-staging`
- **Google Cloud Console Project**: `lang-trak-staging`
- **Service Account**: `firebase-service-account-staging.json` (✅ Implemented)
- **Purpose**: Pre-production validation and final user acceptance testing
- **Usage**: Mirror of production for final validation before release

<!-- section_id: "b944927e-5ba4-4b85-9e75-c7b151aa3b1b" -->
### 4. Production Environment (`lang-trak-prod`)
- **Firebase Project**: `lang-trak-prod`
- **Google Cloud Console Project**: `lang-trak-prod`
- **Service Account**: `firebase-service-account-prod.json` (✅ Implemented)
- **Purpose**: Live application serving real users
- **Usage**: Production deployment with real data and users

<!-- section_id: "64f3091f-1d15-4229-aa80-6dda442a8911" -->
## Environment Isolation Standards

- **Emulators**: Used only for local unit testing
- **Real Firebase Projects**: Used for all environment tiers (dev, test, staging, prod)
- **WSL Requirement**: All operations must be executed within WSL environment
- **Service Account Segregation**: Each environment has dedicated service account credentials
- **Data Isolation**: Complete separation between environments to prevent cross-contamination

<!-- section_id: "33c4402f-f11e-4f99-a384-4d4c0d0325f7" -->
## Firebase and Google Cloud Best Practices

Following Google's recommended enterprise-grade practices:
- Separate Firebase projects for each environment tier
- Corresponding Google Cloud Console projects for advanced features
- Environment-specific service accounts with appropriate permissions
- Professional multi-environment workflow support
- Proper credential management and security practices

<!-- section_id: "d07b5b91-e099-4e01-b989-1c799f0c639f" -->
## Decision Framework

When working with Language Tracker:
1. Verify correct environment tier usage (dev → test → staging → prod)
2. Ensure proper service account credentials are available
3. Confirm execution within WSL environment
4. Validate environment isolation is maintained
5. Follow established deployment and testing workflows

This constitution ensures enterprise-grade, multi-environment professional standards supporting the full development lifecycle from initial development through production deployment.

<!-- section_id: "c05e8206-b99d-43a6-abb2-41fef5022725" -->
## Test-Driven Development (TDD) Requirements

<!-- section_id: "d3f2ef77-aa39-4e6d-b7fa-0cc7b94ddeda" -->
### Change Management Rule
**MANDATORY**: Every code change MUST correspond to a user story with defined features and sub-features.

<!-- section_id: "bcc548c1-45ec-4951-b47c-fa03632d600b" -->
### User Story Validation Requirements
1. **Story Definition**: All changes must reference specific user stories (US-XXX format)
2. **Feature Mapping**: Features and sub-features must be documented and updated as needed
3. **Test Coverage**: Each user story requires comprehensive automated test coverage
4. **Parallel Testing**: All tests must support parallel execution for efficiency

<!-- section_id: "67b101d9-c137-4214-9a05-5de950adb5f6" -->
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

<!-- section_id: "66033cec-fba2-4c94-b7a6-b190f2f205ca" -->
### Test Organization Structure
- `tests/user_stories/` - Dedicated user story automation folder
- `tests/user_stories/automations/` - Test execution configurations for parallel runs
- `tests/user_stories/fast/` - Fast test implementations
- `tests/user_stories/realistic/` - Realistic test implementations

<!-- section_id: "4b91e32a-8e79-4517-a4ac-e4561810fd54" -->
### Enforcement Protocol
All pull requests and changes must:
1. Reference valid user story ID
2. Update user story/feature documentation if needed
3. Include both fast and realistic test coverage
4. Pass all existing tests in parallel execution
5. Demonstrate user story completion through automated validation
