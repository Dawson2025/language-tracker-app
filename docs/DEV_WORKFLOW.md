# Development Workflow

Daily development workflow and common commands for Lang Trak.

## 🚀 Daily Development Routine

### 1. Start Development Session

```bash
# Navigate to project (in WSL)
cd /home/dawson/code/lang-trak-in-progress

# Setup development environment
bash scripts/setup-dev-env.sh

# Verify environment
echo $PROJECT_ID          # Should show: lang-trak-dev
firebase use              # Should show: lang-trak-dev

# Start Next.js development server
npm run dev
```

**Development server:** http://localhost:3000  
**Firebase project:** lang-trak-dev

### 2. Feature Development

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... edit files ...

# Test changes immediately in dev environment
# (already connected to lang-trak-dev)
```

### 3. Unit Testing

```bash
# Setup test environment (uses emulators)
bash scripts/setup-test-env.sh

# Verify test environment
echo $NODE_ENV                    # Should show: test
echo $USE_FIREBASE_EMULATOR      # Should show: true

# Start emulators (in separate terminal)
firebase emulators:start --only firestore,auth

# Run tests
npm test

# Or run specific tests
npm test -- --testPathPattern=components
```

**Emulator UI:** http://127.0.0.1:4002

### 4. Commit and Push

```bash
# Add changes
git add .

# Commit with descriptive message
git commit -m "feat: add user authentication flow"

# Push to remote
git push origin feature/your-feature-name
```

## 🔄 Environment Switching

### Quick Environment Commands

```bash
# Development (most common)
bash scripts/setup-dev-env.sh
npm run dev

# Unit testing
bash scripts/setup-test-env.sh
npm run emulator:start

# Staging (for testing deployments)
bash scripts/setup-staging-env.sh

# Production (deploy only, with caution)
bash scripts/setup-prod-env.sh
```

### Verify Current Environment

```bash
# Check all environment variables
echo "Project ID: $PROJECT_ID"
echo "Environment: $FIREBASE_ENV"
echo "Node Environment: $NODE_ENV"
echo "Using Emulator: $USE_FIREBASE_EMULATOR"

# Check Firebase CLI project
firebase use

# Check Google Cloud project (if using gcloud)
gcloud config get-value project
```

## 🧪 Testing Workflow

### Unit Testing with Emulators

```bash
# 1. Setup test environment
bash scripts/setup-test-env.sh

# 2. Start emulators (separate terminal)
npm run emulator:start

# 3. Run tests
npm test                          # All tests
npm test -- --watch              # Watch mode
npm test -- --coverage           # With coverage
npm test -- components/Button    # Specific test
```

### Integration Testing

```bash
# 1. Setup development environment
bash scripts/setup-dev-env.sh

# 2. Deploy latest code to dev project
firebase deploy

# 3. Run integration tests against real Firebase
npm run test:integration
```

## 📦 Deployment Workflow

### Deploy to Staging

```bash
# 1. Ensure all tests pass
bash scripts/setup-test-env.sh
npm run emulator:start
npm test

# 2. Switch to staging
bash scripts/setup-staging-env.sh

# 3. Deploy to staging
firebase deploy

# 4. Manual testing on staging
open https://lang-trak-staging.web.app

# 5. Run staging tests (if available)
npm run test:staging
```

### Deploy to Production

```bash
# 1. Ensure staging is tested and stable
# ... staging validation ...

# 2. Switch to production (with safety warnings)
bash scripts/setup-prod-env.sh

# 3. Deploy to production
firebase deploy
# Follow safety confirmations

# 4. Verify production deployment
open https://lang-trak-prod.web.app

# 5. Monitor logs
firebase functions:log
```

## 🛠️ Common Development Commands

### Firebase Commands

```bash
# Check current project
firebase use

# List all projects
firebase projects:list

# Switch projects manually
firebase use lang-trak-dev
firebase use lang-trak-staging
firebase use lang-trak-prod

# Deploy specific components
firebase deploy --only hosting
firebase deploy --only functions
firebase deploy --only firestore:rules
```

### Emulator Commands

```bash
# Start specific emulators
firebase emulators:start --only firestore
firebase emulators:start --only auth
firebase emulators:start --only firestore,auth

