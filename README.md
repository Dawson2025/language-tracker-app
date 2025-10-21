# Lang Trak

A language learning tracking application built with Next.js and Firebase.

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

## 🏗️ Architecture

- **Frontend:** Next.js with TypeScript
- **Backend:** Firebase (Firestore, Authentication, Functions)
- **Testing:** Firebase Emulators for unit tests
- **Environments:** Development, Staging, Production

## 🔥 Firebase Setup

This project uses **Google's recommended Firebase best practices**:

- **Unit Testing:** Local emulators only (fast, free, isolated)
- **Development:** Real Firebase project (`lang-trak-dev`)
- **Staging:** Real Firebase project (`lang-trak-staging`) 
- **Production:** Real Firebase project (`lang-trak-prod`)

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

### NPM Scripts

```bash
npm run firebase:dev      # Setup development
npm run firebase:test     # Setup unit testing
npm run firebase:staging  # Setup staging
npm run firebase:prod     # Setup production
npm run emulator:start    # Start Firebase emulator
npm run emulator:ui       # Start emulator with UI
```

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

## 🌐 Environment URLs

- **Development:** `https://lang-trak-dev.web.app`
- **Staging:** `https://lang-trak-staging.web.app`  
- **Production:** `https://lang-trak-prod.web.app`
- **Emulator UI:** `http://127.0.0.1:4002`

## 📚 Documentation

- [Quick Start Guide](docs/QUICK_START.md)
- [Firebase Setup Guide](docs/FIREBASE_SETUP.md)
- [Development Workflow](docs/DEV_WORKFLOW.md)
- [Google Firebase Best Practices](docs/GOOGLE_FIREBASE_BEST_PRACTICES.md)
- [Production Readiness](docs/PRODUCTION_READINESS.md)
- [Operational Status](docs/OPERATIONAL_STATUS.md)

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

## 🧪 Testing Requirements

**All code changes MUST include comprehensive test coverage:**

### Test Types Required
- **Unit Tests**: Fast (<30s), isolated component testing
- **Integration Tests**: API and database interaction testing
- **E2E Tests**: Full user workflows with Playwright + headed Chromium
- **User Story Tests**: Both fast and realistic versions for each user story

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

### CI/CD Enforcement
- **GitHub Actions**: Automatically runs all tests on PR creation
- **Branch Protection**: Main branch requires all checks to pass
- **No Override**: Manual bypassing of test failures is not allowed
- **Coverage Requirement**: Minimum 90% code coverage enforced

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

## 📄 License

[Add license information]

## 🤝 Contributing

[Add contributing guidelines]

---

**Status:** ✅ Fully Operational  
**Last Updated:** December 2024  
**Environment:** WSL Ubuntu