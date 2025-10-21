# Pull Request Template

## 🚨 HARD RULE ENFORCEMENT CHECKLIST

**Before this PR can be merged, ALL of the following MUST be checked:**

### ✅ Automated Testing Requirements (NON-NEGOTIABLE)

- [ ] **All unit tests pass locally** (`pytest tests/unit/` and `npm run test:unit`)
- [ ] **All integration tests pass locally** (`pytest tests/integration/`)
- [ ] **All E2E tests pass locally** (`npx playwright test tests/e2e/`)
- [ ] **All user story tests pass locally** (`npx playwright test tests/user_stories/`)
- [ ] **CI pipeline shows all green checkmarks** (wait for CI to complete)
- [ ] **Code coverage meets 90% minimum requirement**
- [ ] **No security vulnerabilities introduced** (audit checks pass)

### 📋 User Story Alignment

- [ ] **User Story ID Referenced**: This PR implements/fixes: `US-XXX`
- [ ] **User Story Documentation Updated**: If this changes functionality, user story docs are updated
- [ ] **Acceptance Criteria Met**: All acceptance criteria for the user story are satisfied

### 📚 Documentation Requirements

- [ ] **Trickle-Down Documentation Updated**: All relevant levels (TD0-TD4) have been updated
- [ ] **Code Comments Added**: New/complex code includes appropriate comments
- [ ] **API Documentation Updated**: If API changes were made, documentation is current
- [ ] **README Updates**: If setup/usage changes were made, README reflects them

### 🧪 Testing Evidence

- [ ] **Both Fast and Realistic Tests**: User story has both fast (<30s) and realistic (<5min) test coverage
- [ ] **Playwright with Headed Chromium**: E2E tests use headed Chromium as required
- [ ] **Database Validation**: If Firestore interactions were added/modified, database validation tests exist
- [ ] **Parallel Test Execution**: All tests support parallel execution

### 🔄 Change Management

- [ ] **Backwards Compatibility**: Changes maintain backwards compatibility where possible
- [ ] **Environment Isolation**: Changes respect dev/test/staging/prod isolation
- [ ] **Service Account Usage**: Correct service accounts used for each environment
- [ ] **WSL Environment**: All development/testing done within WSL environment

---

## 📝 Pull Request Details

### User Story Reference
**User Story ID**: `US-XXX`
**Link to User Story**: [Link to user story documentation]

### What Changed
<!-- Provide a clear description of what this PR changes/adds/fixes -->

### Why This Change
<!-- Explain the motivation for this change -->

### How to Test
<!-- Provide step-by-step instructions for reviewers to test this change -->

### Screenshots/Evidence
<!-- Include screenshots, test results, or other evidence of functionality -->

### Breaking Changes
<!-- List any breaking changes and migration steps required -->

---

## 🚨 Final Verification

**I certify that:**

- [ ] I have read and followed all Universal Instructions (TD0)
- [ ] I have read and followed the Project Constitution (TD1)
- [ ] All automated tests pass both locally and in CI
- [ ] This PR cannot and will not be merged until ALL tests pass
- [ ] I understand that failing tests will automatically block this PR
- [ ] I have updated all relevant documentation levels
- [ ] I have tested this change in the appropriate environment(s)
- [ ] I have followed all security and coding standards

---

**⚠️ REMINDER: The Hard Testing Rule means NO EXCEPTIONS. This PR will be automatically blocked if any tests fail. The CI pipeline must show all green checkmarks before merge is possible.**