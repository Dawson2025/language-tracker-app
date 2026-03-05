---
resource_id: "166a9a27-b30f-48e6-af5c-ecd83ad7d81e"
---
# Pull Request Template

<!-- section_id: "089d4063-7668-46d6-a825-295614adffba" -->
## 🚨 HARD RULE ENFORCEMENT CHECKLIST

**Before this PR can be merged, ALL of the following MUST be checked:**

<!-- section_id: "b9ecbbc1-5692-4a7a-abd3-de0c4ae0cc26" -->
### ✅ Automated Testing Requirements (NON-NEGOTIABLE)

- [ ] **All unit tests pass locally** (`pytest tests/unit/` and `npm run test:unit`)
- [ ] **All integration tests pass locally** (`pytest tests/integration/`)
- [ ] **All E2E tests pass locally** (`npx playwright test tests/e2e/`)
- [ ] **All user story tests pass locally** (`npx playwright test tests/user_stories/`)
- [ ] **CI pipeline shows all green checkmarks** (wait for CI to complete)
- [ ] **Code coverage meets 90% minimum requirement**
- [ ] **No security vulnerabilities introduced** (audit checks pass)

<!-- section_id: "9125ec17-ca2b-4026-957b-72eb8b441447" -->
### 📋 User Story Alignment

- [ ] **User Story ID Referenced**: This PR implements/fixes: `US-XXX`
- [ ] **User Story Documentation Updated**: If this changes functionality, user story docs are updated
- [ ] **Acceptance Criteria Met**: All acceptance criteria for the user story are satisfied

<!-- section_id: "ae778707-0cc1-488f-88f5-4c9c7cbe8a78" -->
### 📚 Documentation Requirements

- [ ] **Trickle-Down Documentation Updated**: All relevant levels (TD0-TD4) have been updated
- [ ] **Code Comments Added**: New/complex code includes appropriate comments
- [ ] **API Documentation Updated**: If API changes were made, documentation is current
- [ ] **README Updates**: If setup/usage changes were made, README reflects them

<!-- section_id: "a747626e-ef6c-4be7-b50c-a46b1dbfe45a" -->
### 🧪 Testing Evidence

- [ ] **Both Fast and Realistic Tests**: User story has both fast (<30s) and realistic (<5min) test coverage
- [ ] **Playwright with Headed Chromium**: E2E tests use headed Chromium as required
- [ ] **Database Validation**: If Firestore interactions were added/modified, database validation tests exist
- [ ] **Parallel Test Execution**: All tests support parallel execution

<!-- section_id: "d57a3b44-e0be-485a-9698-5aa05f6f3e8e" -->
### 🔄 Change Management

- [ ] **Backwards Compatibility**: Changes maintain backwards compatibility where possible
- [ ] **Environment Isolation**: Changes respect dev/test/staging/prod isolation
- [ ] **Service Account Usage**: Correct service accounts used for each environment
- [ ] **WSL Environment**: All development/testing done within WSL environment

---

<!-- section_id: "af0e5d3e-dd3e-4340-8303-3a6e6e78f63c" -->
## 📝 Pull Request Details

<!-- section_id: "531edd83-af5d-45e3-933c-92b989a9be70" -->
### User Story Reference
**User Story ID**: `US-XXX`
**Link to User Story**: [Link to user story documentation]

<!-- section_id: "b68f6299-04aa-4008-932f-4bd50bf87b97" -->
### What Changed
<!-- Provide a clear description of what this PR changes/adds/fixes -->

<!-- section_id: "d49a442b-6d21-475e-a91a-43d6bd4c7f89" -->
### Why This Change
<!-- Explain the motivation for this change -->

<!-- section_id: "8dbed1d7-8e8c-4523-8ae8-a520fa48d3b4" -->
### How to Test
<!-- Provide step-by-step instructions for reviewers to test this change -->

<!-- section_id: "f606b430-0ad0-4446-a826-c6f60ed95fb0" -->
### Screenshots/Evidence
<!-- Include screenshots, test results, or other evidence of functionality -->

<!-- section_id: "09d2741c-ebcc-41d6-a8fa-36f0d6415453" -->
### Breaking Changes
<!-- List any breaking changes and migration steps required -->

---

<!-- section_id: "b7804d40-0df8-4235-b9a8-38708c0b2854" -->
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