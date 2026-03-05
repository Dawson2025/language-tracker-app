---
resource_id: "c8b0638e-c705-4cb4-9191-a33c06976c77"
---
# Development Workflow

Daily development workflow and common commands for Lang Trak.

<!-- section_id: "4db47208-7959-4c8c-a575-f9f6dfd7e0eb" -->
## 🚀 Daily Development Routine

<!-- section_id: "b9237fe7-66a1-4902-9068-30eb7ea358de" -->
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

<!-- section_id: "60225f52-99a7-4e28-8a93-8613015ac787" -->
### 2. Feature Development

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... edit files ...

# Test changes immediately in dev environment
# (already connected to lang-trak-dev)
```

<!-- section_id: "6b62a564-a558-4043-973e-c9924cb63071" -->
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

<!-- section_id: "2134beab-c8f0-4618-a122-779fc5a0e036" -->
### 4. Commit and Push

```bash
# Add changes
git add .

# Commit with descriptive message
git commit -m "feat: add user authentication flow"

# Push to remote
git push origin feature/your-feature-name
```

<!-- section_id: "ceb08c5a-ed36-4d90-bdfd-e77f1c802bb8" -->
## 🔄 Environment Switching

<!-- section_id: "8da70a1e-52ce-4c51-b307-a22eecb91ebb" -->
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

<!-- section_id: "f98c1e43-a24c-4f7e-bb98-9187fba12f03" -->
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

<!-- section_id: "ec3922bc-58cf-4fd9-8c10-cc7c12289070" -->
## 🧪 Testing Workflow

<!-- section_id: "08df3e3f-2a86-4919-a1f9-876771ed6180" -->
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

<!-- section_id: "e3cb7e52-e8a6-4fa4-830c-dd04a74a90e9" -->
### Integration Testing

```bash
# 1. Setup development environment
bash scripts/setup-dev-env.sh

# 2. Deploy latest code to dev project
firebase deploy

# 3. Run integration tests against real Firebase
npm run test:integration
```

<!-- section_id: "ce16948f-a396-45fe-841b-c1a0f2d43a3f" -->
## 📦 Deployment Workflow

<!-- section_id: "2898cfe0-ac2a-4a8f-85fc-f836fdb33053" -->
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

<!-- section_id: "c1f403fa-dfc5-400d-a332-369cec4581f8" -->
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

<!-- section_id: "675b6e95-e659-4063-a673-4aab700d3b4f" -->
## 🛠️ Common Development Commands

<!-- section_id: "7e8f556c-9b6e-4e35-b19a-1e5dfc730710" -->
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

<!-- section_id: "dc7d595b-6739-4da1-8989-a8fa087df1ef" -->
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

<!-- section_id: "8fd62264-6deb-4fe1-adeb-babcfd089f73" -->
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

<!-- section_id: "af12a684-bef1-422e-815c-c1d55da28b39" -->
## 🔍 Debugging Workflow

<!-- section_id: "f7f6343a-5eab-4d89-aa2e-44a7c42e7d13" -->
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

<!-- section_id: "c02f11d3-33f0-40a0-a924-52c5d9ea86d6" -->
### Emulator Debugging

```bash
# Check emulator logs
firebase emulators:start --inspect-functions

# Reset emulator data
firebase emulators:start --import=./emulator-data --export-on-exit

# Emulator UI debugging
open http://127.0.0.1:4002
```

<!-- section_id: "1a53b142-4c04-4999-857f-60b61acd78cd" -->
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

<!-- section_id: "e86e147b-8df9-4612-abbd-6c83238514ef" -->
## 📊 Monitoring and Logging

<!-- section_id: "bbde79d8-bf8d-44d3-8478-d1bb71f3fcb9" -->
### Development Monitoring

```bash
# Check Firebase project console
open https://console.firebase.google.com/project/lang-trak-dev

# Monitor function logs
firebase functions:log --follow

# Check authentication users
firebase auth:export users.json
```

<!-- section_id: "8325d91b-670f-4aa3-85a5-1b073caf6fab" -->
### Performance Monitoring

```bash
# Run Lighthouse audit
npm run lighthouse

# Check bundle size
npm run bundle-analyzer

# Test build performance
npm run build && npm run start
```

<!-- section_id: "f065bc23-3f57-4b18-a850-a041acab740a" -->
## 🚨 Emergency Procedures

<!-- section_id: "c01ece77-33c8-4838-83e0-9882020e8d43" -->
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

<!-- section_id: "083c275f-fee5-4c48-954b-8808ea953abb" -->
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

<!-- section_id: "32ee640c-3e6a-49f6-9f32-9f79345076b8" -->
## 💡 Tips and Tricks

<!-- section_id: "4dd13624-3ee9-4a61-a47a-9a9a18c4dd25" -->
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

<!-- section_id: "e862afd8-b8cd-4490-88b0-045b44fb096e" -->
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

<!-- section_id: "bf93988d-3beb-4583-a527-ed440ca9cb84" -->
## 📋 Daily Checklist

<!-- section_id: "22a0d5ef-6da9-46de-a1f8-9e5cf994c7c4" -->
### Morning Routine
- [ ] `cd /home/dawson/code/lang-trak-in-progress`
- [ ] `bash scripts/setup-dev-env.sh`
- [ ] `git pull origin main`
- [ ] `npm run dev`

<!-- section_id: "8f9bdd9f-476f-43c0-9456-dd3af38442f4" -->
### Before Each Feature
- [ ] Create feature branch
- [ ] Verify development environment
- [ ] Write tests first (TDD)
- [ ] Start emulator for test-driven development

<!-- section_id: "6c7d3879-db44-47e1-9b55-385139a068c2" -->
### Before Each Commit
- [ ] Run unit tests: `npm test`
- [ ] Check lint: `npm run lint`
- [ ] Build successfully: `npm run build`
- [ ] Commit with descriptive message

<!-- section_id: "99eaec58-c35e-4d58-a977-77f6a9822ac6" -->
### Before Each Deployment
- [ ] All tests pass
- [ ] Deploy to staging first
- [ ] Manual testing on staging
- [ ] Verify environment before production deployment

---

**Questions?** Check [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for detailed setup instructions or [OPERATIONAL_STATUS.md](OPERATIONAL_STATUS.md) for current system status.