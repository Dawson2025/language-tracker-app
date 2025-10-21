# Quick Start Guide

Get Lang Trak up and running in 5 minutes!

## Prerequisites ✅

Make sure you have these installed:

- **WSL Ubuntu** (required for Firebase scripts)
- **Node.js** (16+ recommended)
- **Firebase CLI** (`npm install -g firebase-tools`)
- **Google Cloud CLI** (optional but recommended)
- **Authenticated Google Account** with access to Firebase projects

## Step 1: Clone and Install

```bash
# Clone the repository
git clone <repository-url>
cd lang-trak-in-progress

# Install dependencies
npm install
```

## Step 2: Verify Firebase Setup

```bash
# Check Firebase authentication
firebase login

# List available projects
firebase projects:list

# Verify you can see:
# - lang-trak-dev
# - lang-trak-staging  
# - lang-trak-prod
```

## Step 3: Start Development

**⚠️ Important: Run all Firebase commands in WSL terminal, not Windows PowerShell**

```bash
# Setup development environment
bash scripts/setup-dev-env.sh

# Start Next.js development server
npm run dev
```

Your app should now be running at `http://localhost:3000`

## Step 4: Run Unit Tests

```bash
# Setup test environment (uses emulators)
bash scripts/setup-test-env.sh

# Start Firebase emulators in another terminal
firebase emulators:start --only firestore,auth

# Run tests
npm test
```

Emulator UI will be available at `http://127.0.0.1:4002`

## Step 5: Verify Everything Works

### Check Development Environment
```bash
# Should show: lang-trak-dev
firebase use

# Should show development project info
firebase projects:list --filter="lang-trak-dev"
```

### Check Emulator
```bash
# Start emulator
firebase emulators:start --only firestore,auth

# In another terminal, verify connection
curl http://127.0.0.1:8088
```

### Check NPM Scripts
```bash
# Test environment switching
npm run firebase:dev
npm run firebase:test
npm run firebase:staging
```

## Common Commands

### Daily Development
```bash
# Start your development session
bash scripts/setup-dev-env.sh
npm run dev
```

### Unit Testing
```bash
# Setup test environment
bash scripts/setup-test-env.sh

# Start emulators
npm run emulator:start

# Run tests
npm test
```

### Environment Switching
```bash
npm run firebase:dev      # Development
npm run firebase:test     # Unit testing
npm run firebase:staging  # Staging
npm run firebase:prod     # Production
```

## Troubleshooting 🔧

### "Command not found" errors
- **Problem:** Running scripts from Windows PowerShell
- **Solution:** Always use WSL terminal: `wsl` then run commands

### "Permission denied" errors
- **Problem:** Scripts not executable
- **Solution:** `chmod +x scripts/*.sh`

### "Project not found" errors
- **Problem:** Not authenticated with Firebase
- **Solution:** `firebase login` and verify project access

### Port conflicts
- **Problem:** Emulator ports already in use
- **Solution:** Stop existing processes: `Ctrl+C` or `lsof -i :8088`

### Line ending issues
- **Problem:** Scripts won't execute (Windows CRLF)
- **Solution:** Scripts already fixed with Unix LF endings

## Environment Overview

| Environment | Purpose | Firebase Project | URL |
|-------------|---------|------------------|-----|
| **Test** | Unit testing only | Local emulators | `http://127.0.0.1:4002` |
| **Development** | Daily development | `lang-trak-dev` | `https://lang-trak-dev.web.app` |
| **Staging** | Pre-production testing | `lang-trak-staging` | `https://lang-trak-staging.web.app` |
| **Production** | Live application | `lang-trak-prod` | `https://lang-trak-prod.web.app` |

## Next Steps

1. **Read the docs:** Check out [Firebase Setup Guide](FIREBASE_SETUP.md)
2. **Development workflow:** See [Development Workflow](DEV_WORKFLOW.md)  
3. **Deploy to staging:** Follow [Production Readiness](PRODUCTION_READINESS.md)
4. **Monitor status:** Check [Operational Status](OPERATIONAL_STATUS.md)

---

**Need help?** Check the full [Firebase Setup Guide](FIREBASE_SETUP.md) or [Troubleshooting section](FIREBASE_SETUP.md#troubleshooting) for detailed solutions.

**Ready to develop?** 🚀 Run `bash scripts/setup-dev-env.sh` and start coding!