# Language Tracker Project Constitution - Trickle-Down Level 1

## 📋 Prerequisites

**Before reading this document, you MUST have completed:**
- ✅ [Universal Instructions](../trickle-down-0-universal/UNIVERSAL_INSTRUCTIONS.md) - Trickle-Down Level 0

## 🎯 Project Constitution Overview

This document establishes the **fundamental rules and standards** for the Language Tracker project. All team members and AI agents must follow these requirements without exception.

## 🏗️ Environment Tier Structure

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

## 🔒 Environment Isolation Standards

- **Emulators**: Used only for local unit testing
- **Real Firebase Projects**: Used for all environment tiers (dev, test, staging, prod)
- **WSL Requirement**: All operations must be executed within WSL environment
- **Service Account Segregation**: Each environment has dedicated service account credentials
- **Data Isolation**: Complete separation between environments to prevent cross-contamination

## ☁️ Firebase and Google Cloud Best Practices

Following Google's recommended enterprise-grade practices:
- Separate Firebase projects for each environment tier
- Corresponding Google Cloud Console projects for advanced features
- Environment-specific service accounts with appropriate permissions
- Professional multi-environment workflow support
- Proper credential management and security practices

## 🧪 Test-Driven Development (TDD) Requirements

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

**🚨 PROJECT-SPECIFIC TESTING REQUIREMENTS:**
- All automated tests (unit, integration, e2e) must pass via CI before:
  - Batch progressions between development phases
  - PR merges to main branch
  - Production releases
- Use Playwright MCP server with headed Chromium for UI testing
- Include both fast and realistic test versions for each user story
- Database validation tests for Firestore collections during cloud operations
- No manual overrides or exceptions allowed

## 🚨 Decision Framework

When working with Language Tracker:
1. Verify correct environment tier usage (dev → test → staging → prod)
2. Ensure proper service account credentials are available
3. Confirm execution within WSL environment
4. Validate environment isolation is maintained
5. Follow established deployment and testing workflows

## 📊 Quality Gates

### Code Quality Requirements
- All code must pass linting and static analysis
- Code coverage must be maintained above 80%
- No security vulnerabilities above medium severity
- Performance tests must pass for critical paths

### Documentation Requirements
- All trickle-down documentation levels must be updated
- User stories must reflect current feature state
- API documentation must be current and accurate
- Architecture diagrams must reflect current system state

### Testing Requirements
- Both fast and realistic tests must pass
- Cross-browser compatibility tests must pass
- Performance tests must meet established benchmarks
- Security tests must validate proper authentication and authorization

## 🔄 Continuous Integration/Continuous Deployment (CI/CD)

### Deployment Pipeline
```
Feature Branch → Development → Testing → Staging → Production
     ↓              ↓           ↓          ↓          ↓
   Unit Tests   Integration  E2E Tests  UAT Tests  Monitoring
                   Tests
```

### Environment Promotion Rules
- Development: Automatic deployment on merge to main branch
- Testing: Manual promotion after development validation
- Staging: Manual promotion after testing sign-off
- Production: Manual promotion after staging validation

### Rollback Procedures
- Automatic rollback on critical failures
- Manual rollback capability for all environments
- Data migration rollback plans required
- User notification procedures for production rollbacks

## 🛡️ Security Standards

### Authentication and Authorization
- Firebase Auth integration required for all user features
- Role-based access control (RBAC) implementation
- Session management with appropriate timeouts
- Multi-factor authentication support for admin features

### Data Protection
- All user data encrypted in transit and at rest
- PII data handling according to privacy regulations
- Data retention policies implemented and enforced
- Regular security audits and penetration testing

### Development Security
- No hardcoded secrets in code or configuration
- Environment-specific service accounts with minimal permissions
- Regular dependency updates and vulnerability scanning
- Secure coding practices training for all developers

## 📈 Monitoring and Observability

### Application Monitoring
- Real-time error tracking and alerting
- Performance monitoring with established SLAs
- User experience monitoring and analytics
- Resource utilization tracking across all environments

### Business Metrics
- User engagement and retention metrics
- Feature adoption and usage statistics
- Performance indicators for learning outcomes
- System reliability and availability metrics

### Alerting Strategy
- Critical alerts for system outages
- Warning alerts for performance degradation
- Business metric alerts for anomalous patterns
- Escalation procedures for different alert types

## 🔗 Next Steps

After reading this document completely, proceed to other Trickle-Down Level 1 documents:

- **[USER_STORIES.md](./USER_STORIES.md)** - Complete user story definitions
- **[TDD_FRAMEWORK.md](./TDD_FRAMEWORK.md)** - Detailed TDD implementation
- **[FIREBASE_ARCHITECTURE.md](./FIREBASE_ARCHITECTURE.md)** - Firebase setup details

---

*This Project Constitution establishes non-negotiable standards for all Language Tracker development work. Adherence to these principles ensures project quality, security, and maintainability.*