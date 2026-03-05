---
resource_id: "fa08fd85-0422-45cb-95e6-1939a2e59a8b"
---
# Lang Trak

A language learning tracking application built with Next.js and Firebase.

<!-- section_id: "1a638ae9-0733-4c1c-bcf4-3b4dcabf8d6a" -->
## 🚀 Quick Start

**Prerequisites:** WSL Ubuntu, Node.js, Firebase CLI, authenticated Google Cloud account

```bash
# Clone and setup
git clone <repository-url>
cd lang-trak-in-progress

# Install dependencies
npm install

# Setup development environment
bash scripts/setup-dev-env.sh

# Start development server
npm run dev

# Run unit tests with emulator
bash scripts/setup-test-env.sh
npm run emulator:start
npm test
```

<!-- section_id: "023f560e-0e61-4e49-a21c-a1c333a297e8" -->
## 🏗️ Architecture

- **Frontend:** Next.js with TypeScript
- **Backend:** Firebase (Firestore, Authentication, Functions)
- **Testing:** Firebase Emulators for unit tests
- **Environments:** Development, Staging, Production

<!-- section_id: "c0da5d66-b191-41e8-90bc-1bd1f260afef" -->
## 🔥 Firebase Setup

This project uses **Google's recommended Firebase best practices**:

- **Unit Testing:** Local emulators only (fast, free, isolated)
- **Development:** Real Firebase project (`lang-trak-dev`)
- **Staging:** Real Firebase project (`lang-trak-staging`) 
- **Production:** Real Firebase project (`lang-trak-prod`)

<!-- section_id: "fde7f111-7494-48f5-a3d1-022de4d9f541" -->
### Environment Scripts

All scripts must be run in **WSL terminal**:

```bash
# Development environment
bash scripts/setup-dev-env.sh

# Unit testing with emulators
bash scripts/setup-test-env.sh

# Staging environment
bash scripts/setup-staging-env.sh

# Production environment (with safety warnings)
bash scripts/setup-prod-env.sh
```

<!-- section_id: "39f31e61-d527-4a57-a380-0d52c50fa3db" -->
### NPM Scripts

```bash
npm run firebase:dev      # Setup development
npm run firebase:test     # Setup unit testing
npm run firebase:staging  # Setup staging
npm run firebase:prod     # Setup production
npm run emulator:start    # Start Firebase emulator
npm run emulator:ui       # Start emulator with UI
```

<!-- section_id: "e65988bd-d14e-4e25-a3a1-bcee3de5d5c3" -->
## 📁 Project Structure

```
lang-trak-in-progress/
├── src/                  # Next.js application source
├── functions/           # Firebase Cloud Functions
├── firestore.rules     # Firestore security rules
├── firebase.json       # Firebase configuration
├── scripts/            # Environment setup scripts
├── docs/              # Project documentation
└── package.json       # NPM configuration
```

<!-- section_id: "a92fa10b-58df-4520-bf9c-c1e74774f782" -->
## 🛠️ Development Workflow

1. **Start Development Session**
   ```bash
   bash scripts/setup-dev-env.sh
   npm run dev
   ```

2. **Write Unit Tests**
   ```bash
   bash scripts/setup-test-env.sh
   firebase emulators:start --only firestore,auth
   npm test
   ```

3. **Deploy to Staging**
   ```bash
   bash scripts/setup-staging-env.sh
   firebase deploy
   ```

4. **Deploy to Production**
   ```bash
   bash scripts/setup-prod-env.sh
   firebase deploy  # Includes safety confirmations
   ```

<!-- section_id: "89059950-e1e8-400f-a9df-43b39cfd2a75" -->
## 🌐 Environment URLs

- **Development:** `https://lang-trak-dev.web.app`
- **Staging:** `https://lang-trak-staging.web.app`  
- **Production:** `https://lang-trak-prod.web.app`
- **Emulator UI:** `http://127.0.0.1:4002`