# Start with UI
firebase emulators:start --only firestore,auth,ui

# Check emulator status
curl http://127.0.0.1:8088    # Firestore
curl http://127.0.0.1:9099    # Auth
```

### Development Server Commands

```bash
# Start development server
npm run dev

# Start with specific port
npm run dev -- --port 3001

# Build for production
npm run build

# Start production build locally
npm run start
```

## 🔍 Debugging Workflow

### Firebase Debugging

```bash
# Check Firebase logs
firebase functions:log

# Debug specific function
firebase functions:log --only yourFunctionName

# Check Firestore rules
firebase firestore:rules:get

# Test Firestore rules
firebase firestore:rules:test
```

### Emulator Debugging

```bash
# Check emulator logs
firebase emulators:start --inspect-functions

# Reset emulator data
firebase emulators:start --import=./emulator-data --export-on-exit

# Emulator UI debugging
open http://127.0.0.1:4002
```

### Local Debugging

```bash
# Check Next.js build
npm run build

# Analyze bundle size
npm run analyze

# Check TypeScript
npm run type-check

# Lint code
npm run lint
```

## 📊 Monitoring and Logging

### Development Monitoring

```bash
# Check Firebase project console
open https://console.firebase.google.com/project/lang-trak-dev

# Monitor function logs
firebase functions:log --follow

# Check authentication users
firebase auth:export users.json
```

### Performance Monitoring

```bash
# Run Lighthouse audit
npm run lighthouse

# Check bundle size
npm run bundle-analyzer

# Test build performance
npm run build && npm run start
```

## 🚨 Emergency Procedures

### Rollback Production

```bash
# 1. Switch to production
bash scripts/setup-prod-env.sh

# 2. Check deployment history
firebase hosting:releases:list

# 3. Rollback to previous version
firebase hosting:releases:rollback <release-id>

# 4. Verify rollback
open https://lang-trak-prod.web.app
```

### Fix Broken Deployment

```bash
# 1. Switch to development
bash scripts/setup-dev-env.sh

# 2. Fix issue locally
# ... make fixes ...

# 3. Test with emulator
bash scripts/setup-test-env.sh
npm run emulator:start
npm test

# 4. Deploy fix to staging first
bash scripts/setup-staging-env.sh
firebase deploy

# 5. Verify fix, then deploy to production
bash scripts/setup-prod-env.sh
firebase deploy
```

## 💡 Tips and Tricks

### Efficiency Tips

```bash
# Use aliases for common commands
alias fdev="bash scripts/setup-dev-env.sh"
alias ftest="bash scripts/setup-test-env.sh"
alias fstaging="bash scripts/setup-staging-env.sh"

# Keep multiple terminals open
# Terminal 1: Development server (npm run dev)
# Terminal 2: Tests/emulators
# Terminal 3: Git/deployment commands
```

### Avoiding Common Mistakes

1. **Always verify environment before deployment**
   ```bash
   echo $PROJECT_ID && firebase use
   ```

2. **Never skip staging**
   ```bash
   # Always test in staging first
   bash scripts/setup-staging-env.sh
   firebase deploy
   ```

3. **Use emulators for unit tests only**
   ```bash
   # Don't develop against emulators
   # Use real dev project for development
   ```

## 📋 Daily Checklist

### Morning Routine
- [ ] `cd /home/dawson/code/lang-trak-in-progress`
- [ ] `bash scripts/setup-dev-env.sh`
- [ ] `git pull origin main`
- [ ] `npm run dev`

### Before Each Feature
- [ ] Create feature branch
- [ ] Verify development environment
- [ ] Write tests first (TDD)
- [ ] Start emulator for test-driven development

### Before Each Commit
- [ ] Run unit tests: `npm test`
- [ ] Check lint: `npm run lint`
- [ ] Build successfully: `npm run build`
- [ ] Commit with descriptive message

### Before Each Deployment
- [ ] All tests pass
- [ ] Deploy to staging first
- [ ] Manual testing on staging
- [ ] Verify environment before production deployment

---

**Questions?** Check [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for detailed setup instructions or [OPERATIONAL_STATUS.md](OPERATIONAL_STATUS.md) for current system status.