<!-- section_id: "4635927e-4f75-448d-8cfb-38f5c5c5666e" -->
## 📚 Documentation

- [Quick Start Guide](docs/QUICK_START.md)
- [Firebase Setup Guide](docs/FIREBASE_SETUP.md)
- [Development Workflow](docs/DEV_WORKFLOW.md)
- [Google Firebase Best Practices](docs/GOOGLE_FIREBASE_BEST_PRACTICES.md)
- [Production Readiness](docs/PRODUCTION_READINESS.md)
- [Operational Status](docs/OPERATIONAL_STATUS.md)

<!-- section_id: "df943f90-68c1-46b8-9780-d1e9c5f60f2f" -->
## 🚨 Important Notes

**🚨 HARD RULE: ALL AUTOMATED TESTS MUST PASS BEFORE ANY PROGRESSION**
- **NO EXCEPTIONS** - This rule is enforced by CI/CD automation
- **Blocks all progression** - batch phases, PR merges, releases
- **Applies universally** - all development work, features, bug fixes
- **Automatic enforcement** - failing tests block merges via GitHub Actions

**Environment Standards:**
- **Always run Firebase commands in WSL** to avoid path issues
- **Use emulators for unit tests only** - never for development or staging
- **Production deployments require confirmation** - safety warnings included
- **Environment isolation is critical** - each environment has separate Firebase projects

<!-- section_id: "eaebc073-e14e-4b39-8546-a28709760a85" -->
## 🧪 Testing Requirements

**All code changes MUST include comprehensive test coverage:**

<!-- section_id: "b2afe700-dbe0-47ff-a339-21ea1a0ada07" -->
### Test Types Required
- **Unit Tests**: Fast (<30s), isolated component testing
- **Integration Tests**: API and database interaction testing
- **E2E Tests**: Full user workflows with Playwright + headed Chromium
- **User Story Tests**: Both fast and realistic versions for each user story

<!-- section_id: "1b9b0950-8e7d-4cee-ae85-b4e76be7e044" -->
### Running Tests Locally
```bash
# Unit tests
pytest tests/unit/ --verbose
npm run test:unit

# Integration tests
pytest tests/integration/ --verbose

# E2E tests (requires test environment)
npx playwright test tests/e2e/ --headed

# User story tests
npx playwright test tests/user_stories/ --headed

# All tests with coverage
coverage run -m pytest tests/ --verbose
coverage report --show-missing --fail-under=90
```

<!-- section_id: "631ae3c6-e1f0-4054-abf6-1b5ac38b6018" -->
### CI/CD Enforcement
- **GitHub Actions**: Automatically runs all tests on PR creation
- **Branch Protection**: Main branch requires all checks to pass
- **No Override**: Manual bypassing of test failures is not allowed
- **Coverage Requirement**: Minimum 90% code coverage enforced

<!-- section_id: "fb5d585e-11d4-4935-82f0-7bdc987e2b77" -->
## 🔧 Troubleshooting

**Common Issues:**

1. **Script execution errors:** Ensure you're running in WSL, not Windows PowerShell
2. **Firebase CLI errors:** Check authentication with `firebase login`
3. **Port conflicts:** Stop existing emulators with `Ctrl+C` before starting new ones
4. **Permission errors:** Verify service account permissions in Google Cloud Console

**Getting Help:**

- Check [Operational Status](docs/OPERATIONAL_STATUS.md) for current system status
- Review [Firebase Setup Guide](docs/FIREBASE_SETUP.md) for detailed instructions
- See [Production Readiness](docs/PRODUCTION_READINESS.md) for deployment checklists

<!-- section_id: "f3fd7ad5-0ae0-4377-b586-e3598954a9a0" -->
## 📄 License

[Add license information]

<!-- section_id: "5d75293d-0f1e-4173-8123-e0cea5f98053" -->
## 🤝 Contributing

[Add contributing guidelines]

---

**Status:** ✅ Fully Operational  
**Last Updated:** December 2024  
**Environment:** WSL Ubuntu